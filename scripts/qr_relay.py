#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
qr_relay.py - 动态二维码「秒级中继」：自动从屏幕/ADB 截图里解二维码，一旦解码成功立刻签到

场景: 教室大屏二维码每 10 秒刷一次（其实只有显示计数 c 在变，enc 全程固定）。
      人工截图再转发有 10~60 秒延迟，这个脚本把「看屏幕 -> 解码 -> 提交」压到 <1 秒。

三种取屏方式:
  1) --source adb     用 adb exec-out screencap 抓**另一台**设备/模拟器屏幕（本机 AVD cx29 就绪）
  2) --source screen  抓本机 macOS 屏幕（需要 brew install imagesnap? 不，用 screencapture -x，内置）
  3) --source loop-dir 指定一个目录，外部工具往里面丢图（Syncthing / 相册同步 / 微信文件夹）

行为:
  - 每次取屏 -> cv2 解二维码 -> 内容是新的就 (a) 先本地算 enc 直接提交（--submit），
    或 (b) 只 POST 给你的 relay（--relay http://127.0.0.1:8765/sign?token=...）
  - 解码失败静默继续（大屏闪烁/反光很正常）；成功签到后 --stop-on-success
  - 二维码内容去重（同 enc 不重复提交）

用法:
  # 最省事：本机 AVD 里放着学习通/浏览器，直接抓它
  python3 qr_relay.py --source adb --serial emulator-5554 --submit \
      --uid 12345678 --cookie-file ck.txt --interval 0.7 --stop-on-success

  # 大屏很近、想用电脑摄像头/截屏
  python3 qr_relay.py --source screen --submit --uid 12345678 --cookie-file ck.txt

  # 把解出的内容转给你已有的 relay 服务（另一台机器在签）
  python3 qr_relay.py --source adb --relay 'http://127.0.0.1:8765/sign?token=mysecret'
"""
import argparse, hashlib, json, os, subprocess, sys, tempfile, time, urllib.parse

try:
    import requests
except ImportError:
    sys.exit("need: pip install requests")


def grab_adb(serial):
    cmd = ["adb"]
    if serial:
        cmd += ["-s", serial]
    cmd += ["exec-out", "screencap", "-p"]
    out = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=20)
    if out.returncode != 0:
        raise RuntimeError("adb screencap 失败: " + out.stderr.decode("utf-8", "ignore")[:200])
    return out.stdout


def grab_screen_macos():
    """macOS 自带 screencapture；-x 静音"""
    fd, path = tempfile.mkstemp(suffix=".png")
    os.close(fd)
    subprocess.run(["screencapture", "-x", path], check=True, timeout=20)
    data = open(path, "rb").read()
    os.unlink(path)
    return data


def decode_qr_bytes(data):
    try:
        import cv2
    except ImportError:
        sys.exit("need: pip install opencv-python-headless")
    import numpy as np
    arr = cv2.imdecode(np.frombuffer(data, dtype="uint8"), cv2.IMREAD_COLOR)
    if arr is None:
        return None
    det = cv2.QRCodeDetector()
    ok, texts, _, _ = det.detectAndDecodeMulti(arr)
    if ok and texts:
        for t in texts:
            if t and t.strip():
                return t.strip()
    t, _, _ = det.detectAndDecode(arr)
    return t.strip() if t else None


def build_submit_url(content, uid, phid, name, fid):
    """复用 qr_sign_remote 的通道判定，但只算 URL，便于打印与 --relay 分离"""
    import importlib.util
    here = os.path.dirname(os.path.abspath(__file__))
    spec = importlib.util.spec_from_file_location("qsr", os.path.join(here, "qr_sign_remote.py"))
    qsr = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(qsr)
    return qsr, qsr.classify(content)


def main():
    ap = argparse.ArgumentParser(description="动态二维码秒级中继：截屏→解码→签到")
    ap.add_argument("--source", choices=["adb", "screen", "loop-dir"], default="adb")
    ap.add_argument("--serial", default="", help="adb 设备序列号，如 emulator-5554")
    ap.add_argument("--dir", default="", help="--source loop-dir 时监视的目录")
    ap.add_argument("--interval", type=float, default=0.8, help="取屏间隔秒")
    ap.add_argument("--submit", action="store_true", help="解出后本机直接提交签到")
    ap.add_argument("--relay", default="", help="改为把内容 POST 给中继服务 URL")
    ap.add_argument("--uid", default="", help="puid（--submit 用）")
    ap.add_argument("--cookie", default="", help="Cookie 字符串（--submit 用）")
    ap.add_argument("--cookie-file", default="", help="Cookie 文件（--submit 用）")
    ap.add_argument("--name", default="")
    ap.add_argument("--fid", default="0")
    ap.add_argument("--repeat", type=int, default=1)
    ap.add_argument("--stop-on-success", action="store_true")
    ap.add_argument("--verbose", action="store_true", help="解码失败也打印一行")
    a = ap.parse_args()

    qsr = signer = sess = None
    if a.submit:
        if not (a.relay or a.submit):
            ap.error("--submit 或 --relay 至少给一个")
        qsr, _ = build_submit_url("", a.uid, "", a.name, a.fid)
        sess = requests.Session()
        sess.headers.update({"User-Agent": qsr.UA})
        ck = qsr.load_cookie(a.cookie, a.cookie_file)
        if ck:
            sess.headers["Cookie"] = ck
        ns = type("NS", (), {})()
        ns.phone_id = None
        ns.uid = a.uid or os.environ.get("CHAOXING_UID", "")
        ns.name = a.name
        ns.fid = a.fid
        ns.lat, ns.lon = "-1", "-1"
        ns.repeat = a.repeat
        ns.interval = 0.5
        ns.append_log = ""
        signer = qsr.Signer(ns, sess)

    seen, n_try, t0 = set(), 0, time.time()
    print("[*] 开始取屏: source=%s interval=%.2fs submit=%s relay=%s" % (a.source, a.interval, a.submit, a.relay or "-"))
    while True:
        try:
            if a.source == "adb":
                data = grab_adb(a.serial)
            elif a.source == "screen":
                data = grab_screen_macos()
            else:
                names = [n for n in sorted(os.listdir(a.dir))
                         if n.lower().endswith((".png", ".jpg", ".jpeg", ".webp", ".bmp"))]
                if not names:
                    time.sleep(a.interval)
                    continue
                p = os.path.join(a.dir, names[-1])
                data = open(p, "rb").read()
                os.rename(p, p + ".used")
        except Exception as e:
            print("[!] 取屏失败:", e)
            time.sleep(max(1.0, a.interval))
            continue

        n_try += 1
        content = decode_qr_image_safe(data)
        if not content:
            if a.verbose:
                print("[.] 第%d帧未解出（%.1fs）" % (n_try, time.time() - t0))
            time.sleep(a.interval)
            continue
        key = hashlib.sha1(content.encode("utf-8", "ignore")).hexdigest()
        if key in seen:
            time.sleep(a.interval)
            continue
        seen.add(key)
        print("[+] 第%d帧解出（%.2fs）: %s" % (n_try, time.time() - t0, content[:220]))

        ok = False
        if a.relay:
            try:
                r = requests.post(a.relay, data=content.encode("utf-8"), timeout=15,
                                  headers={"Content-Type": "text/plain"})
                print("    relay -> HTTP %s %s" % (r.status_code, r.text[:200]))
                ok = r.status_code == 200 and '"ok": true' in r.text.replace('"ok":true', '"ok": true')
            except Exception as e:
                print("    relay 失败:", e)
        if a.submit and not ok:
            res = signer.handle(content, source="relay-src")
            ok = bool(res.get("ok"))
        if ok and a.stop_on_success:
            print("[*] 签到成功，退出")
            return
        time.sleep(a.interval)


def decode_qr_image_safe(data):
    try:
        return decode_qr_bytes(data)
    except Exception as e:
        if os.environ.get("QR_RELAY_DEBUG"):
            print("[!] decode error:", e)
        return None


if __name__ == "__main__":
    main()
