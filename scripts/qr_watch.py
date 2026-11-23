#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
qr_watch.py —— 扫码签到「抢签器」：多源取码 → 新码立即提交 → 成功即停

为什么需要它：二维码签到分两种模式
  * ifRefreshEwm=0  静态二维码：一张截图永久有效（随便什么时候签都行）
  * ifRefreshEwm=1  动态二维码：enc 每 N 秒（常见 5 秒）轮换，**旧码提交必回「签到失败，请重新扫描。」**
    所以动态码是「抢时间」问题：必须拿到码后立刻提交。本脚本就是干这个的。

输入源（--source）：
  folder  监视目录：委托方/同学把截图丢进来即签（最通用）
  screen  macOS 本机屏幕（对着显示器上的二维码/网页大屏）
  adb     手机屏幕截图（同学把大屏码显示在自己手机上，或手机浏览器开着大屏网页）
  camera  手机连拍（用相机 App 对着大屏/另一台手机，边拍边解边签）
  http    轮询一个 URL（页面里自动找 enc，或直接是要解析的图片）
  text    直接给一段二维码内容，只跑一次

用法：
  python3 qr_watch.py --source folder --dir ~/qrdrop --uid [学生PUID] --cookie-file ck.txt --stop-on-success
  python3 qr_watch.py --source adb --serial [设备序列号] --uid [学生PUID] --cookie-file ck.txt --stop-on-success
  python3 qr_watch.py --source screen --region 0,0,1440,900 --uid [学生PUID] --cookie-file ck.txt
  python3 qr_watch.py --source http --url 'https://mobilelearn.chaoxing.com/widget/sign/e?id=...' --uid [学生PUID] --cookie-file ck.txt
  python3 qr_watch.py --source text --text 'https://...widget/sign/e?id=<aid>&c=1&enc=<ENC>...' --uid [学生PUID] --cookie-file ck.txt

  # 手里只有一串 enc（新版二维码可能就只印 enc）时，补上活动 id 也能签：
  python3 qr_watch.py --source text --text 4F425653877C633063DC5ADB2F975CE8 --active-id 4000180998898 ...
"""
import argparse, hashlib, os, re, subprocess, sys, tempfile, time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    import qr_sign_remote as qsr
except Exception as e:
    sys.exit("need qr_sign_remote.py in same dir: %r" % e)

try:
    import cv2
    import numpy as np
except ImportError:
    cv2 = None
    np = None

ADB = os.environ.get("ADB", "adb")
IMG_EXT = (".png", ".jpg", ".jpeg", ".webp", ".bmp", ".gif")
RE_ENC = re.compile(r"\benc=([0-9A-Fa-f]{16,64})\b")
RE_HEX = re.compile(r"^[0-9A-Fa-f]{16,64}$")
DONE_HINT = ("请重新扫描", "二维码时间过期", "链接已失效", "已过期")


def decode_bytes(b):
    if cv2 is None:
        raise RuntimeError("need opencv-python-headless")
    arr = cv2.imdecode(np.frombuffer(b, dtype="uint8"), cv2.IMREAD_COLOR)
    if arr is None:
        raise RuntimeError("bad image")
    det = cv2.QRCodeDetector()
    ok, texts, _, _ = det.detectAndDecodeMulti(arr)
    if ok and texts:
        for t in texts:
            if t:
                return t
    t, _, _ = det.detectAndDecode(arr)
    if t:
        return t
    raise RuntimeError("no QR")


def extract_from_text(body, base=""):
    """从 HTML/JSON/纯文本里找二维码内容"""
    if not body:
        return None
    m = RE_ENC.search(body)
    if m:
        aid = ""
        a = re.search(r"[?&](?:id|activeId)=(\d+)", body)
        if a:
            aid = a.group(1)
        return "https://mobilelearn.chaoxing.com/widget/sign/e?id=%s&c=1&enc=%s" % (aid, m.group(1))
    m = re.search(r"(https?://[^\s\"'<>]*widget/sign/e[^\s\"'<>]*)", body)
    if m:
        return m.group(1)
    s = body.strip()
    if RE_HEX.match(s):
        return s
    return None


class Source:
    """每 tick 返回 (content_or_None, image_bytes_or_None)"""

    def __init__(self, a):
        self.a = a
        self.seen_files = set()
        self.last_dcim = ""
        self.seq = 0

    # ---- 各来源 ----
    def folder(self):
        d = os.path.expanduser(self.a.dir)
        os.makedirs(d, exist_ok=True)
        out = []
        for n in sorted(os.listdir(d)):
            if n.startswith("_") or n == "latest.png":
                continue
            p = os.path.join(d, n)
            if not os.path.isfile(p) or n in self.seen_files:
                continue
            time.sleep(0.12)                     # 等写盘完成
            self.seen_files.add(n)
            if n.lower().endswith(IMG_EXT):
                try:
                    out.append((decode_bytes(open(p, "rb").read()), n))
                except Exception as e:
                    print("[folder] %s 解码失败: %s" % (n, e))
            else:
                out.append((open(p, encoding="utf-8", errors="ignore").read().strip(), n))
        return out

    def screen(self):
        fd, tmp = tempfile.mkstemp(suffix=".png")
        os.close(fd)
        cmd = ["screencapture", "-x", "-t", "png"]
        if self.a.region:
            cmd += ["-R", self.a.region]
        cmd.append(tmp)
        subprocess.run(cmd, check=False)
        b = open(tmp, "rb").read()
        os.unlink(tmp)
        try:
            return [(decode_bytes(b), "screen")]
        except Exception:
            return []

    def adb_frame(self):
        r = subprocess.run([ADB] + (["-s", self.a.serial] if self.a.serial else []) +
                           ["exec-out", "screencap", "-p"], capture_output=True)
        if not r.stdout:
            return []
        try:
            return [(decode_bytes(r.stdout), "adb-screen")]
        except Exception:
            return []

    # ---- 手机连拍 ----
    def camera(self):
        ser = (["-s", self.a.serial] if self.a.serial else [])
        if self.seq == 0:
            subprocess.run([ADB] + ser + ["shell", "am", "start", "-a",
                                          "android.media.action.STILL_IMAGE_CAMERA"],
                           capture_output=True)
            time.sleep(2.5)
        self.seq += 1
        subprocess.run([ADB] + ser + ["shell", "input", "keyevent", "27"], capture_output=True)
        time.sleep(0.7)
        r = subprocess.run([ADB] + ser + ["shell", "ls", "-t",
                                          "/sdcard/DCIM/Camera/"], capture_output=True, text=True)
        names = [x.strip() for x in (r.stdout or "").splitlines() if x.strip().lower().endswith((".jpg", ".jpeg"))]
        if not names:
            print("[camera] DCIM/Camera 没找到照片")
            return []
        newest = names[0]
        if newest == self.last_dcim:
            return []
        self.last_dcim = newest
        fd, tmp = tempfile.mkstemp(suffix=".jpg")
        os.close(fd)
        subprocess.run([ADB] + ser + ["pull", "/sdcard/DCIM/Camera/" + newest, tmp],
                       capture_output=True)
        b = open(tmp, "rb").read()
        os.unlink(tmp)
        try:
            return [(decode_bytes(b), "camera:" + newest)]
        except Exception:
            return []

    def http(self):
        import requests
        try:
            r = requests.get(self.a.url, timeout=15,
                             headers={"User-Agent": qsr.UA, "Cookie": self.a.cookie or ""})
        except Exception as e:
            print("[http] 请求失败:", e)
            return []
        ct = (r.headers.get("Content-Type") or "").lower()
        if "image" in ct:
            try:
                return [(decode_bytes(r.content), "http-image")]
            except Exception:
                return []
        c = extract_from_text(r.text)
        return [(c, "http")] if c else []

    def poll(self):
        s = self.a.source
        if s == "folder":
            return self.folder()
        if s == "screen":
            return self.screen()
        if s == "adb":
            return self.adb_frame()
        if s == "camera":
            return self.camera()
        if s == "http":
            return self.http()
        if s == "text":
            if self.seq:
                return []
            self.seq = 1
            return [(self.a.text, "text")]
        return []


def submit_bare_enc(a, sess, enc):
    """手里只有一串 enc：补 activeId 走通道 C"""
    import requests  # noqa
    url = (qsr.MOBILE + "pptSign/stuSignajax?enc=" + enc +
           "&activeId=" + a.active_id + "&uid=" + (a.uid or "") +
           "&name=" + (a.name or "") + "&fid=" + (a.fid or "0") +
           "&clientip=&useragent=&latitude=" + a.lat + "&longitude=" + a.lon + "&appType=15")
    r = sess.get(url, timeout=20)
    body = r.text.strip()
    print("[C/enc] GET %s" % url)
    print("[C/enc] HTTP %s %s" % (r.status_code, body[:200]))
    return {"ok": "success" in body.lower(), "msg": body[:200], "kind": "enc"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", choices=["folder", "screen", "adb", "camera", "http", "text"],
                    default="folder")
    ap.add_argument("--dir", default="~/qrdrop")
    ap.add_argument("--region", default="", help="screen 源截图区域 x,y,w,h")
    ap.add_argument("--serial", default="", help="adb 设备序列号")
    ap.add_argument("--url", default="")
    ap.add_argument("--text", default="")
    ap.add_argument("--uid", default="")
    ap.add_argument("--cookie", default="")
    ap.add_argument("--cookie-file", default="")
    ap.add_argument("--active-id", default="", help="只有裸 enc 时用它补活动 id")
    ap.add_argument("--name", default="")
    ap.add_argument("--fid", default="0")
    ap.add_argument("--lat", default="-1")
    ap.add_argument("--lon", default="-1")
    ap.add_argument("--interval", type=float, default=0.8)
    ap.add_argument("--max-seconds", type=float, default=600)
    ap.add_argument("--max-submits", type=int, default=40)
    ap.add_argument("--repeat", type=int, default=1)
    ap.add_argument("--stop-on-success", action="store_true")
    ap.add_argument("--append-log", default="")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    a.cookie = qsr.load_cookie(a.cookie, a.cookie_file)
    if not a.cookie:
        sys.exit("need --cookie / --cookie-file")
    if not a.uid:
        m = re.search(r"(?:^|;\s*)_uid=([0-9]+)", a.cookie) or re.search(r"puid=([0-9]+)", a.cookie)
        if m:
            a.uid = m.group(1)
            print("[cfg] uid 从 cookie 推断 = %s" % a.uid)

    import requests
    # 抢签只要快：不用风控层（它的 8s 最小间隔/每小时配额会把 5 秒窗口拖没），只用 App UA + Cookie
    sess = requests.Session()
    sess.headers.update({"User-Agent": qsr.UA, "Accept": "*/*",
                         "Accept-Language": "zh-CN,zh;q=0.9", "Connection": "keep-alive",
                         "Referer": qsr.MOBILE, "Cookie": a.cookie})
    a.phone_id = qsr.phone_id()
    signer = qsr.Signer(a, sess) if hasattr(qsr, "Signer") else None

    src = Source(a)
    t0 = time.time()
    submitted = 0
    hits = set()
    print("[watch] source=%s interval=%.1fs stop_on_success=%s" % (a.source, a.interval, a.stop_on_success))
    while time.time() - t0 < a.max_seconds:
        try:
            items = src.poll()
        except Exception as e:
            print("[watch] 取源异常:", e)
            items = []
        for content, tag in items:
            if not content:
                continue
            key = hashlib.sha1(content.encode("utf-8", "ignore")).hexdigest()
            if key in hits:
                continue
            hits.add(key)
            if a.dry_run:
                print("[dry] %s -> %s" % (tag, content[:160]))
                continue
            if submitted >= a.max_submits:
                print("[watch] 已达 --max-submits=%d，停" % a.max_submits)
                return
            submitted += 1
            print("\n==== [%s] 第 %d 次提交 %s ====" % (time.strftime("%H:%M:%S"), submitted, tag))
            if RE_HEX.match(content.strip()) and a.active_id:
                res = submit_bare_enc(a, sess, content.strip())
            elif signer:
                res = signer.handle(content, source=tag)
            else:
                res = {"ok": False, "msg": "no signer"}
            if a.append_log:
                import json as _j
                open(a.append_log, "a", encoding="utf-8").write(
                    _j.dumps({"t": time.strftime("%F %T"), "src": tag, "content": content[:300],
                              "res": res}, ensure_ascii=False) + "\n")
            if res.get("ok"):
                print("[=] 签到成功！（%s）" % tag)
                if a.stop_on_success:
                    return
        if a.source == "text" and src.seq:
            break
        time.sleep(max(0.15, a.interval))
    print("[watch] 结束：提交 %d 次" % submitted)


if __name__ == "__main__":
    main()
