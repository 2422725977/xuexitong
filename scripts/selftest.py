#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
selftest.py —— 伪装层 / 风控层回归测试（不联网，秒级跑完）。

    python3 scripts/selftest.py          # 全跑
    python3 scripts/selftest.py -v       # 打印每条用例

覆盖四组：
  A 判级器语料（risk_guard.CORPUS）：真风控文案 → HALT/COOLDOWN，业务错误 → NOTICE，成功 → OK
  B 闸门与熔断：HALT 抛 RiskHalt / 熔断拦截 / COOLDOWN 抛 RiskCooldown / 配额与静默硬阻塞即抛
  C 调用方熔断：autosign.main 与 qr_sign_remote.Signer.handle 在风控下优雅停机、不继续重试
  D 审计脱敏：长值变 abc***，只留必要参数

任何一条 FAIL → 退出码 1。
"""
import contextlib
import io
import json
import os
import sys
import time
import types

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import stealth_session as S
from risk_guard import CORPUS
import autosign as A
import qr_sign_remote as Q

PASS, FAIL = [], []


def check(name, ok, detail=""):
    (PASS if ok else FAIL).append(name)
    if VERBOSE:
        print("  %s %s %s" % ("PASS" if ok else "FAIL", name, ("| " + str(detail)[:90]) if detail else ""))


class FakeResp:
    def __init__(self, body, code=200):
        self.text = body
        self.status_code = code
        self.content = body.encode()
        self.headers = {}


def reset_state():
    rg = S.RateGovernor()
    rg.writes, rg.last_write, rg.cooldown_until = [], 0.0, 0.0
    rg.save()
    S.RiskGuard().reset()


def mk(per_hour=100, min_interval=0.0, quiet=None):
    ss = S.StealthSession(uid="10000000", audit=False, max_writes_per_hour=per_hour,
                          min_interval=min_interval, quiet=quiet)
    ss.cover_traffic = lambda n=1, quiet=True: []
    return ss


# ---------------- A 判级器 ----------------
def group_a():
    print("[A] 判级器语料 %d 条" % len(CORPUS))
    for name, status, body, want in CORPUS:
        g = S.RiskGuard(path="/tmp/.cx_risk_selftest.json")
        got = g.classify(status, body)["level"]
        check("A/%s" % name, got == want, "期望 %s 得到 %s" % (want, got))


# ---------------- B 闸门与熔断 ----------------
def group_b():
    print("[B] 闸门与熔断")
    reset_state()
    ss = mk()
    ss.session.request = lambda m, u, **kw: FakeResp("请先登录再进行签到")
    try:
        ss.get("https://mobilelearn.chaoxing.com/pptSign/stuSignajax?enc=x&activeId=1")
        check("B/写操作 HALT 抛 RiskHalt", False, "没抛异常")
    except S.RiskHalt as e:
        check("B/写操作 HALT 抛 RiskHalt", True, str(e)[:50])
    check("B/HALT 记入停机", ss.guard.state["halted"] is True)
    try:
        ss.get("https://mobilelearn.chaoxing.com/pptSign/stuSignajax?enc=y")
        check("B/停机后熔断拦截", False)
    except RuntimeError:
        check("B/停机后熔断拦截", True)

    ss.guard.reset()
    ss.rate.cooldown_until = 0
    ss.session.request = lambda m, u, **kw: FakeResp("操作频繁，请稍后再试")
    try:
        ss.get("https://mobilelearn.chaoxing.com/pptSign/stuSignajax?enc=z")
        check("B/限流抛 RiskCooldown", False)
    except S.RiskCooldown:
        check("B/限流抛 RiskCooldown", True)
    check("B/冷却已持久化", S.RateGovernor().cooldown_until > time.time())

    reset_state()
    ss2 = mk(per_hour=1)
    ss2.rate.cooldown_until = 0
    ss2.session.request = lambda m, u, **kw: FakeResp("success")
    r = ss2.get("https://mobilelearn.chaoxing.com/pptSign/stuSignajax?a=1")
    check("B/首次写放行", r.status_code == 200)
    try:
        ss2.get("https://mobilelearn.chaoxing.com/pptSign/stuSignajax?a=2")
        check("B/配额满即抛(不睡满)", False)
    except S.RiskCooldown:
        check("B/配额满即抛(不睡满)", True)

    ss4 = mk(quiet=(0, 24))
    ok, need, why = ss4.rate.check()
    check("B/静默时段判定", ok is False and "静默" in why)
    try:
        ss4.session.request = lambda m, u, **kw: FakeResp("success")
        ss4.get("https://fanyappfy.chaoxing.com/usersign/addsign?signId=2")
        check("B/静默时段即抛(不挂住)", False)
    except S.RiskCooldown:
        check("B/静默时段即抛(不挂住)", True)

    # 冷却超过 max_sleep → 抛而不是睡
    rg = S.RateGovernor()
    rg.cooldown(30)
    try:
        rg.wait_for_slot(max_sleep=90)
        check("B/长冷却不阻塞进程", False)
    except S.RiskCooldown:
        check("B/长冷却不阻塞进程", True)
    rg.cooldown(-10 ** 6)

    reset_state()
    ss3 = mk()
    ss3.session.request = lambda m, u, **kw: FakeResp('{"msg":"signId  not exists","statusCode":308}')
    ss3.get("https://fanyappfy.chaoxing.com/usersign/addsign?signId=1")
    check("B/业务错误不停机", ss3.guard.state["halted"] is False)

    check("B/静默时段解析",
          S.parse_quiet("1-7") == (1, 7) and S.parse_quiet("none") is None
          and S.parse_quiet("22-6") == (22, 6) and S.parse_quiet(None) == (1, 7))
    try:
        S.parse_quiet("abc")
        check("B/非法静默时段被拒", False)
    except ValueError:
        check("B/非法静默时段被拒", True)


# ---------------- C 调用方熔断 ----------------
def group_c():
    print("[C] 调用方熔断（autosign / qr_sign_remote）")
    A.list_activities = lambda *a, **k: [{"activeId": "111", "signType": 2}]
    A.detail = lambda *a, **k: {}

    def raiser(exc):
        def _f(*a, **k):
            raise exc
        return _f

    for label, exc, mark, extra in (("HALT", A.RiskHalt("登录态失效"), "[STOP] 风控停机", "未成功"),
                                    ("COOLDOWN", A.RiskCooldown("被限流"), "[WAIT]", None)):
        A.submit = raiser(exc)
        buf = io.StringIO()
        argv = sys.argv
        sys.argv = ["autosign.py", "--uid", "10000000"]
        try:
            with contextlib.redirect_stdout(buf):
                A.main()
        finally:
            sys.argv = argv
        out = buf.getvalue()
        check("C/autosign %s 优雅停机" % label, mark in out)
        if extra:
            check("C/autosign %s 未继续提交" % label, extra not in out)

    A.submit = lambda *a, **k: (True, "success")
    buf = io.StringIO()
    argv = sys.argv
    sys.argv = ["autosign.py", "--uid", "10000000"]
    try:
        with contextlib.redirect_stdout(buf):
            A.main()
    finally:
        sys.argv = argv
    check("C/autosign 正常路径仍成功", "签到成功" in buf.getvalue())

    class HaltSess:
        def get(self, url, **kw):
            raise S.RiskHalt("登录态失效：真的登录一次再来")

        def __getattr__(self, k):
            return lambda *a, **k2: FakeResp("")

    class CoolSess(HaltSess):
        def get(self, url, **kw):
            raise S.RiskCooldown("被限流，已冷却 30 分钟")

    def qargs():
        return types.SimpleNamespace(repeat=1, interval=0.1, append_log="", name="张三", fid="0",
                                     lat="-1", lon="-1", phone_id="a" * 32, uid="10000000", stealth=True)

    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        res = Q.Signer(qargs(), HaltSess()).handle(
            "https://mobilelearn.chaoxing.com/widget/sign/e?id=123&c=99&enc=abc", source="st")
    check("C/qr 通道 C HALT 停机", res.get("halt") is True)
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        res2 = Q.Signer(qargs(), CoolSess()).handle(
            "https://mobilelearn.chaoxing.com/widget/sign/e?id=124&c=99&enc=abc", source="st")
    check("C/qr 通道 C 冷却停手", res2.get("cooldown") is True)
    buf = io.StringIO()
    sg = Q.Signer(qargs(), HaltSess())          # 去重是 per-Signer 的，必须同一个实例
    with contextlib.redirect_stdout(buf):
        res3 = sg.handle(json.dumps({"time": 1, "signId": 2}), source="st")
        dup = sg.handle(json.dumps({"time": 1, "signId": 2}), source="st")
    check("C/qr 通道 A HALT 停机", res3.get("halt") is True and res3.get("kind") == "json")
    check("C/qr 去重仍生效", dup.get("dup") is True)


# ---------------- D 审计脱敏 ----------------
def group_d():
    print("[D] 审计脱敏")
    ss = mk()
    ss.audit_on = True
    ss.audit("GET", "https://mobilelearn.chaoxing.com/newsign/studentSign?rcode=SECRETVALUE&uid=10000000"
                    "&activeId=987&courseId=12345", 200, 12, 30, "OK", "OK")
    last = json.loads(open(S.AUDIT_PATH, encoding="utf-8").read().strip().splitlines()[-1])
    check("D/长值被打码", "SECRETVALUE" not in last["url"] and "SEC***" in last["url"])
    check("D/关键参数保留", "uid=10000000" in last["url"] and "activeId=987" in last["url"])
    check("D/记录结论与耗时", last["verdict"] == "OK" and last["ms"] == 30)
    rep = ss.report()
    check("D/report 结构完整", set(["writes", "reads", "tls", "device", "rate", "risk"]) <= set(rep))


VERBOSE = "-v" in sys.argv or "--verbose" in sys.argv

if __name__ == "__main__":
    t0 = time.time()
    reset_state()
    group_a()
    group_b()
    group_c()
    group_d()
    reset_state()
    print("\n结果: %d 通过, %d 失败, 用时 %.1fs" % (len(PASS), len(FAIL), time.time() - t0))
    for f in FAIL:
        print("  FAIL:", f)
    sys.exit(1 if FAIL else 0)
