# -*- coding: utf-8 -*-
"""学生端「零二维码、零教师账号」远程签到可行性实测。
只用学生 cookie：activelist 发现活动 -> getPPTActiveInfo 判型 -> 按型提交。
"""
import json, os, re, sys, time
import requests
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cx_pipeline as C
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

UA_APP = ('Mozilla/5.0 (Linux; Android 13; SM-G975F Build/TQ3A.230901.001) AppleWebKit/537.36 (KHTML, like Gecko) '
          'Version/4.0 Chrome/120.0.0.0 Mobile Safari/537.36 (schild:26f6a66da55ad239903fba6f674e8c66) (device:SM-G975F) '
          'Language/zh_CN com.ssreader.ChaoXingStudy/ChaoXingStudy_3_6_2_android_phone_20230101')
MOBILE = "https://mobilelearn.chaoxing.com"
COURSE, CLAZZ, TUID, SUID = "269282723", "159926750", "[教师PUID]", "[学生PUID]"
FID, CHATID = "0", "330606364917761"
sck = open("ck.txt", encoding="utf-8").read().strip()
tck = open("ck_tch.txt", encoding="utf-8").read().strip()
S = requests.Session(); S.headers.update({"Cookie": sck, "User-Agent": UA_APP})
T = C.TeacherSide(tck, TUID, quiet_hours=None, max_writes_per_hour=60, min_interval=0.2, per_day=2000)
out = {"ts": time.strftime("%Y-%m-%d %H:%M:%S")}

def activelist(show_started="0", extra=None):
    p = {"fid": FID, "courseId": COURSE, "classId": CLAZZ,
         "showNotStartedActive": show_started, "_": str(int(time.time()*1000))}
    if extra: p.update(extra)
    r = S.get(MOBILE + "/v2/apis/active/student/activelist", params=p, timeout=30)
    try: d = r.json().get("data") or {}
    except Exception: d = {}
    return r.status_code, d

def pptinfo(aid):
    try:
        return S.get(MOBILE + "/v2/apis/active/getPPTActiveInfo", params={"activeId": aid}, timeout=25).json().get("data") or {}
    except Exception:
        return {}

def submit(aid, **kw):
    params = {"activeId": aid, "courseId": COURSE, "uid": SUID, "clientip": "", "useragent": "", 
              "latitude": "-1", "longitude": "-1", "appType": "0", "fid": FID, "name": ""}
    params.update(kw)
    r = S.get(MOBILE + "/pptSign/stuSignajax", params=params, timeout=25)
    return r.status_code, r.text.strip()[:120]

# 1) 教师造三个活动（模拟真实老师发起的签到）
fixtures = {}
for kind, kws in [("normal", dict(other_id="0")),
                  ("code", dict(other_id="5", code="123456")),
                  ("qr", dict(other_id="2"))]:
    aid = T.create_sign(COURSE, CLAZZ, time_long="1800000", start=True, title="stu-remote-" + kind, **kws)
    fixtures[kind] = aid
    print("[fixture] %-6s aid=%s" % (kind, aid))
out["fixtures"] = fixtures
time.sleep(1)

# 2) 学生侧：只用学生 cookie 发现活动
st, d = activelist()
print()
print("===== 学生端 activelist (只用学生 cookie) =====")
print("[activelist] HTTP=%s keys=%s total=%s" % (st, list(d.keys())[:8], d.get("total") or d.get("totalCount")))
lst = d.get("activeList") or d.get("list") or []
print("[activelist] 条数=%s" % len(lst))
out["activelist"] = {"http": st, "keys": list(d.keys()), "count": len(lst)}
seen = []
for a in lst[:12]:
    aid = str(a.get("id") or a.get("activeId") or "")
    seen.append((aid, a.get("title") or a.get("name"), a.get("userStatus"), a.get("status")))
print("[activelist] 前 12 条 (aid, title, userStatus, status):")
for s in seen: print("   ", s)
out["activelist_rows"] = seen

# 3) 学生侧判型 + 提交（不用二维码、不用教师 cookie）
print()
print("===== 学生侧判型 + 提交 =====")
res = {}
for aid in [fixtures["normal"], fixtures["code"], fixtures["qr"]]:
    info = pptinfo(aid)
    typ = {"otherId": info.get("otherId"), "ifphoto": info.get("ifphoto"),
           "ifopenAddress": info.get("ifopenAddress"), "status": info.get("status"),
           "title": info.get("title"), "chatid": info.get("chatid")}
    code, body = submit(aid)
    res[aid] = {"info": typ, "submit": {"http": code, "body": body}}
    print("aid=%s type=%s ifphoto=%s ifopenAddress=%s -> 提交 HTTP %s : %s"
          % (aid, typ["otherId"], typ["ifphoto"], typ["ifopenAddress"], code, body))
out["submit"] = res

# 4) 签到码类：学生能不能从任何学生侧接口读到码？
print()
print("===== 学生侧能否读到签到码/enc =====")
probe = {}
for name, url, params in [
    ("refreshQRCode", MOBILE + "/v2/apis/sign/refreshQRCode", {"activeId": fixtures["qr"], "time": str(int(time.time()*1000))}),
    ("getSignCode(stu)", MOBILE + "/widget/sign/pcStuSignController/getSignCode", {"activeId": fixtures["code"]}),
    ("getSignCode(tea)", MOBILE + "/widget/sign/pcTeaSignController/getSignCode", {"activeId": fixtures["code"]}),
    ("getLastSigninSettings", MOBILE + "/widget/sign/pcTeaSignController/getLastSigninSettings", {"activeId": fixtures["code"]}),
    ("signDetail", MOBILE + "/newsign/signDetail", {"activePrimaryId": fixtures["code"], "type": "1"}),
]:
    try:
        r = S.get(url, params=params, timeout=20)
        body = r.text.strip().replace(chr(10), " ")[:160]
        probe[name] = {"http": r.status_code, "body": body}
        print("%-24s HTTP %s  %s" % (name, r.status_code, body))
    except Exception as e:
        probe[name] = {"err": str(e)}; print("%-24s ERR %s" % (name, e))
out["probe"] = probe

json.dump(out, open("out/stu_remote.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print()
print("[saved] out/stu_remote.json")
