# -*- coding: utf-8 -*-
"""v12：
1) 试 otherId=1（可能才是"拍照签到"的 proper 类型，且必须同时带 ifPhoto=1）
2) 用活动所属学校 fid=328749 再打一轮（我们此前只测过 0/12/1022）
3) 对比 otherId=0+ifPhoto=1 与 otherId=1 的 preSign 页面差异
"""
import json, os, re, sys, time
from urllib.parse import quote
import requests
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cx_pipeline as C

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
UA_APP = ('Mozilla/5.0 (Linux; Android 13; SM-G975F Build/TQ3A.230901.001) AppleWebKit/537.36 (KHTML, like Gecko) '
          'Version/4.0 Chrome/120.0.0.0 Mobile Safari/537.36 (schild:b1c2d3e4f5a60718) (device:SM-G975F) '
          'Language/zh_CN com.ssreader.ChaoXingStudy/ChaoxingStudy_3_6_2_android_phone_20230101')
MOBILE = "https://mobilelearn.chaoxing.com"
COURSE, CLAZZ, TUID = "269282723", "159926750", "401537379"
OID = "943f4d2e543135b82012c341971e905c"
sck = open("ck.txt", encoding="utf-8").read().strip()
tck = open("ck_tch.txt", encoding="utf-8").read().strip()
S = requests.Session(); S.headers.update({"Cookie": sck, "User-Agent": UA_APP})

t = C.TeacherSide(tck, TUID, quiet_hours=None, max_writes_per_hour=60, min_interval=0.3, per_day=2000)

print("=== 1) otherId=1 变体 ===")
for kw in ({"other_id": "1", "if_photo": "1", "face": "0"},
           {"other_id": "1", "if_photo": "1", "face": "1"}):
    aid = t.create_sign(COURSE, CLAZZ, time_long="1800000", title="拍照v12-otherId1", verbose=False, **kw)
    print("[create otherId=1 %s] aid=%s" % (json.dumps(kw, ensure_ascii=False), aid))
    if aid:
        d = S.get(MOBILE + "/newsign/signDetail?activePrimaryId=%s&type=1" % aid, timeout=25).json()
        print("   signDetail: otherId=%s ifPhoto=%s status=%s" % (d.get("otherId"), d.get("ifPhoto"), d.get("status")))
        p = S.get(MOBILE + "/v2/apis/active/getPPTActiveInfo?activeId=%s" % aid, timeout=25).text
        print("   pptActiveInfo keys:", sorted(json.loads(p).get("data", {}).keys())[:40])
        break

print("\n=== 2) fid=328749 变体（活动所属学校）===")
AID = "4000180999320"
def go(tag, pairs, method="GET"):
    url = MOBILE + "/pptSign/stuSignajax?" + "&".join("%s=%s" % (k, quote(str(v), safe="")) for k, v in pairs)
    rr = S.get(url, timeout=25) if method == "GET" else S.post(MOBILE + "/pptSign/stuSignajax", data=dict(pairs), timeout=25)
    print("[%-26s] %s :: %s" % (tag, rr.status_code, rr.text.strip()[:120]))
    return rr.text.strip()

for fid in ("328749", "102"):
    go("fid=%s+oid" % fid, [("activeId", AID), ("uid", "493228247"), ("clientip", ""), ("useragent", ""),
                            ("latitude", "-1"), ("longitude", "-1"), ("appType", "15"), ("fid", fid),
                            ("objectId", OID), ("name", "学生示例")])
    go("fid=%s+oid+course" % fid, [("activeId", AID), ("uid", "493228247"), ("fid", fid), ("courseId", COURSE),
                                   ("classId", CLAZZ), ("clientip", ""), ("appType", "15"), ("name", "学生示例"),
                                   ("useragent", ""), ("objectId", OID), ("latitude", "-1"), ("longitude", "-1")])

print("\n=== 3) preSign 页面差异（otherId=0+ifPhoto vs 普通）===")
def page(aid, tag):
    u = (MOBILE + "/newsign/preSign?courseId=%s&classId=%s&activePrimaryId=%s&general=1&sys=1&ls=1&appType=15"
         "&uid=493228247&isTeacherViewOpen=0" % (COURSE, CLAZZ, aid))
    r = S.get(u, timeout=25)
    txt = r.text
    marks = {k: txt.count(k) for k in ("newOpenPhoto", "objectId", "photoResult", "deviceCode", "CLIENT_CHOOSE_IMAGE",
                                       "ifPhoto", "photoAuth", "captcha", "VALIDATE_CODE_STR", "signToken", "enc2")}
    print("[page %s] aid=%s len=%d %s" % (tag, aid, len(txt), json.dumps(marks)))
    open("out/preSign_%s_%s.html" % (tag, aid), "w", encoding="utf-8").write(txt)
    return txt
page(AID, "photo_v12")
