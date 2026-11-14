#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
risk_guard.py —— 风控层独立 CLI / 回归测试。

stealth_session.RiskGuard 负责"判级 + strikes + 熔断"，本脚本负责：
  --selftest     用 13 个人工构造响应（含真风控文案与业务错误）回归判级器，防止误判/漏判
  --check FILE   对一个真实响应体判级（配合 -i / curl 存下来的响应）
  --decide URL   模拟一次"看到这个响应会发生什么"（打印 level 与最终 action，不写状态）
  --monitor      盯审计日志（~/.chaoxing_audit.jsonl），实时打印 HALT/COOLDOWN
  --state        打印当前 strikes / 冷却 / 停机
  --reset        清空冷却与停机（先确认已经处理完风控原因）

判级语义（与 stealth_session 一致）：
  HALT     立刻停机：登录失效 / 验证码 / 账号异常 / 403 / 401
  COOLDOWN 限流：429 / "操作频繁" → 冷却后再来
  WARN     服务端抖动：5xx
  NOTICE   **业务**错误：301/306-312、二维码过期 → 不是风控，别自己吓自己
  OK       正常（success / statusCode 300）

用法示例：
  python3 scripts/risk_guard.py --selftest
  curl -s -b cookies.txt 'https://mobilelearn.chaoxing.com/pptSign/stuSignajax?...' -o resp.txt
  python3 scripts/risk_guard.py --check resp.txt --status 200
"""
import argparse, json, os, sys, time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from stealth_session import (RiskGuard, RateGovernor, StealthSession, redact,
                             AUDIT_PATH, RISK_PATH, RISK_SIGNALS)

CORPUS = [
    ("登录失效（通道 C 文案）", 200, "请先登录再进行签到", "HALT"),
    ("登录失效（英文）", 200, '{"error":"login required"}', "HALT"),
    ("未登录", 200, "未登录或登录已过期", "HALT"),
    ("验证码/人机", 200, "请完成安全验证：拖动滑块", "HALT"),
    ("账号异常", 200, '{"msg":"账号异常，请稍后再试"}', "HALT"),
    ("账号被风控", 200, '{"msg":"触发 riskControl 规则"}', "HALT"),
    ("HTTP 401", 401, "", "HALT"),
    ("HTTP 403（WAF）", 403, "Access Denied", "HALT"),
    ("HTTP 429", 429, "too many requests", "COOLDOWN"),
    ("限流文案", 200, "操作频繁，请稍后再试", "COOLDOWN"),
    ("请求过快", 200, '{"msg":"请求过快，请稍后再试"}', "COOLDOWN"),
    ("HTTP 503", 503, "service unavailable", "WARN"),
    ("业务码 308（signId 不存在）", 200, '{"msg":"signId  not exists","status":false,"statusCode":308}', "NOTICE"),
    ("二维码过期 307", 200, '{"msg":"二维码时间过期","statusCode":307}', "NOTICE"),
    ("enc 验证错误 306", 200, '{"msg":"enc验证错误","statusCode":306}', "NOTICE"),
    ("成功文本", 200, "success", "OK"),
    ("成功 JSON 300", 200, '{"statusCode":300,"msg":"签到成功"}', "OK"),
    ("普通页面（不该误判）", 200, "<html><body>学习通首页</body></html>", "OK"),
]


def selftest(verbose=True):
    bad = 0
    for name, status, body, want in CORPUS:
        g = RiskGuard(path=os.path.join("/tmp", ".cx_risk_test.json"))
        got = g.classify(status, body)["level"]
        ok = got == want
        bad += 0 if ok else 1
        if verbose:
            print("  %s %-28s 期望 %-8s 实际 %-8s %s" % ("PASS" if ok else "FAIL", name, want, got,
                                                       "" if ok else "| " + g.classify(status, body)["reason"][:50]))
    print("判级回归: %d/%d 通过" % (len(CORPUS) - bad, len(CORPUS)))
    return bad


def check_file(path, status=200):
    try:
        body = open(path, encoding="utf-8", errors="replace").read()
    except Exception as e:
        sys.exit("读不到 %s: %s" % (path, e))
    g = RiskGuard()
    v = g.classify(status, body)
    print("HTTP %s  判级 %s  |  %s" % (status, v["level"], v["reason"]))
    print("原文片段:", (body or "")[:300].replace("\n", " "))
    return v


def decide(url, body, status=200, dry=True):
    g = RiskGuard(path=os.path.join("/tmp", ".cx_risk_dry.json")) if dry else RiskGuard()
    v = g.classify(status, body)
    action = g.observe(v, url)
    print("url    :", redact(url))
    print("level  :", v["level"], "|", v["reason"])
    print("action :", action, "（该响应对应的处置）")
    print("state  : soft=%d hard=%d halted=%s cooldown=%s" %
          (g.state["soft"], g.state["hard"], g.state["halted"],
           time.strftime("%H:%M:%S", time.localtime(g.state["cooldown_until"])) if g.state["cooldown_until"] > time.time() else "-"))
    return action


def monitor(poll=3.0, follow=True):
    print("盯审计 %s（Ctrl-C 退出）" % AUDIT_PATH)
    pos = 0
    if os.path.exists(AUDIT_PATH):
        pos = os.path.getsize(AUDIT_PATH)
    while True:
        if os.path.exists(AUDIT_PATH):
            size = os.path.getsize(AUDIT_PATH)
            if size < pos:      # 轮转
                pos = 0
            if size > pos:
                with open(AUDIT_PATH, encoding="utf-8") as f:
                    f.seek(pos)
                    for line in f:
                        try:
                            d = json.loads(line)
                        except Exception:
                            continue
                        flag = d.get("verdict")
                        mark = "  " if flag in ("OK", "NOTICE") else ("!!" if flag in ("HALT", "COOLDOWN") else " ?")
                        print("%s %s %-4s %-3s %-8s %s | %s" % (mark, d.get("t", "")[11:], d.get("m"), d.get("code"),
                                                               flag, str(d.get("url"))[:60], str(d.get("why"))[:40]))
                    pos = f.tell()
        if not follow:
            return
        time.sleep(poll)


def main():
    ap = argparse.ArgumentParser(description="风控层 CLI：判级回归 / 响应判级 / 审计监视 / 状态管理")
    ap.add_argument("--selftest", action="store_true", help="跑判级回归（13 条人工语料）")
    ap.add_argument("--check", metavar="FILE", help="对一个保存下来的响应体判级")
    ap.add_argument("--status", type=int, default=200)
    ap.add_argument("--decide", metavar="URL", help="模拟：这个响应会发生什么（不落状态）")
    ap.add_argument("--body", default="", help="配合 --decide 的响应体")
    ap.add_argument("--monitor", action="store_true", help="实时盯审计日志")
    ap.add_argument("--poll", type=float, default=3.0)
    ap.add_argument("--state", action="store_true")
    ap.add_argument("--reset", action="store_true")
    a = ap.parse_args()

    if a.selftest:
        sys.exit(0 if selftest() == 0 else 1)
    if a.check:
        check_file(a.check, a.status)
        return
    if a.decide:
        decide(a.decide, a.body, a.status)
        return
    if a.monitor:
        monitor(a.poll)
        return
    if a.state:
        g = RiskGuard()
        print(json.dumps({k: v for k, v in g.state.items() if k != "events"}, ensure_ascii=False, indent=2))
        print("最近事件:")
        for e in g.state.get("events", [])[-8:]:
            print("  %s %-8s %s" % (time.strftime("%H:%M:%S", time.localtime(e["t"])), e["level"], e["reason"][:70]))
        r = RateGovernor()
        print("限速: 近 1h 写 %d/%d，24h 写 %d/%d，最小间隔 %.0fs，静默 %s" %
              (len([x for x in r.writes if x > time.time() - 3600]), r.per_hour, len(r.writes), r.per_day,
               r.min_interval, r.quiet))
        return
    if a.reset:
        RiskGuard().reset()
        r = RateGovernor()
        r.cooldown_until = 0
        r.save()
        print("已清空停机/冷却（strikes 归零）")
        return
    ap.print_help()


if __name__ == "__main__":
    main()
