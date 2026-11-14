#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
qr_sign_remote.py - 学习通(com.chaoxing.mobile) 远程扫码签到 / 无相机 / 无到场
                        v2: 新增「动态二维码」流水线（watch 目录 / serve 中继 / stdin 管道）

协议来自学习通 6.7.8 (versionCode 10946) 解壳后的反编译:
  A) 原生扫签  SignInfoActivity.m5  ->  GET {fanyappfy}/usersign/addsign?
       enc = MD5(signId + "-" + userId + "-" + time + "-" + phoneId)   (com.fanzhou.util.j.d)
       二维码内容 = JSON: {"time":"...","signId":"..."}
  B) H5 扫签  main.f.s("SIGNIN:...") -> GET {mobilelearn}/newsign/studentSign?rcode=<urlenc>&uid=<uid>
  C) 大屏/旧版 URL 二维码  https://mobilelearn.chaoxing.com/widget/sign/e?id=&c=&enc=
       -> GET {mobilelearn}/pptSign/stuSignajax?...&enc=<enc>&activeId=<id>&uid=&fid=&appType=15
       注: c 每 10 秒变，enc/id 全程不变 -> 任意时刻的一张截图都能签

不需要相机、不需要人脸、不需要本人到场；只需要:
  1. 一条登录后的 cookie（学习通主站会话）
  2. 你的 puid (uid)
  3. 二维码的内容文本 或 一张二维码截图 —— 而且**多旧都行**

用法:
  # 一次性
  python3 qr_sign_remote.py --qr '{"time":"1712000000","signId":"1234567890"}' --uid 1 --cookie-file ck.txt
  python3 qr_sign_remote.py --qr-image qr.png --uid 1 --cookie-file ck.txt

  # 动态二维码（几秒刷一次）：盯目录，新图一进来就解+签
  python3 qr_sign_remote.py --watch ~/qrdrop --uid 1 --cookie-file ck.txt

  # 动态二维码最优解：起一个中继服务，让能看见二维码的人/机器直接 POST 给它
  python3 qr_sign_remote.py --serve 8765 --uid 1 --cookie-file ck.txt --token mysecret
  #   curl "http://127.0.0.1:8765/sign?text=<二维码原文>&token=mysecret"
  #   curl -X POST --data-binary @qr.png "http://127.0.0.1:8765/image?token=mysecret"

  # 从管道读（配合截图工具/热键脚本）
  tail -f qrlines.txt | python3 qr_sign_remote.py --stdin --uid 1 --cookie-file ck.txt
"""
import argparse, hashlib, json, os, shutil, sys, threading, time, urllib.parse

try:
    import requests
except ImportError:
    sys.exit("need: pip install requests")

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:                        # 伪装层：设备档案 / 完整头 / 拟人延迟 / 掩护流量 / 风控熔断
    from stealth_session import (make_session, Device, warmup, human_delay,
                                 explain as stealth_explain, HAVE_CFFI,
                                 RiskHalt, RiskCooldown, parse_quiet)
except Exception:
    make_session = warmup = human_delay = None
    Device = None
    HAVE_CFFI = False
    def stealth_explain(*a, **k):
        return ""
    class RiskHalt(RuntimeError):
        pass
    class RiskCooldown(RuntimeError):
        pass
    def parse_quiet(s):
        return None

UA = ("Mozilla/5.0 (Linux; Android 13; SM-S9180 Build/TP1A.220624.014; wv) "
      "AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/114.0.0.0 "
      "Mobile Safari/537.36 (schild:00000000) (device:SM-S9180) "
      "Language/zh-CN com.chaoxing.mobile/ChaoXingStudy_10946")

FANYA   = "https://fanyappfy.chaoxing.com/"
MOBILE  = "https://mobilelearn.chaoxing.com/"
IMG_EXT = (".png", ".jpg", ".jpeg", ".webp", ".bmp", ".gif", ".heic")

ERR = {
    301: "签到失败（数据库插入失败）",
    306: "enc验证错误",
    307: "二维码时间过期",
    308: "签到id不存在",
    309: "用户不存在",
    310: "用户单位信息错误",
    311: "用户角色错误",
    312: "系统错误",
}


def md5hex(s: str) -> str:
    return hashlib.md5(s.encode("utf-8")).hexdigest()


def load_cookie(arg_cookie, arg_file):
    """cookie 可以是一整行 'a=1; b=2'，也可以是 Netscape cookies.txt"""
    if arg_cookie:
        return arg_cookie.strip()
    if not arg_file:
        return ""
    raw = open(arg_file, "r", encoding="utf-8", errors="ignore").read()
    if raw.lstrip().startswith("# Netscape") or ("\t" in (raw.splitlines()[0] if raw.strip() else "")):
        jar = []
        for line in raw.splitlines():
            if not line or line.startswith("#"):
                continue
            p = line.split("\t")
            if len(p) >= 7:
                jar.append("%s=%s" % (p[5], p[6]))
        return "; ".join(jar)
    return raw.strip()


def phone_id(persist="~/.chaoxing_phone_id"):
    """an.b: SharedPreferences appProfile/uniqueId，缺省 = UUID 去横线（32 hex）"""
    p = os.path.expanduser(persist)
    if os.path.exists(p):
        v = open(p).read().strip()
        if v:
            return v
    import uuid
    v = uuid.uuid4().hex
    try:
        open(p, "w").write(v)
    except OSError:
        pass
    return v


def decode_qr_image(path):
    """用 opencv 解二维码"""
    try:
        import cv2
    except ImportError:
        sys.exit("need: pip install opencv-python-headless   (或直接 --qr '<内容文本>')")
    img = cv2.imread(path)
    if img is None:
        raise RuntimeError("cannot read image: " + path)
    det = cv2.QRCodeDetector()
    ok, texts, _, _ = det.detectAndDecodeMulti(img)
    if ok and texts:
        for t in texts:
            if t:
                return t
    t, _, _ = det.detectAndDecode(img)
    if t:
        return t
    raise RuntimeError("no QR found in " + path + "（截屏请裁到只含二维码、尽量正对）")


def decode_qr_bytes(data: bytes):
    """解内存里的图片（中继服务用）"""
    try:
        import cv2
    except ImportError:
        raise RuntimeError("need: pip install opencv-python-headless")
    import numpy as np
    arr = cv2.imdecode(np.frombuffer(data, dtype="uint8"), cv2.IMREAD_COLOR)
    if arr is None:
        raise RuntimeError("bad image bytes")
    det = cv2.QRCodeDetector()
    ok, texts, _, _ = det.detectAndDecodeMulti(arr)
    if ok and texts:
        for t in texts:
            if t:
                return t
    t, _, _ = det.detectAndDecode(arr)
    if t:
        return t
    raise RuntimeError("no QR found in uploaded image")


def classify(content):
    c = content.strip()
    low = c.lower()
    if low.startswith("signin:"):
        return "h5", c
    if "widget/sign/e" in low or ("enc=" in low and ("id=" in low or "activeid" in low)):
        return "url", c
    if "\n" in c and "{" not in c:
        # 可能是一整段二维码 URL 里带了换行
        c = c.replace("\n", "").strip()
    if c.startswith("{"):
        try:
            return "json", json.loads(c)
        except json.JSONDecodeError:
            pass
    try:
        return "json", json.loads(c)
    except Exception:
        return "unknown", c


def submit_native(sess, qr: dict, uid: str, phid: str, verbose=True):
    """通道 A: usersign/addsign"""
    sign_id = str(qr.get("signId") or qr.get("signid") or "")
    t = str(qr.get("time") or "")
    if not sign_id or not t:
        return {"ok": False, "msg": "二维码 JSON 缺少 time/signId: %r" % qr}
    enc = md5hex("%s-%s-%s-%s" % (sign_id, uid, t, phid))
    url = (FANYA + "usersign/addsign?signId=" + urllib.parse.quote(sign_id) +
           "&userId=" + urllib.parse.quote(uid) +
           "&time=" + urllib.parse.quote(t) +
           "&phoneId=" + urllib.parse.quote(phid) +
           "&enc=" + enc + "&ctype=stusign")
    if verbose:
        print("[A] enc = MD5(%s-%s-%s-%s) = %s" % (sign_id, uid, t, phid, enc))
        print("[A] GET %s" % url)
    r = sess.get(url, timeout=15)
    body = r.text.strip()
    if verbose:
        print("[A] HTTP %s  %s" % (r.status_code, body[:500]))
    try:
        j = r.json()
    except ValueError:
        return {"ok": False, "code": None, "msg": body[:300]}
    code = j.get("statusCode")
    return {
        "ok": code == 300, "code": code, "raw": j,
        "msg": j.get("msg") or ERR.get(code, "?"),
        "data": j.get("data"), "stuName": j.get("stuName"),
    }


def submit_h5(sess, content: str, uid: str, verbose=True):
    """通道 B: newsign/studentSign?rcode=<urlenc 整串>&uid=<uid>"""
    url = (MOBILE + "newsign/studentSign?rcode=" +
           urllib.parse.quote(content, safe="") + "&uid=" + urllib.parse.quote(uid))
    if verbose:
        print("[B] GET %s" % url)
    r = sess.get(url, timeout=15)
    body = r.text
    if verbose:
        print("[B] HTTP %s len=%d" % (r.status_code, len(body)))
    hit = None
    for kw in ("签到成功", "已经签到", "已签到", "签到失败", "失败", "过期", "不存在"):
        if kw in body:
            hit = kw
            break
    return {"ok": hit in ("签到成功", "已经签到", "已签到"), "msg": hit or body[:200], "raw": body[:2000]}


def submit_url(sess, content: str, uid: str, name: str, fid: str, lat="-1", lon="-1", verbose=True):
    """通道 C: pptSign/stuSignajax（大屏/旧版二维码，含 enc）"""
    q = urllib.parse.parse_qs(urllib.parse.urlparse(content if content.lower().startswith("http")
                                                   else "https://x/?" + content).query)
    if not q and "?" in content:
        q = urllib.parse.parse_qs(content.split("?", 1)[1])
    aid = (q.get("id") or q.get("activeId") or [""])[0]
    enc = (q.get("enc") or [""])[0]
    if not aid or not enc:
        return {"ok": False, "msg": "URL 二维码里没有 id/enc: %s" % content[:200]}
    url = (MOBILE + "pptSign/stuSignajax?"
           "enc=" + urllib.parse.quote(enc) +
           "&name=" + urllib.parse.quote(name) +
           "&activeId=" + urllib.parse.quote(aid) +
           "&uid=" + urllib.parse.quote(uid) +
           "&clientip=&useragent=&latitude=" + lat + "&longitude=" + lon +
           "&fid=" + urllib.parse.quote(fid) + "&appType=15")
    if verbose:
        print("[C] GET %s" % url)
    r = sess.get(url, timeout=15)
    body = r.text.strip()
    if verbose:
        print("[C] HTTP %s  %s" % (r.status_code, body[:500]))
    return {"ok": ("success" in body.lower() or "签到成功" in body), "msg": body[:300]}


class Signer:
    """把「一段二维码内容」变成「一次提交」的封装，供各种输入模式复用"""

    def __init__(self, a, sess):
        self.a = a
        self.sess = sess
        self.stealth = bool(getattr(a, "stealth", False))
        self.phid = a.phone_id or phone_id()
        self.uid = a.uid or os.environ.get("CHAOXING_UID", "")
        self.seen = set()
        self.last = {}
        self.lock = threading.Lock()
        self.count = {"tried": 0, "ok": 0}

    def handle(self, content, source="", verbose=True):
        if not content or not content.strip():
            return {"ok": False, "msg": "empty content"}
        content = content.strip()
        key = hashlib.sha1(content.encode("utf-8", "ignore")).hexdigest()
        with self.lock:
            if key in self.seen:
                return {"ok": False, "msg": "duplicate (already handled)", "dup": True}
            self.seen.add(key)
        kind, obj = classify(content)
        tag = "[%s]" % (source or kind)
        if kind == "unknown":
            print("%s 无法识别: %s" % (tag, content[:160]))
            return {"ok": False, "msg": "unknown format", "kind": kind}
        if verbose:
            print("%s kind=%s content=%s" % (tag, kind, content[:200]))
        if not self.uid and kind in ("json", "h5", "url"):
            print("%s 缺 uid（用 --uid 或 CHAOXING_UID）" % tag)
            return {"ok": False, "msg": "missing uid"}
        res = {"ok": False, "msg": "not attempted", "kind": kind}
        for i in range(max(1, self.a.repeat)):
            try:
                if kind == "json":
                    res = submit_native(self.sess, obj, self.uid, self.phid, verbose=verbose)
                elif kind == "h5":
                    res = submit_h5(self.sess, obj, self.uid, verbose=verbose)
                else:
                    res = submit_url(self.sess, content, self.uid, self.a.name, self.a.fid,
                                     self.a.lat, self.a.lon, verbose=verbose)
            except RiskHalt as e:          # 登录失效/验证码/403 —— 停手，重试只会更糟
                print("%s [STOP] 风控停机：%s" % (tag, e))
                print("%s [STOP] 去 App 里人工登录/正常签到一次再回来；本次不再提交。" % tag)
                res = {"ok": False, "msg": "risk halt: %s" % e, "halt": True, "kind": kind}
                break
            except RiskCooldown as e:      # 429/限流/配额满 —— 等冷却
                print("%s [WAIT] %s（本次不重试）" % (tag, e))
                res = {"ok": False, "msg": "risk cooldown: %s" % e, "cooldown": True, "kind": kind}
                break
            res["kind"] = kind
            self.count["tried"] += 1
            if res.get("ok"):
                self.count["ok"] += 1
                print("%s [+] 签到成功: %s" % (tag, json.dumps(res, ensure_ascii=False)[:300]))
                break
            if res.get("code") in (306, 308, 309):   # 不随时间变化，重试无意义
                print("%s [-] 硬失败 code=%s (%s)" % (tag, res.get("code"), res.get("msg")))
                break
            if i + 1 < max(1, self.a.repeat):
                print("%s [-] 第%d次未成功(%s)，%.1fs 后重试" %
                      (tag, i + 1, res.get("code") or res.get("msg"), self.a.interval))
                time.sleep(self.a.interval)
        if not res.get("ok"):
            print("%s [-] 未成功: %s" % (tag, json.dumps(res, ensure_ascii=False)[:300]))
        self.last = res
        if self.a.append_log:
            try:
                with open(os.path.expanduser(self.a.append_log), "a", encoding="utf-8") as f:
                    f.write(json.dumps({"t": time.strftime("%F %T"), "src": source,
                                        "content": content[:400], "res": res},
                                       ensure_ascii=False) + "\n")
            except OSError:
                pass
        return res


def mode_watch(a, signer):
    d = os.path.expanduser(a.watch)
    done = os.path.join(d, "_done")
    os.makedirs(done, exist_ok=True)
    print("[watch] 监视 %s （新文件里是二维码图片或二维码文本都行；处理完移到 _done/）" % d)
    while True:
        try:
            names = sorted(os.listdir(d))
        except OSError as e:
            print("[watch] 目录不可读:", e)
            names = []
        for n in names:
            p = os.path.join(d, n)
            if not os.path.isfile(p):
                continue
            time.sleep(0.15)                      # 等写完（截图工具可能分块落盘）
            try:
                if n.lower().endswith(IMG_EXT):
                    content = decode_qr_image(p)
                else:
                    content = open(p, encoding="utf-8", errors="ignore").read().strip()
            except Exception as e:
                print("[watch] 解析失败 %s: %s" % (n, e))
                content = None
            if content:
                signer.handle(content, source="watch:" + n)
            try:
                shutil.move(p, os.path.join(done, n))
            except OSError:
                pass
        time.sleep(max(0.3, a.interval))


def mode_stdin(a, signer):
    print("[stdin] 每行一段二维码内容（JSON / SIGNIN:... / URL），Ctrl-D 结束")
    for line in sys.stdin:
        signer.handle(line, source="stdin")


def mode_serve(a, signer):
    from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

    PORT = int(a.serve)
    TOKEN = a.token or ""

    PAGE = ("<html><meta charset=utf-8><body style='font:14px/1.6 monospace'>"
            "<h3>学习通签到中继</h3>"
            "<p>用手机/电脑打开下面任一形式即可把二维码喂进来：</p>"
            "<pre>GET  /sign?text=&lt;二维码原文，URL 编码&gt;&amp;token=%s\n"
            "POST /sign   body=二维码原文\n"
            "POST /image  body=&lt;二维码图片原始字节&gt;   （自动用 cv2 解码）\n"
            "GET  /last   查看最近一次结果\nGET  /stat   计数</pre>"
            "<p>提示：二维码里 c 每 10 秒变一次但 enc 不变，所以**发一次就够**，不必实时。</p>"
            "</body></html>") % TOKEN

    class H(BaseHTTPRequestHandler):
        def log_message(self, fmt, *args):
            print("[serve] " + (fmt % args))

        def _send(self, code, body, ctype="application/json; charset=utf-8"):
            b = body.encode("utf-8") if isinstance(body, str) else body
            self.send_response(code)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(b)))
            self.end_headers()
            self.wfile.write(b)

        def _token_ok(self, q):
            if not TOKEN:
                return True
            return (q.get("token", [""])[0] == TOKEN)

        def do_GET(self):
            u = urllib.parse.urlparse(self.path)
            q = urllib.parse.parse_qs(u.query)
            if u.path in ("/", "/index.html"):
                return self._send(200, PAGE, "text/html; charset=utf-8")
            if u.path == "/stat":
                return self._send(200, json.dumps(signer.count, ensure_ascii=False))
            if u.path == "/last":
                return self._send(200, json.dumps(signer.last, ensure_ascii=False))
            if u.path in ("/sign", "/qr"):
                if not self._token_ok(q):
                    return self._send(403, json.dumps({"error": "bad token"}))
                text = (q.get("text") or q.get("qr") or q.get("content") or [""])[0]
                if not text:
                    return self._send(400, json.dumps({"error": "need ?text="}, ensure_ascii=False))
                res = signer.handle(text, source="serve:" + self.client_address[0])
                return self._send(200, json.dumps(res, ensure_ascii=False))
            return self._send(404, json.dumps({"error": "not found"}))

        def do_POST(self):
            u = urllib.parse.urlparse(self.path)
            q = urllib.parse.parse_qs(u.query)
            if not self._token_ok(q):
                return self._send(403, json.dumps({"error": "bad token"}))
            n = int(self.headers.get("Content-Length") or 0)
            raw = self.rfile.read(n) if n else b""
            if u.path in ("/sign", "/qr"):
                try:
                    text = raw.decode("utf-8", "ignore")
                except Exception:
                    text = ""
                if not text.strip():
                    text = q.get("text", [""])[0]
                res = signer.handle(text, source="serve-post:" + self.client_address[0])
                return self._send(200, json.dumps(res, ensure_ascii=False))
            if u.path == "/image":
                try:
                    text = decode_qr_bytes(raw)
                except Exception as e:
                    return self._send(400, json.dumps({"error": str(e)}, ensure_ascii=False))
                res = signer.handle(text, source="serve-image:" + self.client_address[0])
                return self._send(200, json.dumps(res, ensure_ascii=False))
            return self._send(404, json.dumps({"error": "not found"}))

    srv = ThreadingHTTPServer(("127.0.0.1" if not a.host else a.host, PORT), H)
    print("[serve] 监听 http://%s:%d/  （token=%s）" %
          (a.host or "127.0.0.1", PORT, TOKEN or "(无，仅建议绑 127.0.0.1)"))
    print("[serve] 例: curl 'http://127.0.0.1:%d/sign?text=%%7B%%22signId%%22...&token=%s'" % (PORT, TOKEN))
    srv.serve_forever()


def main():
    ap = argparse.ArgumentParser(description="学习通远程扫码签到（无相机/无到场，支持动态二维码）")
    src = ap.add_mutually_exclusive_group(required=False)
    src.add_argument("--qr", help="二维码内容文本（JSON / SIGNIN:... / URL）")
    src.add_argument("--qr-image", help="二维码图片路径（png/jpg 截图）")
    src.add_argument("--qr-file", help="二维码内容所在文本文件")
    src.add_argument("--watch", help="监视目录：新出现的图片/文本自动解+签（动态二维码用）")
    src.add_argument("--serve", help="起中继 HTTP 服务，端口号，如 8765")
    src.add_argument("--stdin", action="store_true", help="从标准输入逐行读二维码内容")
    ap.add_argument("--uid", default="", help="你的 puid（学习通 uid）")
    ap.add_argument("--cookie", help="Cookie 字符串")
    ap.add_argument("--cookie-file", help="Cookie 文件（一行字符串 或 Netscape 格式）")
    ap.add_argument("--phone-id", default=None, help="phoneId（默认读 ~/.chaoxing_phone_id）")
    ap.add_argument("--name", default="", help="真实姓名（通道 C 需要）")
    ap.add_argument("--fid", default="0", help="学校 fid（通道 C）")
    ap.add_argument("--lat", default="-1")
    ap.add_argument("--lon", default="-1")
    ap.add_argument("--repeat", type=int, default=1, help="单个二维码的重试次数")
    ap.add_argument("--interval", type=float, default=2.0, help="重试间隔 / watch 轮询间隔（秒）")
    ap.add_argument("--token", default="", help="--serve 的访问口令（公网务必设置）")
    ap.add_argument("--host", default="", help="--serve 绑定地址（默认 127.0.0.1）")
    ap.add_argument("--append-log", default="", help="把每次结果追加到该文件（JSONL）")
    ap.add_argument("--dry-run", action="store_true", help="只打印将发出的请求，不提交")
    ap.add_argument("--stealth", action="store_true",
                    help="伪装层：设备档案一致 + 完整头 + 签到前掩护流量（推荐开）")
    ap.add_argument("--no-tls", action="store_true", help="关闭 curl_cffi 浏览器 TLS 指纹")
    ap.add_argument("--max-writes-per-hour", type=int, default=6,
                    help="每小时写配额（风控层，默认 6）")
    ap.add_argument("--min-interval", type=float, default=8.0, help="两次写最小间隔秒（默认 8）")
    ap.add_argument("--quiet-hours", default="1-7", help="静默时段 如 1-7；none 关闭（默认 1-7）")
    a = ap.parse_args()

    if not any([a.qr, a.qr_image, a.qr_file, a.watch, a.serve, a.stdin]):
        ap.error("至少要给 --qr / --qr-image / --qr-file / --watch / --serve / --stdin 之一")

    ck = load_cookie(a.cookie, a.cookie_file)
    if a.stealth and make_session:
        dev = Device.load_or_create(uid=a.uid)
        if a.phone_id:
            dev.phone_id = a.phone_id
            dev.save()
        sess = make_session(cookie=ck, device=dev, uid=a.uid, tls=not a.no_tls,
                            max_writes_per_hour=a.max_writes_per_hour,
                            min_interval=a.min_interval, quiet=parse_quiet(a.quiet_hours))
        print("[stealth] phoneId=%s  TLS=%s" % (dev.phone_id,
              "curl_cffi" if getattr(sess, "_cx_tls", False) else "requests"))
        print("[risk] 写配额 %d/小时，最小间隔 %.0fs，静默时段 %s" %
              (a.max_writes_per_hour, a.min_interval, a.quiet_hours))
        warmup(sess, uid=a.uid)
    else:
        sess = requests.Session()
        sess.headers.update({"User-Agent": UA, "Accept": "*/*",
                             "Accept-Language": "zh-CN,zh;q=0.9", "Connection": "keep-alive"})
    if ck:
        sess.headers["Cookie"] = ck
    else:
        print("[!] 没给 cookie，服务端会返回 309/未登录；请补 --cookie/--cookie-file")

    phid = a.phone_id or phone_id()
    uid = a.uid or os.environ.get("CHAOXING_UID", "")

    if a.dry_run:
        content = a.qr
        if a.qr_image:
            content = decode_qr_image(a.qr_image)
        elif a.qr_file:
            content = open(a.qr_file, encoding="utf-8").read().strip()
        print("[dry-run] uid=%s phoneId=%s cookie=%s" % (uid, phid, (ck[:60] + "...") if ck else "(none)"))
        if content:
            print("[dry-run] 内容:", content[:300])
            kind, obj = classify(content)
            print("[dry-run] 通道:", kind)
            if kind == "json":
                print("[dry-run] enc =", md5hex("%s-%s-%s-%s" % (obj.get("signId"), uid, obj.get("time"), phid)))
            elif kind == "url":
                q = urllib.parse.parse_qs(urllib.parse.urlparse(content).query)
                print("[dry-run] activeId=%s enc=%s" % ((q.get("id") or q.get("activeId") or [""])[0],
                                                        (q.get("enc") or [""])[0]))
        return

    if a.serve:
        return mode_serve(a, Signer(a, sess))
    signer = Signer(a, sess)
    if a.watch:
        return mode_watch(a, signer)
    if a.stdin:
        return mode_stdin(a, signer)

    content = a.qr
    if a.qr_image:
        content = decode_qr_image(a.qr_image)
    elif a.qr_file:
        content = open(a.qr_file, encoding="utf-8").read().strip()
    res = signer.handle(content, source="cli")
    sys.exit(0 if res.get("ok") else 1)


if __name__ == "__main__":
    main()
