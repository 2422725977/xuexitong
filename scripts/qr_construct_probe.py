# -*- coding: utf-8 -*-
"""二维码 enc 可构建性 + 学生侧消息/通知接口探测。"""
import json, os, re, sys, time, hashlib
import requests
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cx_pipeline as C
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

UA_APP = ('Mozilla/5.0 (Linux; Android 13; SM-G975F Build/TQ3A.230901.001) AppleWebKit/537.36 (KHTML, like Gecko) '
          'Version/4.0 Chrome/120.0.0.0 Mobile Safari/537.36 (schild:26f6a66da55ad239903fba6f674e8c66) (device:SM-G975F) '
          'Language/zh_CN com.ssreader.ChaoXingStudy/ChaoXingStudy_3_6_2_android_phone_20230101')
MOBILE = "https://mobilelearn.chaoxing.com"
COURSE, CLAZZ, TUID, SUID = "269282723", "159926750", "[教师PUID]", "[学生PUID]"
QR_AID = "4000182046940"
sck = open("ck.txt", encoding="utf-8").read().strip()
tck = open("ck_tch.txt", encoding="utf-8").read().strip()
S = requests.Session(); S.headers.update({"Cookie": sck, "User-Agent": UA_APP})
T = requests.Session(); T.headers.update({"Cookie": tck, "User-Agent": UA_APP})
out = {}

print("===== A) enc 采样：形状与可构建性 =====")
samples = []
for i in range(8):
    ts = int(time.time() * 1000)
    r = T.get(MOBILE + "/v2/apis/sign/refreshQRCode", params={"activeId": QR_AID, "time": str(ts)}, timeout=20)
    try:
        d = r.json().get("data") or {}
        enc = d.get("enc") or ""
        row = {"ts": ts, "enc": enc, "signCode": d.get("signCode"), "refresh": d.get("refresh"), "len": len(enc)}
        samples.append(row)
        print("  ts=%d enc=%-36s len=%d signCode=%s refresh=%s" % (ts, enc, len(enc), row["signCode"], row["refresh"]))
    except Exception as e:
        print("  ERR", e)
    time.sleep(1.2)
out["enc_samples"] = samples
encs = [s["enc"] for s in samples if s["enc"]]
print("[enc] 去重后 %d 个 / 采样 %d 次；长度集合 %s" % (len(set(encs)), len(encs), sorted({len(e) for e in encs})))

# 候选公式（离线暴力，只看能不能命中）
def try_forms(enc, aid, signcode, ts):
    cands = {}
    for name, v in [("md5(aid)", aid), ("md5(aid+sc)", aid + str(signcode)), ("md5(sc+aid)", str(signcode) + aid),
                    ("md5(aid+ts)", aid + str(ts)), ("md5(ts+aid)", str(ts) + aid)]:
        cands[name] = hashlib.md5(v.encode()).hexdigest()
    hits = [k for k, v in cands.items() if v.lower() == enc.lower()]
    return hits
for s in samples:
    if s["enc"]:
        h = try_forms(s["enc"], QR_AID, s["signCode"], s["ts"])
        if h: print("  ★ 命中公式:", h)
try:
    print("[enc] 同活动内 enc 是否稳定：", len(set(encs)) == 1, "→ 轮换中应 False")
except Exception: pass

print()
print("===== B) getPPTActiveInfo 全字段找 enc/码 =====")
r = S.get(MOBILE + "/v2/apis/active/getPPTActiveInfo", params={"activeId": QR_AID}, timeout=25)
info = r.json().get("data") or {}
keys = sorted(info.keys())
print("[info] 字段数=%d" % len(keys))
hitk = [k for k in keys if re.search(r"enc|code|token|secret|sign", k, re.I)]
print("[info] 含 enc/code/token/sign 的键:", {k: info[k] for k in hitk})
print("[info] enc 值里是否含真 enc 串:", any(s["enc"] and s["enc"] in str(v) for s in samples for v in info.values()))
out["infokeys"] = keys
out["infohit"] = {k: info.get(k) for k in hitk}

print()
print("===== C) 学生侧消息/通知类接口探测 =====")
cands = [
    ("/v2/apis/message/getMessageList", {"fid": "0", "page": "1", "pageSize": "20"}),
    ("/v2/apis/message/list", {"page": "1", "pageSize": "20"}),
    ("/v2/apis/notice/list", {"page": "1", "pageSize": "20"}),
    ("/v2/apis/push/msglist", {"page": "1", "pageSize": "20"}),
    ("/v2/apis/active/student/activemsg", {"courseId": COURSE, "classId": CLAZZ}),
    ("/v2/apis/active/student/coursemsg", {"courseId": COURSE, "classId": CLAZZ, "page": "1", "pageSize": "20"}),
    ("/v2/apis/active/student/courseactivecount", {"courseId": COURSE, "classId": CLAZZ}),
    ("/ppt/activeAPI/classTaskCount", {"courseId": COURSE, "classId": CLAZZ, "uid": SUID}),
    ("/v2/apis/active/getActiveDataV2", {"activeId": QR_AID}),
    ("/ppt/taskAPI/getActiveDataV2", {"activeId": QR_AID}),
]
res = {}
for path, p in cands:
    try:
        rr = S.get(MOBILE + path, params=p, timeout=20)
        body = rr.text.strip().replace(chr(10), " ")[:220]
        res[path] = {"http": rr.status_code, "body": body}
        print("%-46s HTTP %s  %s" % (path, rr.status_code, body))
    except Exception as e:
        res[path] = {"err": str(e)}; print("%-46s ERR %s" % (path, e))
out["msg_probe"] = res

json.dump(out, open("out/qr_construct.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print()
print("[saved] out/qr_construct.json")
