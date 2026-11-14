#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
stealth_session.py - 学习通请求「像客户端」化的一层：设备档案一致性 + 完整头 + 拟人延迟 + 掩护流量。

为什么需要：
  6.7.8 解壳后可确认客户端有两条服务端可见的旁证链：
    1) com.chaoxing.mobile.s.Oa()  ->  https://data-xxt.aichaoxing.com/analysis/ac_event
       ?state=<事件>&userId=<puid>&request_path=<页面/接口>&time=<秒>&enc=<md5>
       即「App 在界面上发生了什么」会被单独上报到行为分析域；
    2) assets/RiskStub.dex（梆梆 everisk 风控 SDK，541 类）在 Application 阶段就起来跑设备/行为采集。
  纯协议提交没有这两条旁证。因此把「请求本身」做干净（头、顺序、时序、指纹）成本最低、收益最直接。

提供:
  Device           设备档案（uid / phoneId / UA / schild / 分辨率…），可持久化，保证多次运行同一指纹
  make_session()   带全套头的 requests.Session（装了 curl_cffi 则用浏览器 TLS 指纹）
  human_delay()    3–30s 拟人延迟
  warmup()         提交前后打「学习流量」：课程列表 / 消息 / 任务点，制造正常使用痕迹
  explain()        把签到响应翻译成"这一步是被登录挡了还是被风控挡了"

用法（作为库）:
    from stealth_session import make_session, Device, warmup, human_delay
    dev = Device.load_or_create(uid="12345678")
    s = make_session(cookie=ck, device=dev)
    warmup(s)                      # 先读后写
    human_delay()                  # 再等几秒
    # ... 正常提交签到 ...

自检:
    python3 stealth_session.py --show
    python3 stealth_session.py --probe https://mobilelearn.chaoxing.com/
"""
import argparse, hashlib, json, os, random, re, sys, time

try:
    import requests
except ImportError:
    sys.exit("need: pip install requests")

try:  # 有 curl_cffi 就用它的浏览器 TLS 指纹（JA3 与 Chrome 一致）
    from curl_cffi import requests as cffi_requests
    HAVE_CFFI = True
except Exception:
    HAVE_CFFI = False

PROFILE_PATH = os.path.expanduser("~/.chaoxing_device.json")

UA_TPL = ("Mozilla/5.0 (Linux; Android {av}; {model} Build/{build}; wv) "
          "AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/{chrome} "
          "Mobile Safari/537.36 (schild:{schild}) (device:{model}) "
          "Language/zh-CN com.chaoxing.mobile/ChaoXingStudy_{vc}")

DEVICES = [
    ("13", "SM-S9180", "TP1A.220624.014", "114.0.0.0"),
    ("12", "2201122C", "SKQ1.211006.001", "108.0.0.0"),
    ("14", "PGT110", "UKQ1.230924.001", "120.0.0.0"),
    ("13", "V2227A", "TP1A.220624.014", "116.0.0.0"),
]

READS = [  # 掩护流量：只看读接口（可写绝对 URL）
    "https://mooc1-api.chaoxing.com/mycourse/backclazzdata?view=json&rss=1",
    "https://mobilelearn.chaoxing.com/ppt/activeAPI/courseactivelist?status=1&page=1&pageSize=20",
    "https://mobilelearn.chaoxing.com/teachingPlanAPI/noFinishActiveCount?chatId=&tuid={uid}",
    "https://mobilelearn.chaoxing.com/ppt/activeAPI/personalActiveLibraryV2?page=1&pageSize=20",
]


def d5(s):
    return hashlib.md5(s.encode("utf-8", "ignore")).hexdigest()


class Device:
    """一套自洽的设备指纹。同一 uid 永远配同一个 phoneId/UA，否则服务端侧两个指纹会打架。"""

    def __init__(self, uid="", phone_id="", ua="", schild="00000000", vc="10946", model="SM-S9180"):
        self.uid = uid
        self.phone_id = phone_id or d5("cx-" + str(random.random()))[:32]
        self.schild = schild
        self.vc = vc
        self.model = model
        self.ua = ua or UA_TPL.format(av="13", model=model, build="TP1A.220624.014",
                                      chrome="114.0.0.0", schild=schild, vc=vc)

    def to_dict(self):
        return {"uid": self.uid, "phone_id": self.phone_id, "ua": self.ua,
                "schild": self.schild, "vc": self.vc, "model": self.model}

    @classmethod
    def from_dict(cls, d):
        return cls(**{k: d.get(k, "") for k in ("uid", "phone_id", "ua", "schild", "vc", "model")})

    @classmethod
    def load_or_create(cls, uid="", path=PROFILE_PATH):
        if os.path.exists(path):
            try:
                d = json.load(open(path, encoding="utf-8"))
                dev = cls.from_dict(d)
                if uid:
                    dev.uid = uid
                return dev
            except Exception:
                pass
        av, model, build, chrome = random.choice(DEVICES)
        dev = cls(uid=uid, model=model,
                  ua=UA_TPL.format(av=av, model=model, build=build, chrome=chrome,
                                   schild="00000000", vc="10946"))
        dev.save(path)
        return dev

    def save(self, path=PROFILE_PATH):
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(self.to_dict(), f, ensure_ascii=False, indent=2)
        except Exception:
            pass


def base_headers(device, referer=None, xhr=False):
    h = {
        "User-Agent": device.ua,
        "Accept": "*/*",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
        "Referer": referer or "https://mobilelearn.chaoxing.com/",
    }
    if xhr:
        h["X-Requested-With"] = "com.chaoxing.mobile"
    return h


def make_session(cookie=None, device=None, uid="", referer=None, impersonate="chrome120",
                 tls=True, xhr=False, proxy=None):
    """返回一个「长得像 App」的会话。装了 curl_cffi 且 tls=True 时启用浏览器 TLS 指纹。"""
    device = device or Device.load_or_create(uid=uid)
    use_cffi = HAVE_CFFI and tls
    sess = cffi_requests.Session(impersonate=impersonate) if use_cffi else requests.Session()
    sess.headers.update(base_headers(device, referer=referer, xhr=xhr))
    if cookie:
        sess.headers["Cookie"] = cookie.strip()
    sess._cx_device = device          # 挂上档案，方便 warmup/日志引用
    sess._cx_tls = use_cffi
    if proxy:
        sess.proxies = {"http": proxy, "https": proxy}
    return sess


def human_delay(lo=3.0, hi=30.0, quiet=False):
    """签到场景的拟人延迟。0 秒提交是最显眼的异常特征之一。"""
    s = random.uniform(lo, hi)
    if not quiet:
        print("[stealth] 拟人延迟 %.1fs" % s)
    time.sleep(s)
    return s


def warmup(sess, base="https://mobilelearn.chaoxing.com", uid="", paths=None, quiet=False):
    """先读后写：签到前先产生几次正常浏览请求，降低"只会写接口"的可疑度。"""
    dev = getattr(sess, "_cx_device", None)
    uid = uid or (dev.uid if dev else "")
    paths = paths or READS
    out = []
    for p in paths:
        url = (p if p.startswith("http") else base + p).replace("{uid}", str(uid))
        try:
            r = sess.get(url, timeout=20)
            out.append((r.status_code, len(r.content), p))
            if not quiet:
                print("[stealth] warmup %s -> %s %dB" % (p, r.status_code, len(r.content)))
        except Exception as e:
            out.append(("ERR", str(e)[:60], p))
            if not quiet:
                print("[stealth] warmup %s -> ERR %s" % (p, str(e)[:80]))
        time.sleep(random.uniform(1.5, 4.0))
    return out


RISK_HINTS = [
    ("请先登录", "未登录：cookie 缺失/过期或不是学习通域下的会话 cookie（pid/uf/p_uid 那条）"),
    ("success", "提交被接受"),
    ("statusCode", "通道 A 的 JSON 回包，看 statusCode：300 成功 / 306 enc 错 / 307 二维码过期 / 308 signId 不存在"),
]


def explain(body, status=None):
    b = (body or "")[:400]
    for k, v in RISK_HINTS:
        if k in b:
            return v
    if status == 403:
        return "403：网关/WAF 层拦了（多半是头或频率）"
    return "未识别回包，原文：%s" % b


def probe(url="https://mobilelearn.chaoxing.com/", uid="", cookie=None, tls=True):
    dev = Device.load_or_create(uid=uid)
    s = make_session(cookie=cookie, device=dev, tls=tls)
    r = s.get(url, timeout=25)
    print("设备档案: %s" % json.dumps(dev.to_dict(), ensure_ascii=False)[:200])
    print("TLS 指纹: %s" % ("curl_cffi(chrome)" if getattr(s, "_cx_tls", False) else "requests(默认)"))
    print("HTTP %s  %d bytes" % (r.status_code, len(r.content)))
    print("解读: %s" % explain(r.text, r.status_code))
    return r


def main():
    ap = argparse.ArgumentParser(description="学习通请求伪装层（设备档案/头/延迟/掩护流量）")
    ap.add_argument("--show", action="store_true", help="打印当前设备档案")
    ap.add_argument("--new-device", action="store_true", help="重新生成设备档案")
    ap.add_argument("--uid", default="")
    ap.add_argument("--probe", nargs="?", const="https://mobilelearn.chaoxing.com/",
                    help="探测一个 URL，看头/TLS/回包解读")
    ap.add_argument("--warmup", action="store_true", help="跑一遍掩护流量")
    ap.add_argument("--cookie", default=None)
    ap.add_argument("--no-tls", action="store_true", help="不用 curl_cffi TLS 指纹")
    a = ap.parse_args()

    if a.new_device:
        dev = Device(uid=a.uid)
        dev.save()
        print("已生成:", json.dumps(dev.to_dict(), ensure_ascii=False))
        return
    if a.show:
        dev = Device.load_or_create(uid=a.uid)
        print(json.dumps(dev.to_dict(), ensure_ascii=False, indent=2))
        print("TLS 可用:", HAVE_CFFI)
        return
    if a.warmup:
        s = make_session(cookie=a.cookie, uid=a.uid, tls=not a.no_tls)
        warmup(s, uid=a.uid)
        return
    if a.probe:
        probe(a.probe, uid=a.uid, cookie=a.cookie, tls=not a.no_tls)
        return
    ap.print_help()


if __name__ == "__main__":
    main()
