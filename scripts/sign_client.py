#!/usr/bin/env python3
"""学习通 6.7.8 扫码签到复现客户端（占位符版）。

协议来源：SignInfoActivity.m5() → wm.a.a + gc.b.j + usersign/addsign?
参数： signId / userId / time / phoneId / enc / ctype=stusign
enc  = md5(signId + "-" + userId + "-" + time + "-" + phoneId)   （小写 hex）
phoneId = 客户端持久化 UUID（32 位无横线 hex），可任意固定
"""
import argparse, hashlib, json, sys, uuid
import urllib.request, urllib.error

BASE = "https://fanyappfy.chaoxing.com/usersign/addsign?"
UA = "Mozilla/5.0 (Linux; Android 11) ChaoXingStudy/6.7.8"

def parse_qr(content: str):
    """二维码内容：{"time":..,"signId":..}，兜底解析成 URL 查询串。"""
    content = content.strip()
    if content.startswith("{"):
        d = json.loads(content)
        return str(d["signId"]), str(d["time"])
    q = {}
    for part in content.split("?")[-1].split("&"):
        if "=" in part:
            k, v = part.split("=", 1)
            q[k] = v
    return q["signId"], q["time"]

def do_sign(sign_id: str, ts: str, uid: str, cookie: str, phone_id: str):
    enc = hashlib.md5(("%s-%s-%s-%s" % (sign_id, uid, ts, phone_id)).encode()).hexdigest()
    url = BASE + "signId=%s&userId=%s&time=%s&phoneId=%s&enc=%s&ctype=stusign" % (
        sign_id, uid, ts, phone_id, enc)
    req = urllib.request.Request(url, headers={"Cookie": cookie, "User-Agent": UA})
    print("GET", url)
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            body = r.read().decode("utf-8", "replace")
            print("HTTP", r.status)
            print(body)
    except urllib.error.HTTPError as e:
        print("HTTP", e.code, e.read().decode("utf-8", "replace"))
    except Exception as e:
        print("ERROR", e)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--qr", required=True, help='二维码内容或 {"signId":..,"time":..}')
    ap.add_argument("--uid", required=True, help="登录账号 puid（cookie 里的 _uid）")
    ap.add_argument("--cookie", required=True, help="学习通登录态 cookie")
    ap.add_argument("--phone-id", default=None, help="固定设备 id（默认随机生成）")
    a = ap.parse_args()
    sign_id, ts = parse_qr(a.qr)
    do_sign(sign_id, ts, a.uid, a.cookie, a.phone_id or uuid.uuid4().hex)

if __name__ == "__main__":
    main()
