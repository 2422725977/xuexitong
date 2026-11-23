# -*- coding: utf-8 -*-
"""学生侧能否从 getPPTActiveInfo 读到「签到码 / 手势码 / 位置真值」——决定各类型能否纯远程签。"""
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
sck = open("ck.txt", encoding="utf-8").read().strip()
tck = open("ck_tch.txt", encoding="utf-8").read().strip()
S = requests.Session(); S.headers.update({"Cookie": sck, "User-Agent": UA_APP})
T = C.TeacherSide(tck, TUID, quiet_hours=None, max_writes_per_hour=60, min_interval=0.2, per_day=2000)
out = {"ts": time.strftime("%Y-%m-%d %H:%M:%S"), "fixtures": {}, "info": {}, "submit": {}}

def info(aid):
    try:
        return S.get(MOBILE + "/v2/apis/active/getPPTActiveInfo", params={"activeId": aid}, timeout=25).json().get("data") or {}
    except Exception:
        return {}

def submit(aid, **kw):
    p = {"activeId": aid, "courseId": COURSE, "uid": SUID, "clientip": "", "useragent": "",
         "latitude": "-1", "longitude": "-1", "appType": "0", "fid": "0", "name": ""}
    p.update(kw)
    r = S.get(MOBILE + "/pptSign/stuSignajax", params=p, timeout=25)
    return r.status_code, r.text.strip()[:120]

# 1) 造三类活动
f = {}
for kind, kws in [("code", dict(other_id="5", code="246810")),
                  ("gesture", dict(other_id="3", code="147258")),
                  ("location", dict(other_id="4", ifopen_address="1",
                                    location={"address": "成都市温江区 四川农业大学(成都校区)",
                                              "latitude": 30.71142640936642,
                                              "longitude": 103.868397592583,
                                              "range": "500米"}))]:
    aid = T.create_sign(COURSE, CLAZZ, time_long="1800000", start=True, title="stu-read-" + kind, **kws)
    f[kind] = aid
    print("[fixture] %-9s aid=%s" % (kind, aid))
out["fixtures"] = f
time.sleep(1)

KEY = re.compile(r"code|location|latitude|longitude|address|range|gesture|point|hand|enc", re.I)
for kind, aid in f.items():
    d = info(aid)
    hits = {k: d[k] for k in d if KEY.search(str(k))}
    out["info"][kind] = {"aid": aid, "otherId": d.get("otherId"), "hits": hits}
    print()
    print("=== %s aid=%s otherId=%s ===" % (kind, aid, d.get("otherId")))
    for k in sorted(hits):
        v = str(hits[k])
        print("   %-26s = %s" % (k, v[:90]))

# 2) 位置类：学生能不能用读到的坐标签成
d = info(f["location"])
lat = d.get("locationLatitude") or d.get("latitude")
lon = d.get("locationLongitude") or d.get("longitude")
addr = d.get("locationText") or ""
if lat and lon and str(lat) != "-1":
    locjson = json.dumps({"result": 1, "address": addr, "longitude": float(lon), "latitude": float(lat)},
                         separators=(",", ":"))
    code, body = submit(f["location"], location=locjson, locationResult=locjson)
    out["submit"]["location_read_from_info"] = {"locjson": locjson, "http": code, "body": body}
    print()
    print("[location] 用 getPPTActiveInfo 读到的坐标提交 -> HTTP %s : %s" % (code, body))
else:
    print()
    print("[location] 学生侧读不到坐标（lat/lon 缺失或 -1）→ 需要教师活动页")

# 3) 签到码类：读到的 signCode 能不能提交
d = info(f["code"]); sc = d.get("signCode") or d.get("code") or ""
if sc:
    code, body = submit(f["code"], signCode=str(sc))
    out["submit"]["code_read_from_info"] = {"signCode": str(sc), "http": code, "body": body}
    print("[code] 用 getPPTActiveInfo 读到的 signCode=%s 提交 -> HTTP %s : %s" % (sc, code, body))
else:
    print("[code] 学生侧读不到 signCode")

json.dump(out, open("out/stu_read_secret.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print()
print("[saved] out/stu_read_secret.json")
