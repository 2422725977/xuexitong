# -*- coding: utf-8 -*-
"""risk_integration_test.py —— 策略层与业务脚本的接线回归（离线，不打服务端）

验证四件事：
  1) stu_guard：只读 activelist 成功后自动登记本域探针（R1），随后写动作才放行；
  2) stu_guard：提交成功后计入配额与目标计数；第 4 次同活动提交被 R3 拦住；
  3) stu_guard：响应出现「请先登录」→ HALT，之后所有写动作被拦；
  4) video_task：上报前 allow（含 R2 单调进度）→ 上报后 observe（rollbackPoint 识别）。
全程用假 session，不发真实请求。
"""
import json
import os
import sys
import tempfile
import types

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
TMP = tempfile.mkdtemp()

import risk_center as R
import stu_guard as SG
import video_task as VT

R.CENTER_PATH = os.path.join(TMP, "rc.json")
R.AUDIT_PATH = os.path.join(TMP, "rc.jsonl")

bad = []


def ck(name, ok, extra=""):
    print("  %s %s%s" % ("PASS" if ok else "FAIL", name, "" if ok else "  | " + str(extra)))
    if not ok:
        bad.append(name)


class Resp(object):
    def __init__(self, text, code=200):
        self.text, self.status_code = text, code

    def json(self):
        return json.loads(self.text)


class FakeSess(object):
    """按 URL 分派：activelist → 空列表；stuSignajax → 由 seq 决定。"""

    def __init__(self, seq=None):
        self.seq = list(seq or ["success"])
        self.calls = []
        self.headers = {}

    def get(self, url, **kw):
        self.calls.append(url)
        if "activelist" in url:
            return Resp('{"data":{"activeList":[]}}')
        return Resp(self.seq.pop(0))


def new_guard(seq=None, risk=True):
    g = SG.Guard("_uid=1; vc3=2", "10000000", "269282723", "159926750", log=lambda *a: None, risk=risk)
    g.rc = R.RiskCenter(uid="10000000", path=os.path.join(TMP, "rc_%d.json" % len(os.listdir(TMP))))
    g.rc.audit_path = os.path.join(TMP, "audit.jsonl")
    g.s = FakeSess(seq)
    return g


print("== 1) stu_guard R1 只读先行 / 写入计数 ==")
g = new_guard(["success", "success", "success", "success", "success"])
g.rc.wait = lambda *a, **k: (True, "")     # 测试里不让 wait 真睡
ok, why = g.rc.allow("sign", url=SG.MOBILE + "/pptSign/stuSignajax", target="A1")
ck("未探针时写动作被拦（R1 只读先行）", (not ok) and "R1" in why, why)
g.activelist()
ck("activelist 后登记探针", "mobilelearn.chaoxing.com" in g.rc.state["probes"])
b, d = g.submit("A1", action="sign_probe")
ck("提交成功文本", b == "success", b)
ck("写计数 +1", g.rc.state["day_counts"].get("sign_probe") == 1, g.rc.state["day_counts"])

print("== 2) R3 目标级上限（sign_probe 上限 12，sign 上限 3）==")
g2 = new_guard(["success"] * 20)
g2.activelist()
g2.rc.wait = lambda *a, **k: (True, "")
g2.rc.state["targets"]["sign:A2"] = 3          # 已经写过 3 次（sign 的 per_target=3）
g2.rc.state["actions"]["sign"] = [R.now() - 600]
b, d = g2.submit("A2", action="sign")
ck("第 4 次同活动 sign 被 R3 拦", str(b).startswith("RISK_BLOCKED") and "已写 3 次" in b, b)

print("== 3) 硬信号 HALT 后全拦 ==")
g3 = new_guard(["success", "请先登录再进行签到", "success"])
g3.rc.wait = lambda *a, **k: (True, "")
g3.activelist()
g3.submit("A3", action="sign_probe")                     # 正常一次
b, d = g3.submit("A3", action="sign_probe")             # 登录失效 → 本次入账并 HALT
ck("软/硬信号入账（HALT 生效于下一次）", g3.rc.state["halted"] is True, g3.rc.state["halted_reason"])
b, d = g3.submit("A3", action="sign_probe")             # 下一次被拦
ck("HALT 后返回风控拦截", str(b).startswith("RISK_BLOCKED"), b)
ok, why = g3.rc.allow("read", url=SG.MOBILE + "/x")
ck("HALT 连 read 都拦", (not ok) and "HALT" in why, why)
ck("审计文件已生成", os.path.exists(g3.rc.audit_path))

print("== 4) video_task allow/observe 接线 ==")
args = types.SimpleNamespace(
    uid="10000000", cookie="_uid=1; vc3=2", cookie_file=None, referer="https://mooc1-api.chaoxing.com/",
    ua_mode="browser", max_writes_per_hour=90, min_interval=5.0, quiet_hours="1-7", stealth=False,
    no_risk_center=False, report_interval=60, timeout=20, dry_run=False, audit="", raw_fmt=False,
    chunk=60, speed=1.0, pace="real", isdrag=False, clip_start=None, start=0, limit=2,
    report_url="https://mooc1-api.chaoxing.com/multimedia/log/a/deadbeef", object_id="obj1",
    job_id="J1", clazz_id="159926750", duration=180, rt=None, other_info=None, vbegin=None, vend=None,
    job_json=None, course_id="269282723", knowledge_id="k1", dump=None)
vt = VT.VideoTask(args, salt="abc!$_~12345")
vt.job = {"clazzid": "159926750", "objectid": "obj1", "jobid": "J1", "duration": 180,
          "reportUrl": "https://mooc1-api.chaoxing.com/multimedia/log/a/deadbeef", "rt": "0.0"}
vt.rc = R.RiskCenter(uid="10000000", path=os.path.join(TMP, "rc_video.json"))
vt.rc.audit_path = os.path.join(TMP, "video_audit.jsonl")
sess = FakeSess(['{"result":1}', '{"result":203,"rollbackPoint":120,"rollbackStatus":true}'])
vt.open = lambda: sess                    # 关键：同一个实例，序列才不会被重置
vt.rc.probe("https://mooc1-api.chaoxing.com/ananas/job?jobid=J1")
vt.rc.state["actions"]["video_report"] = []      # 测试里不等 60 秒最小间隔
v1 = vt.one_report(60, 0, None)
ck("上报 1 正常", v1.get("result") == 1 and vt.sent == 1, v1)
ck("进度已记账", vt.rc.state["progress"].get("video_report:J1") == 60, vt.rc.state["progress"])
vt.rc.state["actions"]["video_report"] = []
v2 = vt.one_report(120, 0, None)
ck("上报 2 触发 rollback 识别", "回退" in vt.rc.state["events"][-1]["why"] or vt.rollbacks >= 1,
   vt.rc.state["events"][-1])
ok, why = vt.rc.allow("video_report", url="https://mooc1-api.chaoxing.com/multimedia/log/a/deadbeef",
                      target="J1", progress=90, report_interval=60)
ck("R2 进度倒退被拦（接线后同样生效）", (not ok) and ("未前进" in why or "距上次" in why), why)

print("== 5) cx_pipeline StudentSide 接线 ==")
import cx_pipeline as CP
str_ = CP.StudentSide("_uid=1; vc3=2", "10000000", risk=True)
str_.rc = R.RiskCenter(uid="10000000", path=os.path.join(TMP, "rc_cp.json"))
str_.rc.audit_path = os.path.join(TMP, "cp_audit.jsonl")
str_.rc.wait = lambda *a, **k: (True, "")
str_.sess = FakeSess(["success"] * 4)
out1 = str_.submit("A9", "DEADBEEF", verbose=False, extra={"x": "1"})
ck("R1 自愈后放行并计入配额", str_.rc.state["day_counts"].get("sign_probe") == 1, str_.rc.state["day_counts"])
ck("只读探针已登记", "mobilelearn.chaoxing.com" in str_.rc.state["probes"], str_.rc.state["probes"])
str_.rc.state["targets"]["sign_probe:A9"] = 12
out2 = str_.submit("A9", "DEADBEEF", verbose=False, extra={"x": "1"})
ck("目标上限后返回 RISK_BLOCKED", isinstance(out2, dict) and out2.get("status") == "RISK_BLOCKED", out2)
str_.rc.state["halted"] = True
str_.rc.state["halted_reason"] = "test"
out3 = str_.submit("A9", "DEADBEEF", verbose=False, extra={"x": "1"})
ck("HALT 后 submit 直接拒绝", isinstance(out3, dict) and out3.get("status") == "RISK_BLOCKED", out3)

print("接线回归: 失败 %d 项" % len(bad))
sys.exit(1 if bad else 0)
