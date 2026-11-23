#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
qr_screen_sim.py —— 「教师大屏二维码」模拟器（用来实测扫码签到链路 / 抢 5 秒刷新窗口）

做的事：按固定周期向学习通教师端要一次**当前有效 enc**（GET /v2/apis/sign/refreshQRCode），
        把它渲染成真正的二维码 PNG 落到目录里（默认同时更新 latest.png）。
        动态二维码（ifRefreshEwm=1）时每次拿到的 enc 都不同 —— 正好模拟大屏每 N 秒刷新。

用法：
  python3 qr_screen_sim.py --aid 4000180998898 --out out/qrdrop --interval 2 --count 30
  python3 qr_screen_sim.py --aid 4000180998898 --out out/qrdrop --serve 8899   # 顺带起个网页当大屏
"""
import argparse, os, sys, time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import requests
try:
    import qrcode
except ImportError:
    sys.exit("need: pip install qrcode pillow")

MOBILE = "https://mobilelearn.chaoxing.com/"
UA = ("Mozilla/5.0 (Linux; Android 13; SM-S9180 Build/TPA1.220624.014) "
      "AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/114.0.0.0 "
      "Mobile Safari/537.36 (schild:00000000) (device:SM-S9180) "
      "Language/zh-CN com.chaoxing.mobile/ChaoXingStudy_10946")


def load_cookie(path, raw=""):
    if raw:
        return raw.strip()
    txt = open(path, encoding="utf-8", errors="ignore").read()
    if txt.lstrip().startswith("# Netscape") or "\t" in txt.splitlines()[0]:
        pairs = []
        for line in txt.splitlines():
            if not line.strip() or line.startswith("#"):
                continue
            p = line.split("\t")
            if len(p) >= 7:
                pairs.append("%s=%s" % (p[5], p[6]))
        return "; ".join(pairs)
    return txt.strip()


def qr_url(aid, enc, c="1"):
    return ("https://mobilelearn.chaoxing.com/widget/sign/e?id=%s&c=%s&enc=%s"
            "&DB_STRATEGY=PRIMARY_KEY&STRATEGY_PARA=id" % (aid, c, enc))


def fetch_enc(sess, aid):
    r = sess.get(MOBILE + "v2/apis/sign/refreshQRCode?activeId=%s&time=%d" % (aid, int(time.time() * 1000)),
                 timeout=20)
    try:
        j = r.json()
    except ValueError:
        return None, r.text[:200]
    d = j.get("data") or {}
    return d.get("enc"), j


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--aid", required=True, help="签到活动 id（activeId）")
    ap.add_argument("--out", default="out/qrdrop", help="二维码 PNG 落盘目录")
    ap.add_argument("--interval", type=float, default=2.0, help="刷新周期秒（模拟大屏刷新）")
    ap.add_argument("--count", type=int, default=30, help="生成多少个后停（0=无限）")
    ap.add_argument("--cookie-file", default="ck_tch.txt")
    ap.add_argument("--cookie", default="")
    ap.add_argument("--serve", default="", help="可选：起 HTTP 服务把二维码当网页大屏（端口）")
    a = ap.parse_args()

    ck = load_cookie(a.cookie_file, a.cookie)
    sess = requests.Session()
    sess.headers.update({"Cookie": ck, "User-Agent": UA})
    os.makedirs(a.out, exist_ok=True)

    if a.serve:
        import threading
        from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

        class H(BaseHTTPRequestHandler):
            def log_message(self, *x):
                pass

            def do_GET(self):
                p = os.path.join(a.out, "latest.png")
                if not os.path.exists(p):
                    self.send_response(404); self.end_headers(); return
                b = open(p, "rb").read()
                self.send_response(200)
                self.send_header("Content-Type", "image/png")
                self.send_header("Content-Length", str(len(b)))
                self.end_headers()
                self.wfile.write(b)

        srv = ThreadingHTTPServer(("0.0.0.0", int(a.serve)), H)
        threading.Thread(target=srv.serve_forever, daemon=True).start()
        print("[sim] 大屏网页: http://<本机IP>:%s/  （手机浏览器打开即可对着它扫）" % a.serve)

    n = 0
    while True:
        enc, raw = fetch_enc(sess, a.aid)
        if not enc:
            print("[sim] 取 enc 失败: %s" % str(raw)[:200])
        else:
            n += 1
            url = qr_url(a.aid, enc, c=str(n))
            img = qrcode.make(url)
            name = "qr_%03d_%s.png" % (n, enc[:8])
            img.save(os.path.join(a.out, name))
            img.save(os.path.join(a.out, "latest.png"))
            print("[sim] #%d enc=%s -> %s/%s" % (n, enc, a.out, name))
        if a.count and n >= a.count:
            break
        time.sleep(max(0.3, a.interval))
    print("[sim] done, %d 张" % n)


if __name__ == "__main__":
    main()
