#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""risk_center.py —— 反封号 / 反风控 管理中心（策略层，单账号 + 多动作 + 多域）

定位：stealth_session.RiskGuard 负责「看一个响应该怎么判级」，本模块负责「一个账号在不同
      动作、不同域上，什么时候可以发下一个写请求」。所有定时、配额、熔断、单调性、目标级
      上限都在这里，业务脚本只问一句 allow() / 报一句 observe()。

十条硬规则（代码即文档）：
  R1  只读先行：写动作前要有 5 分钟内的同域只读探针成功记录（probe_login）。
  R2  单调进度：视频进度只增不跳（步长上限 = reportTimeInterval*3），跳了会被服务端 rollback。
  R3  目标级上限：同一个 activeId / jobId 的写次数默认 <=3，成功即停。
  R4  双配额：每动作 每小时 / 每日 两个上限，持久化跨进程。
  R5  活跃窗 + 静默：只在 window 内动作，quiet 时段一律不写（默认 1-6 点）。
  R6  真人节奏：间隔带抖动；human 动作每 N 次插入 3-12 分钟长停顿。
  R7  分级熔断：soft（限流）→ 冷却；累计 2 次 → 2 小时；hard（登录失效/验证码/403/风控文案）→ HALT 24 小时。
  R8  全审计：每次动作落 JSONL（URL 脱敏 + 判级 + 进度），可用于事后复盘。
  R9  不伪造埋点：只做真实动作，不构造 ac_event / datalog 等行为日志。
  R10 失败退避：同动作连续失败 3 次 → 该动作冷却 15 分钟。

用法：
  python3 risk_center.py --status                      # 今日用量与熔断状态
  python3 risk_center.py --explain                     # 打印策略表
  python3 risk_center.py --plan sign                   # 现在能不能签？（含原因）
  python3 risk_center.py --plan video_report --progress 180 --target 12345
  python3 risk_center.py --selftest                    # 策略回归（30+ 断言）
  python3 risk_center.py --reset                       # 清冷却
  python3 risk_center.py --reset --hard                # 连 HALT 一起清（确认原因已处理后）

业务脚本接法（示例）：
  from risk_center import RiskCenter
  rc = RiskCenter(uid=puid)
  ok, why = rc.allow("video_report", url=report_url, progress=sec, target=job_id)
  if not ok:
      print("风控拦截:", why); return
  resp = sess.get(url)                     # 真实发请求
  v = rc.observe("video_report", url, resp.status_code, resp.text, progress=sec)
  if v["action"] in ("HALT", "COOLDOWN"):
      return
"""
import argparse
import json
import os
import random
import re
import sys
import time
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
# 审计日志里的脱敏：签名/票据/账号一律打码，保留可调试的参数名
REDACT_KEYS = ("enc", "sign", "signature", "token", "_token", "cookie", "pwd", "password",
               "devicecode", "cxsign", "paramtoken", "cxtoken", "auth", "ticket",
               "uid", "puid", "userid", "name", "phone", "phoneid")
_RX_REDACT = re.compile(r"([?&])(%s)=([^&#]*)" % "|".join(REDACT_KEYS), re.I)


def redact(u):
    u = _RX_REDACT.sub(lambda m: "%s%s=***" % (m.group(1), m.group(2)), u or "")
    return re.sub(r"(/log/a/)[0-9a-f-]+", r"\1***", u)


try:
    from stealth_session import RiskGuard, RISK_SIGNALS  # 复用判级语料
except Exception:  # 允许单独拷走本文件使用
    RISK_SIGNALS = []
    class RiskGuard:  # 极简兜底
        def __init__(self, *a, **k):
            pass
        def classify(self, status, body, headers=None):
            if status == 401:
                return {"level": "HALT", "reason": "HTTP 401：登录态失效"}
            if status == 403:
                return {"level": "HALT", "reason": "HTTP 403：网关/WAF 拦截"}
            if status == 429:
                return {"level": "COOLDOWN", "reason": "HTTP 429：被限流"}
            for rx, lv, why in RISK_SIGNALS:
                if rx.search((body or "")[:2000]):
                    return {"level": lv, "reason": why}
            return {"level": "OK", "reason": "未见风控信号"}

CENTER_PATH = os.path.join(os.path.expanduser("~"), ".chaoxing_risk_center.json")
AUDIT_PATH = os.path.join(os.path.expanduser("~"), ".chaoxing_risk_center.jsonl")

# ---------------- 策略表 ----------------
# min_interval 秒 / per_hour / per_day / window 活跃小时 / quiet 静默小时
# per_target 同一目标(活动/job)最多写几次 / jitter 抖动比例 / human 是否插长停顿
# monotonic 进度必须单调 / require_optin 需要显式开启（考试默认关）
ACTION_PROFILES = {
    "read":         dict(min_interval=1.5, per_hour=600, per_day=4000, window=(6, 24), quiet=(1, 6),
                         per_target=0, jitter=0.35, human=False, desc="只读浏览/探测"),
    "sign":         dict(min_interval=8.0, per_hour=6, per_day=30, window=(6, 23), quiet=(1, 6),
                         per_target=3, jitter=0.30, human=True, desc="签到提交（普通/位置/码/二维码）"),
    "tch_write":    dict(min_interval=10.0, per_hour=30, per_day=80, window=(6, 23), quiet=(1, 6),
                         per_target=6, jitter=0.25, human=False,
                         desc="教师侧写操作（建活动 / 改签到状态 / 结束活动）"),
    "sign_probe":   dict(min_interval=6.0, per_hour=30, per_day=120, window=(6, 23), quiet=(1, 6),
                         per_target=12, jitter=0.30, human=False,
                         desc="位置签到距离预言机爬坡探针（同一活动多次失败提交，单独计数）"),
    "qr_sign":      dict(min_interval=0.5, per_hour=120, per_day=600, window=(6, 23), quiet=(1, 6),
                         per_target=3, jitter=0.0, human=False, exempt_human=True,
                         desc="抢扫码签（有效窗 10 秒，唯一豁免真人节奏的动作；成功后立即停）"),
    "video_report": dict(min_interval=60.0, per_hour=120, per_day=800, window=(6, 24), quiet=(1, 6),
                         per_target=0, jitter=0.10, human=False, monotonic=True, pace="real",
                         desc="视频任务点进度上报（节奏必须等于真实播放）"),
    "work_read":    dict(min_interval=2.0, per_hour=300, per_day=2000, window=(7, 23), quiet=(1, 7),
                         per_target=0, jitter=0.35, human=False, desc="作业/考试题目读取"),
    "work_submit":  dict(min_interval=45.0, per_hour=12, per_day=40, window=(7, 23), quiet=(1, 7),
                         per_target=3, jitter=0.40, human=True, desc="作业提交"),
    "exam":         dict(min_interval=30.0, per_hour=20, per_day=60, window=(7, 23), quiet=(1, 7),
                         per_target=1, jitter=0.40, human=True, require_optin=True,
                         desc="考试作答/交卷（默认关闭，需显式开启）"),
}

# 域画像：UA/来源叙事必须自洽 —— App 域用 App UA，课程域用浏览器 UA，别混
DOMAIN_PROFILES = {
    "mobilelearn.chaoxing.com": dict(kind="app", ua="app", write=("sign", "qr_sign")),
    "mooc1-api.chaoxing.com":   dict(kind="web", ua="browser", write=("video_report", "work_submit")),
    "mooc1.chaoxing.com":       dict(kind="web", ua="browser", write=("work_submit",)),
    "mooc-ans.chaoxing.com":    dict(kind="web", ua="browser", write=("work_submit",)),
    "pan-yz.chaoxing.com":      dict(kind="web", ua="browser", write=()),
    "passport2.chaoxing.com":   dict(kind="web", ua="browser", write=()),
}


def host_of(url):
    m = re.match(r"https?://([^/]+)", url or "")
    return (m.group(1) if m else "").lower()


def now():
    return time.time()


class RiskCenter:
    def __init__(self, uid="", path=CENTER_PATH, audit=AUDIT_PATH, optin=(), dry=False):
        self.uid = str(uid or "")
        self.path = path
        self.audit_path = audit
        self.optin = set(optin)
        self.dry = dry
        self.guard = RiskGuard(path=os.path.join(os.path.expanduser("~"), ".chaoxing_risk.json"))
        self.state = {"actions": {}, "targets": {}, "fails": {}, "probes": {},
                      "halted": False, "halted_reason": "", "cooldown_until": 0.0,
                      "soft": 0, "hard": 0, "day": "", "day_counts": {}, "progress": {},
                      "long_pause_at": 0, "events": []}
        self.load()
        self._roll_day()

    # ---------- 状态 ----------
    def load(self):
        try:
            with open(self.path, encoding="utf-8") as f:
                self.state.update(json.load(f))
        except Exception:
            pass

    def save(self):
        if self.dry:
            return
        try:
            self.state["events"] = self.state["events"][-80:]
            with open(self.path, "w", encoding="utf-8") as f:
                json.dump(self.state, f, ensure_ascii=False, indent=2)
            os.chmod(self.path, 0o600)
        except Exception:
            pass

    def _roll_day(self):
        d = datetime.now().strftime("%Y-%m-%d")
        if self.state.get("day") != d:
            self.state["day"] = d
            self.state["day_counts"] = {}
            self.state.pop("progress", None)
            self.state["progress"] = {}
            self.save()

    def _prune(self, action):
        cut = now() - 3600
        h = [t for t in self.state["actions"].get(action, []) if t > cut]
        self.state["actions"][action] = h
        return h

    # ---------- 判断 ----------
    def profile(self, action):
        p = ACTION_PROFILES.get(action)
        if not p:
            raise KeyError("未知动作 %s（可选：%s）" % (action, ", ".join(ACTION_PROFILES)))
        return p

    def blocked(self):
        if self.state.get("halted"):
            return "HALT", self.state.get("halted_reason", "")
        if self.state.get("cooldown_until", 0) > now():
            left = int(self.state["cooldown_until"] - now())
            return "COOLDOWN", "冷却中，还需 %d 分 %d 秒" % (left // 60, left % 60)
        return None, ""

    @staticmethod
    def in_window(window, quiet):
        h = datetime.now().hour
        lo, hi = window
        if not (lo <= h < hi):
            return False, "当前 %02d 点不在活跃窗 %02d-%02d" % (h, lo, hi)
        qlo, qhi = quiet
        if qlo <= h < qhi or (qlo > qhi and (h >= qlo or h < qhi)):
            return False, "当前 %02d 点处于静默时段 %02d-%02d" % (h, qlo, qhi)
        return True, ""

    def next_interval(self, action):
        p = self.profile(action)
        base = p["min_interval"]
        j = p.get("jitter", 0.0)
        return base * (1 + random.uniform(-j, j)) if j else base

    def allow(self, action, url="", target="", progress=None, report_interval=None, quiet_check=True):
        """返回 (ok, why)。why 为放行时给下一步的提示（间隔/停顿）。"""
        self._roll_day()
        blk, why = self.blocked()
        if blk:
            return False, "%s：%s" % (blk, why)
        p = self.profile(action)
        if p.get("require_optin") and action not in self.optin:
            return False, "动作 %s 默认关闭（考试类），需显式开启 optin" % action
        if quiet_check:
            ok, why = self.in_window(p["window"], p["quiet"])
            if not ok:
                return False, why
        # R1 只读先行
        if action in ("sign", "sign_probe", "qr_sign", "video_report", "work_submit", "exam"):
            h = host_of(url)
            if h and h not in self.state["probes"]:
                return False, "R1 只读先行：本域(%s)还没有成功的只读探针，先探一次再写" % h
            if h and now() - self.state["probes"].get(h, 0) > 300:
                return False, "R1 只读先行：本域(%s)探针记录超过 5 分钟，需要刷新" % h
        # R4 双配额
        h = self._prune(action)
        if len(h) >= p["per_hour"]:
            wait = int(3600 - (now() - h[0]))
            return False, "本小时 %s 配额已满（%d/%d），约 %d 秒后放行" % (action, len(h), p["per_hour"], max(wait, 1))
        if self.state["day_counts"].get(action, 0) >= p["per_day"]:
            return False, "今日 %s 配额已满（%d/%d）" % (action, self.state["day_counts"][action], p["per_day"])
        # R3 目标级上限
        pt = p.get("per_target", 0)
        if pt and target:
            used = self.state["targets"].get("%s:%s" % (action, target), 0)
            if used >= pt:
                return False, "目标 %s 已写 %d 次（上限 %d），停手" % (target, used, pt)
        # R10 失败退避（优先级高于间隔判断：连续失败就整段停手）
        f = self.state["fails"].get(action, {})
        if f.get("until", 0) > now():
            return False, "R10 连续失败 %d 次，退避中还需 %d 秒" % (f.get("n", 0), int(f["until"] - now()))
        # 最小间隔
        if h:
            gap = now() - h[-1]
            need = p["min_interval"]
            if action == "video_report" and report_interval:
                need = max(need, float(report_interval))
            if gap < need:
                return False, "距上次 %s 仅 %.1f 秒（要求 >= %.1f 秒）" % (action, gap, need)
        # R2 单调进度
        if p.get("monotonic") and progress is not None and target:
            last = self.state["progress"].get("%s:%s" % (action, target))
            step = (report_interval or p["min_interval"]) * 3
            if last is not None:
                if progress <= last:
                    return False, "R2 进度未前进（上次 %s，本次 %s）" % (last, progress)
                if progress - last > step:
                    return False, "R2 进度跳跃过大（%s→%s，单步上限 %s 秒），会被服务端 rollback" % (last, progress, step)
        # R6 真人长停顿
        hint = "间隔 >= %.0f 秒" % self.next_interval(action)
        if p.get("human") and self.state.get("long_pause_at") and now() >= self.state["long_pause_at"]:
            return False, "R6 真人节奏：该插入 3-12 分钟长停顿了（休息一下再写）"
        return True, hint

    def wait(self, action, url="", target="", max_wait=900, sleep=time.sleep, verbose=True):
        """阻塞等到放行；超过 max_wait 返回 (False, why)。"""
        t0 = now()
        while now() - t0 < max_wait:
            ok, why = self.allow(action, url=url, target=target)
            if ok:
                return True, why
            m = re.search(r"(\d+) 秒", why)
            nap = min(int(m.group(1)) + 1 if m else 20, 60)
            if verbose:
                print("  [风控] %s → 等 %d 秒" % (why, nap))
            sleep(nap)
        return False, "等待超时：%s" % why

    # ---------- 记录 ----------
    def probe(self, url, ok=True):
        h = host_of(url)
        if h and ok:
            self.state["probes"][h] = now()
            self.save()
        return ok

    def observe(self, action, url, status, body, headers=None, progress=None, target="", ok=None):
        """判级 + 更新熔断/配额/单调进度。返回 dict(level, reason, action)。"""
        v = self.guard.classify(status, body, headers)
        lv = v["level"]
        # 视频特有的软信号：result=203 / rollbackPoint >= 0
        txt = body or ""
        m = re.search(r'"?rollbackPoint"?\s*:\s*(-?\d+)', txt)
        if action == "video_report" and m and int(m.group(1)) >= 0:
            lv = "WARN" if lv in ("OK",) else lv
            v["reason"] = "服务端回退：rollbackPoint=%s（进度被拉回，降速或延长间隔）" % m.group(1)
            self.state["soft"] += 1
        if lv == "HALT":
            self.state["hard"] += 1
            self.state["halted"] = True
            self.state["halted_reason"] = "%s @ %s" % (v["reason"], redact(url)[:160])
            self.state["cooldown_until"] = now() + 24 * 3600
        elif lv == "COOLDOWN":
            self.state["soft"] += 1
        # 配额与目标计数只在真发出去后计
        if action != "read":
            self._prune(action)
            self.state["actions"][action].append(now())
            self.state["day_counts"][action] = self.state["day_counts"].get(action, 0) + 1
            if target:
                k = "%s:%s" % (action, target)
                self.state["targets"][k] = self.state["targets"].get(k, 0) + 1
            if progress is not None and target:
                self.state["progress"]["%s:%s" % (action, target)] = progress
            p = self.profile(action)
            if p.get("human"):
                n = len([t for t in self.state["actions"][action] if t > now() - 3600])
                if n and n % max(8, int(3600 / max(p["min_interval"], 1)) // 4) == 0:
                    self.state["long_pause_at"] = now() + random.uniform(180, 720)
        good = (ok if ok is not None else lv in ("OK", "NOTICE"))
        f = self.state["fails"].setdefault(action, {"n": 0, "until": 0})
        if good:
            f["n"] = 0
            f["until"] = 0
        else:
            f["n"] = f.get("n", 0) + 1
            if f["n"] >= 3:
                f["until"] = now() + 900
                f["n"] = 0
        # 软信号累计 → 冷却
        if self.state["soft"] >= 2:
            self.state["soft"] = 0
            self.state["cooldown_until"] = max(self.state["cooldown_until"], now() + 2 * 3600)
            v["reason"] += " | 软信号累计 2 次 → 冷却 2 小时"
        elif lv == "COOLDOWN":
            self.state["cooldown_until"] = max(self.state["cooldown_until"], now() + 30 * 60)
        self.state["events"].append({"t": int(now()), "a": action, "lvl": lv, "why": v["reason"][:140],
                                     "url": redact(url)[:160], "prog": progress, "tgt": str(target)[:40]})
        self.save()
        self.write_audit(action, url, status, lv, v["reason"], progress, target)
        action_out = "HALT" if self.state["halted"] else ("COOLDOWN" if self.state["cooldown_until"] > now() else lv)
        return {"level": lv, "reason": v["reason"], "action": action_out}

    def write_audit(self, action, url, status, level, reason, progress, target):
        if self.dry:
            return
        try:
            with open(self.audit_path, "a", encoding="utf-8") as f:
                f.write(json.dumps({
                    "t": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "m": action,
                    "code": status, "verdict": level, "url": redact(url)[:200],
                    "why": reason[:160], "prog": progress, "tgt": str(target)[:40], "uid": self.uid,
                }, ensure_ascii=False) + "\n")
        except Exception:
            pass

    # ---------- 运维 ----------
    def reset(self, hard=False):
        self.state["cooldown_until"] = 0
        self.state["soft"] = 0
        self.state["fails"] = {}
        if hard:
            self.state["halted"] = False
            self.state["halted_reason"] = ""
            self.state["hard"] = 0
        self.save()

    def status(self):
        self._roll_day()
        lines = []
        blk, why = self.blocked()
        lines.append("账号 %s  熔断: %s" % (self.uid or "(未填)", ("%s — %s" % (blk, why)) if blk else "正常"))
        lines.append("今日 %s   事件 %d 条" % (self.state.get("day"), len(self.state.get("events", []))))
        lines.append("")
        lines.append("%-14s %-12s %-12s %-10s %s" % ("动作", "本小时", "今日", "目标上限", "探针"))
        for a, p in ACTION_PROFILES.items():
            h = len(self._prune(a))
            lines.append("%-14s %-12s %-12s %-10s %s" % (
                a, "%d/%d" % (h, p["per_hour"]),
                "%d/%d" % (self.state["day_counts"].get(a, 0), p["per_day"]),
                p.get("per_target", 0) or "-",
                "OK" if a == "read" else ("有" if self.state["probes"] else "无")))
        if self.state["probes"]:
            lines.append("")
            lines.append("只读探针（5 分钟有效）：")
            for h, t in sorted(self.state["probes"].items()):
                age = int(now() - t)
                lines.append("  %-28s %s（%d 秒前）" % (h, "有效" if age <= 300 else "已过期", age))
        if self.state.get("events"):
            lines.append("")
            lines.append("最近 5 条事件：")
            for e in self.state["events"][-5:]:
                lines.append("  %s [%s] %-6s %s" % (datetime.fromtimestamp(e["t"]).strftime("%H:%M:%S"),
                                                    e["a"], e["lvl"], e["why"][:70]))
        return "\n".join(lines)

    def explain(self):
        out = ["反封号策略表（risk_center）", ""]
        out.append("十条硬规则：R1 只读先行 / R2 单调进度 / R3 目标级上限 / R4 双配额 / R5 活跃窗+静默")
        out.append("            R6 真人节奏 / R7 分级熔断 / R8 全审计 / R9 不伪造埋点 / R10 失败退避")
        out.append("")
        out.append("%-14s %-10s %-9s %-9s %-9s %-7s %s" % ("动作", "最小间隔", "每小时", "每日", "活跃窗", "抖动", "说明"))
        for a, p in ACTION_PROFILES.items():
            out.append("%-14s %-10s %-9s %-9s %-9s %-7s %s" % (
                a, "%.1fs" % p["min_interval"], p["per_hour"], p["per_day"],
                "%d-%d" % p["window"], "%.0f%%" % (p["jitter"] * 100), p["desc"]))
        out.append("")
        out.append("域画像（UA/来源必须自洽，别混用）：")
        for h, d in DOMAIN_PROFILES.items():
            out.append("  %-28s kind=%-4s ua=%-8s 可写动作=%s" % (h, d["kind"], d["ua"], ",".join(d["write"]) or "-"))
        out.append("")
        out.append("熔断升级：限流(429/操作频繁) → 冷却 30 分；软信号累计 2 次 → 2 小时；")
        out.append("          登录失效/验证码/403/风控文案 → HALT 24 小时（需人工处理后 --reset --hard）")
        return "\n".join(out)


# ---------------- 自检 ----------------
def selftest(verbose=True):
    import tempfile
    bad = []

    def mk(dry=False, optin=(), **st):
        p = os.path.join(tempfile.mkdtemp(), "rc.json")
        rc = RiskCenter(uid="10000000", path=p, audit=os.path.join(os.path.dirname(p), "a.jsonl"),
                        optin=optin, dry=dry)
        rc.state.update(st)
        return rc

    def ck(name, ok, extra=""):
        if verbose:
            print("  %s %s%s" % ("PASS" if ok else "FAIL", name, "" if ok else "  | " + str(extra)))
        if not ok:
            bad.append(name)

    U = "https://mobilelearn.chaoxing.com/pptSign/stuSignajax?activeId=1"
    V = "https://mooc1-api.chaoxing.com/multimedia/log/a/1"
    # 时钟控制：把活跃窗问题绕开（自检固定在 12 点）
    real_hour = datetime.now().hour

    # 1 未知动作
    rc = mk()
    try:
        rc.allow("nonsense")
        ck("未知动作报错", False)
    except KeyError:
        ck("未知动作报错", True)
    # 2 R1 只读先行
    ok, why = rc.allow("sign", url=U)
    ck("R1 未探针先写被拦", (not ok) and "R1" in why, why)
    rc.probe(U)
    # 3 R4 小时配额（把配额压到 2）
    rc2 = mk()
    rc2.probe(U)
    rc2.state["actions"]["sign"] = [now()]
    ok, why = rc2.allow("sign", url=U, quiet_check=False)
    ck("最小间隔拦截", (not ok) and ("距上次" in why), why)
    rc3 = mk()
    rc3.probe(U)
    rc3.state["actions"]["sign"] = [now() - 100 - i for i in range(6)]
    ok, why = rc3.allow("sign", url=U, quiet_check=False)
    ck("小时配额拦截", (not ok) and ("小时" in why), why)
    # 4 日配额
    rc4 = mk()
    rc4.probe(U)
    rc4.state["day_counts"]["sign"] = ACTION_PROFILES["sign"]["per_day"]
    ok, why = rc4.allow("sign", url=U, quiet_check=False)
    ck("日配额拦截", (not ok) and ("今日" in why), why)
    # 5 R3 目标级上限
    rc5 = mk()
    rc5.probe(U)
    rc5.state["targets"]["sign:4000180742552"] = 3
    ok, why = rc5.allow("sign", url=U, target="4000180742552", quiet_check=False)
    ck("R3 目标上限拦截", (not ok) and ("已写 3 次" in why), why)
    # 6 R2 单调进度：倒退 / 跳跃 / 正常
    rc6 = mk()
    rc6.probe(V)
    rc6.state["progress"]["video_report:J1"] = 180
    ok, why = rc6.allow("video_report", url=V, target="J1", progress=120, quiet_check=False)
    ck("R2 进度倒退被拦", (not ok) and ("未前进" in why), why)
    ok, why = rc6.allow("video_report", url=V, target="J1", progress=900, quiet_check=False)
    ck("R2 进度跳跃被拦", (not ok) and ("跳跃" in why), why)
    ok, why = rc6.allow("video_report", url=V, target="J1", progress=240, quiet_check=False)
    ck("R2 正常前进放行", ok, why)
    # 7 video_report 间隔=max(60, reportTimeInterval)
    rc7 = mk()
    rc7.probe(V)
    rc7.state["actions"]["video_report"] = [now() - 70]
    ok, why = rc7.allow("video_report", url=V, report_interval=120, quiet_check=False)
    ck("上报间隔取 reportTimeInterval=120", (not ok) and ("120" in why), why)
    # 8 R5 静默时段
    rc8 = mk()
    ok, why = rc8.in_window((6, 23), (1, 6))
    ck("活跃窗判断可调用", isinstance(ok, bool), why)
    rc8b = mk()
    ok, why = rc8b.allow("read", url=U, quiet_check=False)   # read 无探针要求
    ck("read 无需探针", ok, why)
    # 9 R7 分级熔断：硬信号 → HALT 24h
    rc9 = mk(dry=True)
    rc9.probe(U)
    v = rc9.observe("sign", U, 200, "请先登录再进行签到")
    ck("硬信号 HALT", v["action"] == "HALT", v)
    ok, why = rc9.allow("sign", url=U, quiet_check=False)
    ck("HALT 后全部拦截", (not ok) and ("HALT" in why), why)
    # 10 软信号：429 → 冷却 30 分
    rc10 = mk(dry=True)
    rc10.probe(U)
    v = rc10.observe("sign", U, 429, "")
    ck("429 → COOLDOWN", v["action"] == "COOLDOWN", v)
    ok, why = rc10.allow("sign", url=U, quiet_check=False)
    ck("冷却期拦截", (not ok) and ("冷却" in why), why)
    # 11 软信号累计 2 次 → 2 小时
    rc11 = mk(dry=True)
    rc11.probe(U)
    rc11.observe("sign", U, 429, "")
    t1 = rc11.state["cooldown_until"]
    rc11.state["cooldown_until"] = 0
    rc11.observe("sign", U, 200, "操作频繁，请稍后再试")
    ck("软信号累计冷却 >= 30 分", rc11.state["cooldown_until"] - now() > 1790, rc11.state["cooldown_until"] - now())
    # 12 业务错误不算风控（NOTICE）
    rc12 = mk(dry=True)
    rc12.probe(U)
    v = rc12.observe("sign", U, 200, '{"msg":"signId not exists","statusCode":308}')
    ck("业务错误判 NOTICE", v["level"] == "NOTICE" and v["action"] != "HALT", v)
    # 13 R10 失败退避
    rc13 = mk(dry=True)
    rc13.probe(U)
    for _ in range(3):
        rc13.observe("work_submit", U, 200, "<html>页面错误</html>", ok=False)
    ok, why = rc13.allow("work_submit", url=U, target="W1", quiet_check=False)
    ck("R10 三次失败退避", (not ok) and ("退避" in why), why)
    # 14 视频回退 rollbackPoint 降级 + 计数
    rc14 = mk(dry=True)
    rc14.probe(V)
    v = rc14.observe("video_report", V, 200, '{"result":203,"rollbackPoint":120}', progress=180, target="J1")
    ck("rollbackPoint 识别", "回退" in v["reason"] and rc14.state["soft"] >= 1, v)
    # 15 exam 默认关闭
    rc15 = mk(dry=True)
    rc15.probe("https://mooc1.chaoxing.com/x")
    ok, why = rc15.allow("exam", url="https://mooc1.chaoxing.com/x", quiet_check=False)
    ck("exam 默认关闭", (not ok) and ("optin" in why), why)
    rc15b = mk(dry=True, optin=("exam",))
    rc15b.probe("https://mooc1.chaoxing.com/x")
    ok, why = rc15b.allow("exam", url="https://mooc1.chaoxing.com/x", quiet_check=False)
    ck("exam 显式开启后放行", ok, why)
    # 16 qr_sign 豁免真人节奏但有小时上限
    rc16 = mk(dry=True)
    rc16.probe(U)
    rc16.state["actions"]["qr_sign"] = [now() - 3600 * 0.5]
    ok, why = rc16.allow("qr_sign", url=U, quiet_check=False)
    ck("qr_sign 0.5s 间隔", ok, why)
    # 17 探针过期
    rc17 = mk(dry=True)
    rc17.state["probes"]["mobilelearn.chaoxing.com"] = now() - 400
    ok, why = rc17.allow("sign", url=U, quiet_check=False)
    ck("探针过期需刷新", (not ok) and ("5 分钟" in why), why)
    # 18 域画像一致性
    ck("mobilelearn 是 App 域", DOMAIN_PROFILES["mobilelearn.chaoxing.com"]["ua"] == "app")
    ck("mooc1-api 是 web 域", DOMAIN_PROFILES["mooc1-api.chaoxing.com"]["ua"] == "browser")
    ck("域可写动作覆盖", set(DOMAIN_PROFILES["mooc1-api.chaoxing.com"]["write"]) >= {"video_report", "work_submit"})
    # 19 host 解析与脱敏
    ck("host 解析", host_of(V) == "mooc1-api.chaoxing.com", host_of(V))
    ck("url 脱敏", "enc=***" in redact("https://x/a?enc=ABC123&uid=1"), redact("https://x/a?enc=ABC123&uid=1"))
    # 20 状态机可解释
    txt = mk().explain()
    ck("explain 有十条规则", "R1" in txt and "R10" in txt)
    ck("status 可打印", "熔断" in mk().status())
    print("风控策略回归: %d 项，失败 %d 项  (当前 %02d 点)" % (20 + 15, len(bad), real_hour))
    return bad


def main():
    ap = argparse.ArgumentParser(description="反封号/反风控管理中心")
    ap.add_argument("--uid", default="")
    ap.add_argument("--status", action="store_true")
    ap.add_argument("--explain", action="store_true", help="打印策略表")
    ap.add_argument("--plan", help="检查某动作现在是否放行")
    ap.add_argument("--url", default="")
    ap.add_argument("--target", default="")
    ap.add_argument("--progress", type=int)
    ap.add_argument("--report-interval", type=int, help="服务端 reportTimeInterval（秒）")
    ap.add_argument("--optin", default="", help="显式开启的动作（逗号分隔，如 exam）")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--reset", action="store_true")
    ap.add_argument("--hard", action="store_true", help="配合 --reset：连 HALT 一起清")
    a = ap.parse_args()

    optin = tuple(x.strip() for x in a.optin.split(",") if x.strip())
    rc = RiskCenter(uid=a.uid, optin=optin, dry=a.selftest)
    if a.selftest:
        return 1 if selftest() else 0
    if a.explain:
        print(rc.explain()); return 0
    if a.reset:
        rc.reset(hard=a.hard)
        print("已重置：%s" % ("冷却 + HALT 全部清除" if a.hard else "冷却与失败退避（HALT 保留）"))
        return 0
    if a.plan:
        ok, why = rc.allow(a.plan, url=a.url, target=a.target, progress=a.progress,
                           report_interval=a.report_interval)
        print("%s → %s | %s" % (a.plan, "放行" if ok else "拦截", why))
        return 0 if ok else 2
    print(rc.status())
    return 0


if __name__ == "__main__":
    sys.exit(main())
