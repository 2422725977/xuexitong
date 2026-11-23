# -*- coding: utf-8 -*-
"""★ 学生端常驻守护：只用学生 cookie —— 自动发现新签到 + 自动签「普通 / 位置」类。
   普通：activelist 发现 → 直接提交
   位置：getPPTActiveInfo 泄露的地址文本 → 地理编码起点 → 距离预言机爬坡 → 落进范围提交
   二维码：只能提示（需要 enc）；签到码/手势：只能提示（需要码值）
用法：
   python3 scripts/stu_guard.py --cookie-file ck.txt --uid [学生PUID] \
       --course-id 269282723 --class-id 159926750 --interval 12 --once
"""
import argparse, json, math, os, re, sys, time
import requests
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cx_pipeline as C

UA_APP = ('Mozilla/5.0 (Linux; Android 13; SM-G975F Build/TQ3A.230901.001) AppleWebKit/537.36 (KHTML, like Gecko) '
          'Version/4.0 Chrome/120.0.0.0 Mobile Safari/537.36 (schild:26f6a66da55ad239903fba6f674e8c66) (device:SM-G975F) '
          'Language/zh_CN com.ssreader.ChaoXingStudy/ChaoXingStudy_3_6_2_android_phone_20230101')
MOBILE = "https://mobilelearn.chaoxing.com"
RE_M = re.compile(r"距教师指定签到地点([0-9.Ee+-]+)米")
DONE = ("success", "success2", "您已签到过了")
CITY = {"北京": (39.9042, 116.4074), "成都": (30.5728, 104.0668), "上海": (31.2304, 121.4737),
        "重庆": (29.5630, 106.5516), "广州": (23.1291, 113.2644), "深圳": (22.5431, 114.0579),
        "天津": (39.0842, 117.2009), "武汉": (30.5928, 114.3055), "西安": (34.3416, 108.9398),
        "南京": (32.0603, 118.7969), "杭州": (30.2741, 120.1551), "长沙": (28.2282, 112.9388)}


class Guard:
    def __init__(self, cookie, uid, course, clazz, dry=False, do_location=True, log=print, risk=True):
        self.uid, self.course, self.clazz = uid, course, clazz
        self.dry, self.do_location, self.log = dry, do_location, log
        self.rc = None
        if risk:
            try:
                from risk_center import RiskCenter
                self.rc = RiskCenter(uid=str(uid or ""), optin=("sign_probe",))
            except Exception as e:
                self.log("      [风控] 策略层不可用：%s" % e)
        self.s = requests.Session()
        self.s.headers.update({"Cookie": cookie.strip(), "User-Agent": UA_APP})
        self.seen = set()
        self.stats = {"polled": 0, "new": 0, "signed": 0, "needs_secret": 0, "fail": 0}

    # ---------- 只读 ----------
    def activelist(self, show_not_started="0"):
        r = self.s.get(MOBILE + "/v2/apis/active/student/activelist",
                       params={"fid": "0", "courseId": self.course, "classId": self.clazz,
                               "showNotStartedActive": show_not_started, "_": str(int(time.time() * 1000))}, timeout=30)
        try:
            self.stats["polled"] += 1
            if self.rc and r.status_code == 200:
                self.rc.probe(MOBILE + "/v2/apis/active/student/activelist")   # R1 只读先行
            return (r.json().get("data") or {}).get("activeList") or []
        except Exception:
            return []

    def info(self, aid):
        try:
            return self.s.get(MOBILE + "/v2/apis/active/getPPTActiveInfo",
                              params={"activeId": aid}, timeout=25).json().get("data") or {}
        except Exception:
            return {}

    def classify(self, info):
        other = str(info.get("otherId") or "0")
        if str(info.get("ifphoto")) == "1" or other == "1":
            return "photo"
        if str(info.get("ifopenAddress")) == "1" or other == "4":
            return "location"
        return {"0": "normal", "2": "qr", "3": "gesture", "5": "code"}.get(other, "other")

    # ---------- 提交 ----------
    def submit(self, aid, action="sign_probe", **kw):
        """action: sign_probe（位置爬坡的一次探针，允许多次）/ sign（一次性提交，目标上限 3 次）"""
        p = {"activeId": aid, "courseId": self.course, "uid": self.uid, "clientip": "", "useragent": "",
             "latitude": "-1", "longitude": "-1", "appType": "0", "fid": "0", "name": ""}
        p.update(kw)
        url = MOBILE + "/pptSign/stuSignajax"
        if self.rc:
            ok, why = self.rc.allow(action, url=url, target=str(aid))
            if not ok and "R1" in why:
                self.activelist()                     # 自愈：补一次只读探针再试
                ok, why = self.rc.allow(action, url=url, target=str(aid))
            if not ok:
                if any(k in why for k in ("距上次", "小时", "今日", "冷却")):
                    ok, why = self.rc.wait(action, url=url, target=str(aid), max_wait=120, verbose=False)
            if not ok:
                self.log("      [风控] 拦截：%s" % why)
                return "RISK_BLOCKED:" + why, None
        r = self.s.get(url, params=p, timeout=25)
        b = r.text.strip()
        if self.rc:
            v = self.rc.observe(action, url, r.status_code, b, target=str(aid))
            if v["action"] in ("HALT", "COOLDOWN"):
                self.log("      [风控] %s → %s" % (v["action"], v["reason"][:80]))
        m = RE_M.search(b)
        return b, (float(m.group(1)) if m else None)

    def geocode(self, text):
        try:
            rr = requests.get("https://nominatim.openstreetmap.org/search",
                              params={"q": text.replace(" ", ""), "format": "json", "limit": 1},
                              headers={"User-Agent": "cx-research/1.0"}, timeout=20)
            j = rr.json()
            if j:
                return float(j[0]["lat"]), float(j[0]["lon"]), "nominatim"
        except Exception:
            pass
        for k, v in CITY.items():
            if k in text:
                return v[0], v[1], "city:" + k
        return None, None, "none"

    @staticmethod
    def hav(a, b, c, d, R=6371000.0):
        p1, p2 = math.radians(a), math.radians(c)
        dp = math.radians(c - a); dl = math.radians(d - b)
        x = math.sin(dp/2)**2 + math.cos(p1)*math.cos(p2)*math.sin(dl/2)**2
        return 2*R*math.asin(math.sqrt(x))

    def sign_location(self, aid, text, rounds=8):
        lat, lon, src = self.geocode(text or "")
        if lat is None:
            self.log("      [位置] 地址无法地理编码：%r" % text)
            return None
        self.log("      [位置] 起点 (%.6f, %.6f) via %s" % (lat, lon, src))
        for it in range(rounds):
            loc = json.dumps({"result": 1, "address": text, "longitude": round(lon, 12), "latitude": round(lat, 12)},
                             separators=(",", ":"))
            if self.dry:
                self.log("      [dry] 会提交 (%.6f, %.6f)" % (lat, lon)); return None
            body, d = self.submit(aid, location=loc, locationResult=loc)
            self.log("      [位置] #%d (%.6f, %.6f) d=%s -> %s" % (it, lat, lon, d, body[:48]))
            if any(k in body for k in DONE):
                return {"lat": lat, "lon": lon, "dist": d, "body": body, "rounds": it + 1}
            if d is None:
                return None
            dt = max(0.0005, min(0.05, d / 111000.0 * 0.25))
            _, da = self.submit(aid, location=json.dumps({"result": 1, "address": text, "longitude": round(lon, 12), "latitude": round(lat + dt, 12)}, separators=(",", ":")),
                                locationResult=json.dumps({"result": 1, "address": text, "longitude": round(lon, 12), "latitude": round(lat + dt, 12)}, separators=(",", ":")))
            _, db = self.submit(aid, location=json.dumps({"result": 1, "address": text, "longitude": round(lon + dt, 12), "latitude": round(lat, 12)}, separators=(",", ":")),
                                locationResult=json.dumps({"result": 1, "address": text, "longitude": round(lon + dt, 12), "latitude": round(lat, 12)}, separators=(",", ":")))
            if da is None or db is None:
                return None
            g_lat, g_lon = (da - d) / dt, (db - d) / dt
            n2 = g_lat * g_lat + g_lon * g_lon
            if n2 == 0:
                return None
            cap = max(0.02, d / 90000.0)
            lat += max(-cap, min(cap, -0.9 * d * g_lat / n2))
            lon += max(-cap, min(cap, -0.9 * d * g_lon / n2))
            time.sleep(0.3)
        return None

    # ---------- 主循环 ----------
    def scan_once(self):
        acts = self.activelist()
        fresh = []
        for a in acts:
            aid = str(a.get("id") or "")
            if not aid or aid in self.seen:
                continue
            if str(a.get("status")) != "1":
                continue
            self.seen.add(aid)
            fresh.append(aid)
        self.stats["new"] += len(fresh)
        for aid in fresh:
            info = self.info(aid)
            kind = self.classify(info)
            title = info.get("title") or info.get("typeTitle") or ""
            self.log("  [发现] aid=%s kind=%-8s title=%r" % (aid, kind, title))
            if kind == "normal":
                if self.dry:
                    self.log("      [dry] 会直接提交"); continue
                body, _ = self.submit(aid)
                self.log("      [普通] -> %s" % body[:60])
                if any(k in body for k in DONE): self.stats["signed"] += 1
                else: self.stats["fail"] += 1
            elif kind == "location":
                if not self.do_location:
                    self.log("      [位置] 已按参数跳过"); self.stats["needs_secret"] += 1; continue
                r = self.sign_location(aid, (info.get("locationText") or "").strip())
                if r: self.stats["signed"] += 1
                else: self.stats["fail"] += 1
            elif kind == "qr":
                self.log("      [二维码] 需要 enc：贴一张码截图到 --qr-dir 或让人报 enc（静态码一张图永久有效）")
                self.stats["needs_secret"] += 1
            elif kind in ("code", "gesture"):
                self.log("      [%s] 需要码值（读不到；6 次错锁 1 小时）" % ("签到码" if kind == "code" else "手势"))
                self.stats["needs_secret"] += 1
            else:
                self.log("      [%s] 暂不支持（拍照/人脸类）" % kind)
                self.stats["needs_secret"] += 1
        return len(fresh)

    def run(self, interval=12, max_seconds=0, once=False):
        t0 = time.time()
        while True:
            try:
                n = self.scan_once()
                self.log("[guard] 轮询 activelist：新活动 %d 个；累计 已签=%d 需人工=%d 失败=%d"
                         % (n, self.stats["signed"], self.stats["needs_secret"], self.stats["fail"]))
            except Exception as e:
                self.log("[guard] 异常：%s" % e)
            if once:
                break
            if max_seconds and time.time() - t0 > max_seconds:
                break
            time.sleep(interval)
        return self.stats


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cookie-file", default="ck.txt")
    ap.add_argument("--cookie")
    ap.add_argument("--uid", default="")
    ap.add_argument("--course-id", default="")
    ap.add_argument("--class-id", default="")
    ap.add_argument("--interval", type=float, default=12)
    ap.add_argument("--max-seconds", type=float, default=0)
    ap.add_argument("--once", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--no-location", action="store_true")
    ap.add_argument("--log", default="")
    ap.add_argument("--no-risk-center", action="store_true",
                    help="关闭反封号策略层（默认开启：只读先行/双配额/目标上限/熔断/审计）")
    a = ap.parse_args()
    cookie = a.cookie or open(a.cookie_file, encoding="utf-8").read()
    if not a.uid or not a.course_id or not a.class_id:
        print("需要 --uid --course-id --class-id（可从 ck.txt/页面里取）"); sys.exit(2)
    fh = open(a.log, "a", encoding="utf-8") if a.log else None
    def log(msg):
        line = "[%s] %s" % (time.strftime("%H:%M:%S"), msg); print(line)
        if fh: fh.write(line + chr(10)); fh.flush()
    g = Guard(cookie, a.uid, a.course_id, a.class_id, dry=a.dry_run, do_location=not a.no_location,
              log=log, risk=not getattr(a, "no_risk_center", False))
    st = g.run(interval=a.interval, max_seconds=a.max_seconds, once=a.once)
    log("[guard] 结束 %s" % json.dumps(st, ensure_ascii=False))


if __name__ == "__main__":
    main()
