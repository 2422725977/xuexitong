#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ewm_watch.py —— 二维码"展示会话"监视器

用途：判断学习通二维码签到里的"过期"到底是【帧太旧】还是【这枚二维码的展示会话被关了】。

原理（来自 preSign 页面 JS）：
    ajax /newsign/signDetail {activePrimaryId, type:1, msg}
    if(res.isOver==1){ showTip("二维码已过期"); return; }
    if(msg==res.signCode){ navOpen(); } else { 二维码不正确/已过期 }
  → isOver 是"这枚二维码（ewm）"的状态，不是活动状态；活动 status 另算。

用法：
  # 只看状态变化（每 2s 一次，默认 5 分钟）
  python3 scripts/ewm_watch.py --aid 4000180737792 --cookie-file ck.txt

  # 观察到 isOver 翻回 0 时，自动用已知 enc 立即提交（验证"会话活着 = 旧 enc 也认"）
  python3 scripts/ewm_watch.py --aid 4000180737792 --cookie-file ck.txt \
      --enc 0390B614FB587601ADFAE24467D5700D --submit --uid [学生PUID]
"""
import argparse, json, sys, time, urllib.parse, requests

APP_UA = ("Mozilla/5.0 (Linux; U; Android 13) AppleWebKit/533.1 (KHTML, like Gecko) "
          "Version/4.0 ChaoXingStudy_10946Safari")
BASE = "https://mobilelearn.chaoxing.com"


def headers(cookie):
    return {
        "User-Agent": APP_UA,
        "X-Requested-With": "com.chaoxing.mobile",
        "Referer": BASE + "/",
        "Cookie": cookie,
    }


def sign_detail(s, aid):
    r = s.get(BASE + "/newsign/signDetail",
              params={"activePrimaryId": aid, "type": 1},
              headers=headers(s.cookies.get("__cookie__", "")), timeout=20)
    try:
        return r.status_code, r.json()
    except Exception:
        return r.status_code, {"_raw": r.text[:200]}


def submit(s, aid, enc, uid, fid="0", name=""):
    url = BASE + "/pptSign/stuSignajax?" + urllib.parse.urlencode({
        "enc": enc, "name": name, "activeId": aid, "uid": uid,
        "clientip": "", "location": "", "latitude": "-1", "longitude": "-1",
        "fid": fid, "appType": "15", "deviceCode": "", "vpProbability": "", "vpStrategy": "",
    })
    r = s.get(url, headers=headers(s.cookies.get("__cookie__", "")), timeout=20)
    return r.status_code, r.text.strip()[:200]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--aid", required=True, help="活动的 activePrimaryId / activeId")
    ap.add_argument("--cookie-file", required=True)
    ap.add_argument("--cookie", default="")
    ap.add_argument("--enc", default="", help="已知 enc；配合 --submit 在 isOver 翻 0 时立刻提交")
    ap.add_argument("--submit", action="store_true")
    ap.add_argument("--uid", default="")
    ap.add_argument("--fid", default="0")
    ap.add_argument("--name", default="")
    ap.add_argument("--interval", type=float, default=2.0)
    ap.add_argument("--duration", type=float, default=300.0)
    a = ap.parse_args()

    ck = a.cookie or open(a.cookie_file, encoding="utf-8").read().strip()
    s = requests.Session()
    s.cookies.set("__cookie__", ck)  # 只为 headers() 取用
    s.headers.update({"User-Agent": APP_UA, "X-Requested-With": "com.chaoxing.mobile",
                      "Referer": BASE + "/", "Cookie": ck})

    print(f"[*] 监视 aid={a.aid}  间隔 {a.interval}s  时长 {a.duration}s"
          + (f"  enc={a.enc[:8]}…（翻 0 即提交）" if a.submit and a.enc else ""))
    prev = None
    t0 = time.time()
    while time.time() - t0 < a.duration:
        st, d = sign_detail(s, a.aid)
        if isinstance(d, dict) and "isOver" in d:
            cur = (d.get("isOver"), d.get("isBegins"), d.get("status"),
                   d.get("signCode"), d.get("attendNum"))
            if cur != prev:
                ts = time.strftime("%H:%M:%S")
                print(f"[{ts}] isOver={cur[0]} isBegins={cur[1]} status={cur[2]} "
                      f"signCode={cur[3]} attendNum={cur[4]}")
                prev = cur
            else:
                print(f"[{time.strftime('%H:%M:%S')}] 无变化 isOver={cur[0]} signCode={cur[3]}", end="\r")
            if a.submit and a.enc and d.get("isOver") == 0:
                print()
                print("[!] isOver==0（二维码展示会话活着）→ 用已知 enc 立即提交")
                code, body = submit(s, a.aid, a.enc, a.uid, a.fid, a.name)
                print(f"    HTTP {code}  {body}")
                if body in ("success", "success2"):
                    print("[+] 签到成功 —— 证明 enc 是活动级恒定的，过期只是会话关闭")
                    return
                else:
                    print("[-] 仍被拒 —— 说明 enc 与帧/时间绑定，必须新鲜帧")
        else:
            print(f"[!] signDetail 异常: {st} {d}")
        time.sleep(a.interval)
    print("\n[*] 监视结束")


if __name__ == "__main__":
    main()
