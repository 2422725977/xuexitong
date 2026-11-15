#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""教师侧二维码/enc 采集探针（需要教师账号登录态 cookie）。

用途：把"教师端签到页 → 当前二维码内容(id/c/enc)"这条路走通，之后学生侧的提交就不需要真人扫码。
原理：教师页把二维码内容渲染进 HTML/JS，客户端读出来画二维码；只要我们有教师 cookie，
      就能自己反复拉取这份内容，拿到**新鲜 enc**，随到随签。

用法：
  python3 tch_qr_probe.py --aid 4000180737792 --course 269282723 --class 159750 --uid <教师uid> \
      --cookie-file ck_tch.txt --times 3 --interval 8 --out out/tch_probe
输出：每轮的页面大小、候选 enc/signCode/二维码链接、以及跨轮变化对比；原文存 out/tch_probe/roundN.html
"""
import argparse
import os
import re
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from stealth_session import make_session  # noqa: E402

RE_URL_QR = re.compile(r"widget/sign/e\?[^\"'\s<>]+")
RE_ENC_ANY = re.compile(r"[?&]enc=([0-9A-Fa-f]{16,64})")
RE_ENC_VAR = re.compile(r"""(?:var\s+)?enc\s*[=:]\s*["']([^"']{8,128})["']""")
RE_SIGNCODE = re.compile(r"""signCode["'\s:=]{1,4}([A-Za-z0-9]{4,12})""")
RE_EWM_LINK = re.compile(r"https?://[^\"'\s<>]*?(?:sign|ewm|qrcode)[^\"'\s<>]*")
RE_IMG = re.compile(r"https?://[^\"'\s<>]+\.(?:png|jpg|jpeg)")
RE_AJAX = re.compile(r"""url\s*:\s*["']([^"']{3,160})["']""")

TEACHER_URLS = [
    "https://mobilelearn.chaoxing.com/pptSign/gotasksign?courseId={course}&classId={cls}"
    "&activePrimaryId={aid}&source=1&isTeacherViewOpen=1",
    "https://mobilelearn.chaoxing.com/newsign/preSign?activePrimaryId={aid}&sys=1&chatId="
    "&general=&ls=1&appType=15&courseId={course}&classId={cls}&uid={uid}&isTeacherViewOpen=1",
    "https://mobilelearn.chaoxing.com/newsign/signDetail?activePrimaryId={aid}&type=1",
]


def probe_once(sess, urls, tag, out_dir, verbose=True):
    found = {"enc": set(), "qr": set(), "signCode": set(), "img": set(), "ajax": set()}
    rep = []
    for i, u in enumerate(urls):
        try:
            r = sess.get(u, allow_redirects=True, timeout=20)
        except Exception as e:  # noqa: BLE001
            rep.append((i, u[:90], "ERR " + str(e)[:60], 0))
            continue
        body = r.text or ""
        rep.append((i, u[:90], r.status_code, len(body)))
        if out_dir:
            os.makedirs(out_dir, exist_ok=True)
            with open(os.path.join(out_dir, "%s_%d.html" % (tag, i)), "w", encoding="utf-8", errors="ignore") as f:
                f.write(body)
        found["enc"] |= set(RE_ENC_ANY.findall(body))
        found["enc"] |= {v for v in RE_ENC_VAR.findall(body) if len(v) >= 16 and re.fullmatch(r"[0-9A-Za-z+/=_\-]+", v)}
        found["qr"] |= set(RE_URL_QR.findall(body))
        found["signCode"] |= set(RE_SIGNCODE.findall(body))
        found["img"] |= {v for v in RE_IMG.findall(body) if "teachingPlan" in v or "ewm" in v or "qrcode" in v.lower()}
        found["ajax"] |= {v for v in RE_AJAX.findall(body) if re.search(r"sign|ewm|qr|active", v, re.I)}
    if verbose:
        for i, u, st, n in rep:
            print("   [%d] %s -> %s %dB" % (i, u, st, n))
    return found


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--aid", required=True, help="activePrimaryId（签到活动 id）")
    ap.add_argument("--course", required=True)
    ap.add_argument("--class", dest="cls", required=True, help="classId")
    ap.add_argument("--uid", default="", help="教师 uid")
    ap.add_argument("--cookie", default="")
    ap.add_argument("--cookie-file", default="")
    ap.add_argument("--times", type=int, default=3)
    ap.add_argument("--interval", type=float, default=8.0)
    ap.add_argument("--out", default="")
    ap.add_argument("--ua-mode", default="browser", choices=["browser", "h5", "app"])
    a = ap.parse_args()

    ck = (a.cookie or "").strip()
    if not ck and a.cookie_file and os.path.exists(a.cookie_file):
        with open(a.cookie_file, "r", encoding="utf-8", errors="ignore") as f:
            ck = f.read().strip().splitlines()[0].strip()
    if not ck:
        print("[!] 需要教师登录态 cookie（--cookie / --cookie-file ck_tch.txt）")
        return 2

    sess = make_session(cookie=ck, uid=a.uid, referer="https://mobilelearn.chaoxing.com/",
                        ua_mode=a.ua_mode, xhr=True)
    urls = [u.format(course=a.course, cls=a.cls, aid=a.aid, uid=a.uid) for u in TEACHER_URLS]
    print("[*] 教师侧探针 aid=%s course=%s class=%s ua=%s" % (a.aid, a.course, a.cls, a.ua_mode))
    prev = None
    for n in range(1, a.times + 1):
        print("[*] 第 %d/%d 轮" % (n, a.times))
        f = probe_once(sess, urls, "round%d" % n, a.out)
        for k in ("enc", "qr", "signCode", "img", "ajax"):
            vals = sorted(f[k])
            print("   %-9s %d %s" % (k, len(vals), vals[:6]))
        cur = (tuple(sorted(f["enc"])), tuple(sorted(f["qr"])))
        if prev is not None:
            print("   [变化] enc %s / qr %s" % ("变了" if cur[0] != prev[0] else "没变",
                                               "变了" if cur[1] != prev[1] else "没变"))
        prev = cur
        if n < a.times:
            time.sleep(a.interval)
    print("[*] 如果 enc 拿到了：直接喂 qr_sign_remote.py --qr \"<widget/sign/e?...>\" 即可提交")
    return 0


if __name__ == "__main__":
    sys.exit(main())
