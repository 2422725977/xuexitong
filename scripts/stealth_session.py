#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
stealth_session.py v2 —— 学习通「伪装层 + 风控层」。

目标：让协议提交在**服务端可见的每一个维度**上都与真实 App 的同类请求不可区分，
并在出现风控信号时**自己先停手**（避免从"可疑"升级为"被处置"）。

六个维度（v2 全覆盖）：
  1) 身份一致性  Device：uid <-> phoneId <-> UA <-> 机型/系统 永久绑定，改一个就报错
  2) 传输层指纹  TLS/JA3 + HTTP2：curl_cffi impersonate=chrome*；失败自动降级并告警
  3) 头部与语言  UA 用 App 真实的 okhttp/4.12.0（native 接口）或 WebView UA（H5 容器），
                 加 X-Requested-With / Referer 链 / Accept-Language，不用 Python 默认头
  4) 时序与频率  Token bucket + 最小间隔 + 每小时/每日写上限 + 静默时段 + 高斯抖动
                 （"0 秒提交"和"整点整分提交"是最显眼的两个特征）
  5) 流量形态    写操作前后穿插只读学习请求（上课流程：看课表 -> 看活动 -> 签到 -> 看任务点）
  6) 风控熔断    RiskGuard 对每个响应判级；SOFT 累积进入冷却，HARD 立刻停机并要求人工确认

用法（库）：
    from stealth_session import StealthSession, Device
    dev = Device.load_or_create(uid="12345678")          # 档案永久
    ss  = StealthSession(cookie=ck, device=dev, uid="12345678", guard=True)
    ss.warmup()                                          # 先读后写
    r = ss.get("https://mobilelearn.chaoxing.com/pptSign/stuSignajax?...")
    print(ss.explain(r))                                 # 这次是被登录挡了还是被风控挡了

自检 / 运维：
    python3 stealth_session.py --doctor                  # 六维体检（推荐先跑）
    python3 stealth_session.py --show                    # 当前设备档案
    python3 stealth_session.py --new-device --uid UID
    python3 stealth_session.py --simulate 6              # 干跑 6 次提交，打印时序表（不联网）
    python3 stealth_session.py --probe URL --cookie ck
    python3 stealth_session.py --warmup --cookie ck
    python3 stealth_session.py --risk                    # 风控状态
    python3 stealth_session.py --reset-risk              # 清空冷却/停机
    python3 stealth_session.py --audit 20                # 最近 20 条审计

审计：~/.chaoxing_audit.jsonl（每次请求一行，参数值脱敏）
限速：~/.chaoxing_rate.json（写操作的滑动窗口）
风控：~/.chaoxing_risk.json（strikes / cooldown / halt）
档案：~/.chaoxing_device.json（uid<->phoneId<->UA）
"""
import argparse, hashlib, json, os, random, re, statistics, sys, time
from datetime import datetime, time as dtime

try:
    import requests
except ImportError:
    sys.exit("need: pip install requests")

try:  # 有 curl_cffi 就用它的浏览器 TLS 指纹（JA3 与 Chrome 一致）
    from curl_cffi import requests as cffi_requests
    HAVE_CFFI = True
except Exception:
    HAVE_CFFI = False

HOME = os.path.expanduser("~")
PROFILE_PATH = os.path.join(HOME, ".chaoxing_device.json")
RATE_PATH = os.path.join(HOME, ".chaoxing_rate.json")
RISK_PATH = os.path.join(HOME, ".chaoxing_risk.json")
AUDIT_PATH = os.path.join(HOME, ".chaoxing_audit.jsonl")

APP_NAME = "com.chaoxing.mobile"
APP_VER = "6.7.8"
APP_VC = "10946"
OKHTTP_UA = "okhttp/4.12.0"          # 载荷里的真实 OkHttp 版本：okhttp/4.12.0
SCHEMA = 2                      # 档案版本：<2 的旧档案会自动迁移（保留 phoneId，重建自洽的其余字段）

# WebView UA 模板来自解壳字符串池原文：
#   Mozilla/5.0 (Linux; U; Android %s) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 %sSafari/533.1
WEBVIEW_UA_TPL = ("Mozilla/5.0 (Linux; U; Android {av}) AppleWebKit/533.1 (KHTML, like Gecko) "
                  "Version/4.0 {token}Safari/533.1")
WEBVIEW_TOKEN = "ChaoXingStudy_{vc}"      # App 自己用的 token 形态

# 机型池：与 UA/系统版本自洽（同一份档案里不允许出现矛盾组合）
DEVICES = [
    dict(brand="Xiaomi", model="2201122C", android="12", sdk="31", build="SKQ1.211006.001", chrome="108.0.0.0"),
    dict(brand="samsung", model="SM-S9180", android="13", sdk="33", build="TP1A.220624.014", chrome="114.0.0.0"),
    dict(brand="HONOR", model="PGT-AN10", android="13", sdk="33", build="HONORPGT-AN10", chrome="112.0.0.0"),
    dict(brand="OPPO", model="PGT110", android="14", sdk="34", build="UKQ1.230924.001", chrome="120.0.0.0"),
    dict(brand="vivo", model="V2227A", android="13", sdk="33", build="TP1A.220624.014", chrome="116.0.0.0"),
    dict(brand="HUAWEI", model="ELS-AN00", android="12", sdk="31", build="HUAWEIELS-AN00", chrome="110.0.0.0"),
]

# 只读掩护流量（学习动线，可写绝对 URL）
COVER_FLOW = [
    "https://mooc1-api.chaoxing.com/mycourse/backclazzdata?view=json&rss=1",
    "https://mobilelearn.chaoxing.com/ppt/activeAPI/courseactivelist?status=1&page=1&pageSize=20",
    "https://mobilelearn.chaoxing.com/teachingPlanAPI/noFinishActiveCount?chatId=&tuid={uid}",
    "https://mobilelearn.chaoxing.com/ppt/activeAPI/personalActiveLibraryV2?page=1&pageSize=20",
    "https://mobilelearn.chaoxing.com/ppt/activeAPI/courseactivecount?puid={uid}&source=15",
]

# 写操作识别（命中即视为"会产生服务端状态变化"的请求，受限速与风控熔断约束）
WRITE_HINTS = (
    "addsign", "stusignajax", "studentsign", "signin", "gotasksign", "presign",
    "savebegin", "savediscuss", "preAddVote".lower(), "goqvote", "createtaskanswer",
    "sendnotice", "restartactive", "publishactivenotice", "submit", "upload",
    "saverecord", "addscore", "verify", "addsignlog", "sync",
)

# ---------------- 风控信号表 ----------------
# level: HALT 立刻停机 / COOLDOWN 冷却 / WARN 记录并继续 / NOTICE 业务错误（非风控）
RISK_SIGNALS = [
    (re.compile(r"请先登录|未登录|登录已过期|登录失效|重新登录|login\s*required|not\s*login", re.I),
     "HALT", "登录态失效：必须先用真机/真登录刷新 cookie，不能继续硬试"),
    (re.compile(r"验证码|captcha|人机|滑块|安全验证|二次验证|SecVerify|secVerify", re.I),
     "HALT", "出现验证码/人机校验：服务端已把这次行为判为异常，停机并换人工流程"),
    (re.compile(r"账号异常|风险|riskControl|风控|受限|封禁|冻结", re.I),
     "HALT", "账号被风控标记：停机，检查是否触发了频率或设备异常规则"),
    (re.compile(r"403 Forbidden|Access Denied", re.I), "HALT", "网关/WAF 层拦截：头或频率有问题，先停下看审计"),
    (re.compile(r"操作频繁|过于频繁|请求频繁|限流|too\s*many|rate\s*limit|请求过快", re.I),
     "COOLDOWN", "限流：降频冷却后再试"),
    (re.compile(r"系统繁忙|服务器忙|服务不可用|503|502|504", re.I), "WARN", "服务端抖动：退避重试"),
    # 业务错误（不是风控，不要误判成"被发现"）
    (re.compile(r"statusCode\"*\s*:\s*(30[1-9]|31[0-2])", re.I), "NOTICE", "通道 A 业务码 301/306-312：签到参数或状态问题"),
    (re.compile(r"二维码.*过期|signId\s*not\s*exists|签到id不存在", re.I), "NOTICE", "二维码过期/签到 id 不存在：重新取码即可"),
    (re.compile(r"success|statusCode\"*\s*:\s*300|签到成功|恭喜", re.I), "OK", "提交被接受"),
]


def now_ts():
    return time.time()


def d5(s):
    return hashlib.md5(str(s).encode("utf-8", "ignore")).hexdigest()


def parse_quiet(s):
    """把 CLI 字符串解析成静默时段元组。

    '1-7' → (1, 7)；'22-6' → (22, 6)（跨零点）；'' / 'none' / 'off' → None（不静默）。
    默认 (1, 7)：凌晨 1-7 点不写 —— 真人这个点不签到，凌晨爬起来签到本身就是特征。
    """
    if s is None:
        return (1, 7)
    t = str(s).strip().lower()
    if t in ("", "none", "off", "no", "null", "-"):
        return None
    m = re.match(r"^(\d{1,2})\s*[-~,]\s*(\d{1,2})$", t)
    if not m:
        raise ValueError("静默时段格式应为 START-END（如 1-7）或 none，收到 %r" % s)
    a, b = int(m.group(1)), int(m.group(2))
    if not (0 <= a <= 23 and 0 <= b <= 24):
        raise ValueError("静默时段小时需在 0-24，收到 %r" % s)
    if a == b:
        return None
    return (a, b)


def in_quiet_hours(quiet):
    """quiet=(start_hour, end_hour)：跨零点也支持。静默时段不做写操作。"""
    if not quiet:
        return False
    h = datetime.now().hour
    a, b = quiet
    return (a <= h < b) if a <= b else (h >= a or h < b)


def redact(url):
    """审计脱敏：保留参数名，抹掉可疑值（rcode/enc/signId/token/cookie 类）。"""
    try:
        u, _, q = url.partition("?")
        if not q:
            return u
        keep, out = ("uid", "status", "page", "type", "view", "activeId", "activePrimaryId", "courseId", "classId"), []
        for kv in q.split("&"):
            k, _, v = kv.partition("=")
            if k in keep:
                out.append(kv)
            elif len(v) > 6:
                out.append(k + "=" + v[:3] + "***")
            else:
                out.append(kv)
        return u + "?" + "&".join(out)
    except Exception:
        return url[:120]


class RiskHalt(RuntimeError):
    """风控 HALT：立刻停机，不要重试（重试会把"可疑"变成"被处置"）。"""

    def __init__(self, msg, response=None, verdict=None):
        super().__init__(msg)
        self.response = response
        self.verdict = verdict


class RiskCooldown(RuntimeError):
    """风控限流：进入冷却，冷却结束或人工确认后再来。"""

    def __init__(self, msg, response=None, verdict=None):
        super().__init__(msg)
        self.response = response
        self.verdict = verdict


class Device:
    """一套自洽的设备指纹。同一 uid 永久配同一个 phoneId/UA/机型，否则服务端会看到两个指纹。"""

    FIELDS = ("uid", "phone_id", "ua", "webview_ua", "schild", "vc", "model", "brand",
              "android", "sdk", "build", "chrome", "created")

    def __init__(self, uid="", phone_id="", ua="", webview_ua="", schild="00000000", vc=APP_VC,
                 model="SM-S9180", brand="samsung", android="13", sdk="33",
                 build="TP1A.220624.014", chrome="114.0.0.0", created=None, **kw):
        self.uid = str(uid or "")
        self.phone_id = phone_id or d5("cx-" + os.urandom(16).hex())[:32]   # 32 位 hex，与 App 缺省一致
        self.vc = str(vc)
        self.schild = schild
        self.model, self.brand = model, brand
        self.android, self.sdk, self.build, self.chrome = android, sdk, build, chrome
        self.ua = ua or OKHTTP_UA
        self.webview_ua = webview_ua or WEBVIEW_UA_TPL.format(av=android, token=WEBVIEW_TOKEN.format(vc=self.vc))
        self.created = created or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        d = {k: getattr(self, k) for k in self.FIELDS}
        d["schema"] = SCHEMA
        return d

    @classmethod
    def from_dict(cls, d):
        return cls(**{k: d.get(k, "") for k in cls.FIELDS if k in d})

    @classmethod
    def load_or_create(cls, uid="", path=PROFILE_PATH, rotate=False):
        if os.path.exists(path) and not rotate:
            try:
                raw = json.load(open(path, encoding="utf-8"))
                dev = cls.from_dict(raw)
                if raw.get("schema") != SCHEMA:
                    dev = cls.migrate(dev)
                if uid and dev.uid != str(uid):
                    # 换 uid 不等于换设备：保留 phoneId，只换账号（这才是真人的行为）
                    dev.uid = str(uid)
                dev.save(path)
                return dev
            except Exception:
                pass
        d = random.choice(DEVICES)
        dev = cls(uid=uid, **d)
        dev.save(path)
        return dev

    def save(self, path=PROFILE_PATH):
        try:
            os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
            with open(path, "w", encoding="utf-8") as f:
                json.dump(self.to_dict(), f, ensure_ascii=False, indent=2)
            os.chmod(path, 0o600)
        except Exception:
            pass

    @classmethod
    def migrate(cls, dev):
        """旧档案升级：phoneId/uid 保留（身份延续），UA/机型/系统版本重建为自洽组合。"""
        pool = [d for d in DEVICES if d["model"] == dev.model] or [random.choice(DEVICES)]
        d = pool[0]
        dev.brand, dev.model = d["brand"], d["model"]
        dev.android, dev.sdk, dev.build, dev.chrome = d["android"], d["sdk"], d["build"], d["chrome"]
        dev.vc = dev.vc or APP_VC
        dev.ua = OKHTTP_UA
        dev.webview_ua = WEBVIEW_UA_TPL.format(av=dev.android, token=WEBVIEW_TOKEN.format(vc=dev.vc))
        dev.created = dev.created or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return dev

    def check_consistency(self):
        """返回自洽性问题列表；非空说明这份档案会被服务端看出矛盾。"""
        bad = []
        if not re.fullmatch(r"[0-9a-fA-F]{32}", self.phone_id or ""):
            bad.append("phoneId 不是 32 位 hex（App 缺省是 UUID 去横线）")
        if self.ua and not self.ua.startswith("okhttp/"):
            bad.append("原生接口 UA 不是 okhttp/x（App 是 okhttp/4.12.0，浏览器 UA 反而显眼）")
        if self.android and ("Android " + self.android) not in (self.webview_ua or ""):
            bad.append("WebView UA 里的 Android 版本与档案不符（H5 页会暴露）")
        if self.ua and self.ua != OKHTTP_UA:
            bad.append("UA 版本与样本 App 不符（样本为 okhttp/4.12.0）")
        if not self.build:
            bad.append("缺 Build 号")
        if self.model and self.model not in [d["model"] for d in DEVICES]:
            bad.append("机型 %s 不在已知自洽机型池里（可能造出不存在机型）" % self.model)
        return bad


class RateGovernor:
    """写操作的限速闸门：最小间隔 + 每小时/每日配额 + 冷却 + 静默时段。"""

    def __init__(self, min_interval=8.0, per_hour=6, per_day=30, quiet=(1, 7),
                 cooldown_after_soft=2, cooldown_minutes=30, path=RATE_PATH):
        self.min_interval, self.per_hour, self.per_day = min_interval, per_hour, per_day
        self.quiet = quiet
        self.cooldown_after_soft = cooldown_after_soft
        self.cooldown_minutes = cooldown_minutes
        self.path = path
        self.writes = []          # 最近 24h 的写时间戳
        self.last_write = 0.0
        self.cooldown_until = 0.0
        self.load()

    def load(self):
        try:
            d = json.load(open(self.path, encoding="utf-8"))
            self.writes = [float(t) for t in d.get("writes", []) if now_ts() - float(t) < 86400]
            self.last_write = float(d.get("last_write", 0))
            self.cooldown_until = float(d.get("cooldown_until", 0))
        except Exception:
            pass

    def save(self):
        try:
            json.dump({"writes": self.writes[-200:], "last_write": self.last_write,
                       "cooldown_until": self.cooldown_until}, open(self.path, "w", encoding="utf-8"))
            os.chmod(self.path, 0o600)
        except Exception:
            pass

    def prune(self):
        cutoff = now_ts() - 86400
        self.writes = [t for t in self.writes if t > cutoff]

    def check(self, dry=False):
        """返回 (是否放行, 需要等待秒数, 原因)。"""
        self.prune()
        t = now_ts()
        if in_quiet_hours(self.quiet):
            return False, 0, "静默时段 %02d:00-%02d:00 内不提交（真人这个点不签到）" % self.quiet
        if self.cooldown_until > t:
            return False, self.cooldown_until - t, "冷却中（%.0f 分钟后到期）" % ((self.cooldown_until - t) / 60)
        if len([x for x in self.writes if x > t - 3600]) >= self.per_hour:
            oldest = min(x for x in self.writes if x > t - 3600)
            return False, oldest + 3600 - t, "本小时写配额已满（%d/小时）" % self.per_hour
        if len(self.writes) >= self.per_day:
            return False, 0, "24 小时写配额已满（%d 次）" % self.per_day
        gap = self.min_interval - (t - self.last_write)
        if gap > 0:
            return False, gap, "距上次写仅 %.1fs（下限 %.1fs）" % (t - self.last_write, self.min_interval)
        return True, 0, "OK"

    def record_write(self):
        self.prune()
        self.last_write = now_ts()
        self.writes.append(self.last_write)
        self.save()

    def cooldown(self, minutes=None):
        self.cooldown_until = now_ts() + (minutes or self.cooldown_minutes) * 60
        self.save()

    HARD_BLOCK = ("冷却中", "配额已满", "静默时段")

    def wait_for_slot(self, max_wait=1800, quiet=False, max_sleep=90.0):
        """等到放行，返回实际等待秒数。

        原则：**只等"小间隔"（min_interval），绝不为冷却/配额把进程挂住**。
        冷却中 / 配额满 / 静默时段属于硬阻塞 —— 一旦等待量超过 max_sleep，
        立刻抛 RiskCooldown 交回调用方，由人决定是等还是改天。
        （踩过的坑：30 分钟冷却会把 wait_for_slot 睡满，CLI 看起来像卡死。）
        """
        waited = 0.0
        while True:
            ok, need, why = self.check()
            if ok:
                return waited
            hard = any(k in why for k in self.HARD_BLOCK)
            if hard and (need <= 0 or need > max_sleep):
                raise RiskCooldown("限速闸门不放行：%s" % why)
            if need <= 0:
                raise RuntimeError("限速闸门不放行：" + why)
            if waited >= max_wait:
                raise RuntimeError("限速闸门等待超时：" + why)
            step = min(need, 60) + random.uniform(0.5, 2.5)
            if not quiet:
                print("[risk] %s -> 等 %.0fs" % (why, step))
            time.sleep(step)
            waited += step


class RiskGuard:
    """响应判级 + strikes + 冷却/停机（持久化，进程重启也记得）。"""

    def __init__(self, path=RISK_PATH, cooldown_after_soft=2, cooldown_minutes=30):
        self.path = path
        self.cooldown_after_soft = cooldown_after_soft
        self.cooldown_minutes = cooldown_minutes
        self.state = {"soft": 0, "hard": 0, "halted": False, "halted_reason": "",
                      "cooldown_until": 0.0, "updated": 0, "events": []}
        self.load()

    def load(self):
        try:
            self.state.update(json.load(open(self.path, encoding="utf-8")))
        except Exception:
            pass

    def save(self):
        try:
            self.state["updated"] = int(now_ts())
            self.state["events"] = self.state["events"][-50:]
            json.dump(self.state, open(self.path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
            os.chmod(self.path, 0o600)
        except Exception:
            pass

    def classify(self, status, body, headers=None):
        """返回 dict(level, reason)。level: OK/NOTICE/WARN/COOLDOWN/HALT。"""
        text = (body or "")[:2000]
        if status in (401,):
            return {"level": "HALT", "reason": "HTTP 401：登录态失效"}
        if status == 403:
            return {"level": "HALT", "reason": "HTTP 403：网关/WAF 拦截（头/频率/TLS 指纹问题）"}
        if status == 429:
            return {"level": "COOLDOWN", "reason": "HTTP 429：被限流"}
        for rx, level, reason in RISK_SIGNALS:
            if rx.search(text) or (level == "HALT" and rx.search(str(status))):
                return {"level": level, "reason": reason}
        if status and status >= 500:
            return {"level": "WARN", "reason": "HTTP %s：服务端异常" % status}
        return {"level": "OK", "reason": "未见风控信号"}

    def observe(self, verdict, url=""):
        """把一次判级结果写进状态机；返回最终动作 action。"""
        lv = verdict["level"]
        if lv == "HALT":
            self.state["hard"] += 1
            self.state["halted"] = True
            self.state["halted_reason"] = verdict["reason"] + (" @ %s" % redact(url) if url else "")
        elif lv == "COOLDOWN":
            self.state["soft"] += 1
        if self.state["soft"] >= self.cooldown_after_soft:
            self.state["cooldown_until"] = now_ts() + self.cooldown_minutes * 60
            self.state["soft"] = 0
        self.state["events"].append({"t": int(now_ts()), "level": lv, "reason": verdict["reason"][:160],
                                     "url": redact(url)[:200]})
        self.save()
        if self.state["halted"]:
            return "HALT"
        if self.state["cooldown_until"] > now_ts():
            return "COOLDOWN"
        return lv

    def blocked(self):
        if self.state.get("halted"):
            return "HALT", self.state.get("halted_reason", "")
        if self.state.get("cooldown_until", 0) > now_ts():
            return "COOLDOWN", "冷却至 %s" % datetime.fromtimestamp(self.state["cooldown_until"]).strftime("%H:%M:%S")
        return None, ""

    def reset(self):
        self.state = {"soft": 0, "hard": 0, "halted": False, "halted_reason": "",
                      "cooldown_until": 0.0, "updated": 0, "events": self.state.get("events", [])}
        self.save()


class StealthSession:
    """把 requests.Session 包成「像 App 且在风控面前会自己刹车」的会话。"""

    def __init__(self, cookie=None, device=None, uid="", referer=None, impersonate="chrome120",
                 tls=True, xhr=False, proxy=None, guard=True, policy=None, audit=True,
                 max_writes_per_hour=6, min_interval=8.0, per_day=30, quiet=(1, 7), ua_mode="app"):
        self.device = device or Device.load_or_create(uid=uid)
        if uid:
            self.device.uid = str(uid)
        self.uid = str(uid or self.device.uid or "")
        self.ua_mode = ua_mode                      # app=okhttp UA；h5=WebView UA
        self.use_tls = bool(HAVE_CFFI and tls)
        self.guard = RiskGuard()
        self.rate = RateGovernor(min_interval=min_interval, per_hour=max_writes_per_hour,
                                 per_day=per_day, quiet=quiet)
        self.audit_on = audit
        self.referer = referer or "https://mobilelearn.chaoxing.com/"
        self.writes = 0
        self.reads = 0
        self.verdicts = []
        self.session = cffi_requests.Session(impersonate=impersonate) if self.use_tls else requests.Session()
        self.session.headers.update(self.base_headers())
        if cookie:
            self.session.headers["Cookie"] = cookie.strip()
        if proxy:
            self.session.proxies = {"http": proxy, "https": proxy}

    # --- 兼容 v1 的属性名（外部脚本读 sess._cx_device / _cx_tls） ---
    @property
    def _cx_device(self):
        return self.device

    @property
    def _cx_tls(self):
        return self.use_tls

    @property
    def headers(self):
        return self.session.headers

    @property
    def proxies(self):
        return self.session.proxies

    @proxies.setter
    def proxies(self, v):
        self.session.proxies = v

    def base_headers(self):
        ua = self.device.ua if self.ua_mode == "app" else self.device.webview_ua
        return {
            "User-Agent": ua,
            "Accept": "*/*",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
            "Referer": self.referer,
            "X-Requested-With": APP_NAME,
        }

    def set_cookie(self, cookie):
        self.session.headers["Cookie"] = (cookie or "").strip()

    # ---------------- 请求 ----------------
    def is_write(self, method, url):
        u = (url or "").lower()
        if any(h in u for h in WRITE_HINTS):
            return True
        return str(method).upper() in ("POST", "PUT", "DELETE")

    def request(self, method, url, **kw):
        method = str(method).upper()
        write = self.is_write(method, url)
        blocked, why = self.guard.blocked()
        if blocked:
            raise RuntimeError("风控熔断中（%s）：%s —— 用 --reset-risk 前请先看 ~/.chaoxing_risk.json" % (blocked, why))
        if write:
            self.rate.wait_for_slot()
            self.cover_traffic(n=random.choice([1, 2]))   # 先读后写
        else:
            time.sleep(max(0.0, random.gauss(0.7, 0.35)))  # 读操作也要有人的节奏，防"扫描式"读

        kw.setdefault("timeout", 25)
        kw.setdefault("allow_redirects", True)
        t0 = now_ts()
        try:
            r = self.session.request(method, url, **kw)
        except Exception as e:
            self.audit(method, url, "ERR", 0, now_ts() - t0, str(e)[:120], "WARN")
            if write:
                self._backoff(write=True)
            raise
        ms = (now_ts() - t0) * 1000
        body = r.text if getattr(r, "text", None) is not None else ""
        v = self.guard.classify(r.status_code, body, dict(r.headers or {}))
        action = self.guard.observe(v, url) if self.guard_on else v["level"]
        self.verdicts.append((url, v))
        if write:
            self.rate.record_write()
            self.writes += 1
        else:
            self.reads += 1
        if v["level"] == "WARN":
            self._backoff(write=False)
        self.audit(method, url, r.status_code, len(r.content or b""), ms, v["reason"], action)
        if write and action == "HALT":
            raise RiskHalt("风控停机：%s（已记录到 %s）" % (v["reason"], RISK_PATH), response=r, verdict=v)
        if write and action == "COOLDOWN":
            self.rate.cooldown()
            raise RiskCooldown("被限流，已冷却 %d 分钟：%s" % (self.rate.cooldown_minutes, v["reason"]),
                               response=r, verdict=v)
        return r

    guard_on = True

    def get(self, url, **kw):
        return self.request("GET", url, **kw)

    def post(self, url, **kw):
        return self.request("POST", url, **kw)

    def _backoff(self, write=True):
        base = 30 if write else 10
        s = min(base * random.uniform(1.0, 2.0), 300)
        print("[risk] 退避 %.0fs" % s)
        time.sleep(s)

    # ---------------- 掩护流量 ----------------
    def cover_traffic(self, n=1, quiet=True):
        """在读接口上产生正常学习痕迹（课表 / 活动列表 / 任务点）。"""
        out = []
        for p in random.sample(COVER_FLOW, min(n, len(COVER_FLOW))):
            url = p.replace("{uid}", self.uid)
            try:
                r = self.session.get(url, timeout=15)
                out.append((r.status_code, len(r.content or b"")))
                if not quiet:
                    print("[stealth] 掩护 %s -> %s" % (redact(url), r.status_code))
            except Exception as e:
                out.append(("ERR", str(e)[:60]))
            time.sleep(random.uniform(1.5, 5.0))
        return out

    def warmup(self, n=None, quiet=False):
        n = n or len(COVER_FLOW)
        return self.cover_traffic(n=n, quiet=quiet)

    def explain(self, r):
        return explain(getattr(r, "text", ""), getattr(r, "status_code", None))

    # ---------------- 审计 ----------------
    def audit(self, method, url, status, size, ms, reason, action):
        if not self.audit_on:
            return
        try:
            rec = {"t": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "uid": self.uid[-6:],
                   "m": method, "url": redact(url), "code": status, "bytes": size,
                   "ms": int(ms), "verdict": action, "why": reason[:120],
                   "tls": "curl_cffi" if self.use_tls else "requests", "ua": self.ua_mode}
            with open(AUDIT_PATH, "a", encoding="utf-8") as f:
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        except Exception:
            pass

    def report(self):
        return {"writes": self.writes, "reads": self.reads,
                "tls": "curl_cffi" if self.use_tls else "requests(默认,可被 JA3 区分)",
                "device": self.device.to_dict(),
                "rate": {"min_interval": self.rate.min_interval, "per_hour": self.rate.per_hour,
                         "per_day": self.rate.per_day, "quiet": self.rate.quiet,
                         "writes_1h": len([x for x in self.rate.writes if x > now_ts() - 3600]),
                         "writes_24h": len(self.rate.writes)},
                "risk": {"halted": self.guard.state["halted"],
                         "reason": self.guard.state.get("halted_reason", ""),
                         "soft": self.guard.state["soft"]}}


# ---------------- 向后兼容的函数式 API（v1 调用方继续可用） ----------------
def make_session(cookie=None, device=None, uid="", referer=None, impersonate="chrome120",
                 tls=True, xhr=False, proxy=None, guard=True, **kw):
    ss = StealthSession(cookie=cookie, device=device, uid=uid, referer=referer,
                        impersonate=impersonate, tls=tls, xhr=xhr, proxy=proxy, guard=guard,
                        ua_mode=("h5" if xhr else "app"), **kw)
    return ss


def base_headers(device, referer=None, xhr=False):
    ua = device.webview_ua if xhr else device.ua
    h = {"User-Agent": ua, "Accept": "*/*", "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
         "Accept-Encoding": "gzip, deflate", "Connection": "keep-alive",
         "Referer": referer or "https://mobilelearn.chaoxing.com/"}
    if xhr:
        h["X-Requested-With"] = APP_NAME
    return h


def human_delay(lo=3.0, hi=30.0, quiet=False):
    """拟人延迟：截断高斯（真人不是均匀分布，扎堆在均值附近）。"""
    mu = (lo + hi) / 2.0
    s = min(max(random.gauss(mu, (hi - lo) / 4.0), lo), hi)
    if not quiet:
        print("[stealth] 拟人延迟 %.1fs" % s)
    time.sleep(s)
    return s


def warmup(sess, base="https://mobilelearn.chaoxing.com", uid="", paths=None, quiet=False):
    if hasattr(sess, "cover_traffic"):
        if paths:
            out = []
            for p in paths:
                url = (p if p.startswith("http") else base + p).replace("{uid}", str(uid))
                try:
                    r = sess.session.get(url, timeout=15)
                    out.append((r.status_code, len(r.content or b""), p))
                except Exception as e:
                    out.append(("ERR", str(e)[:60], p))
                time.sleep(random.uniform(1.5, 5.0))
            return out
        return sess.cover_traffic(n=len(COVER_FLOW), quiet=quiet)
    # 退化为裸 session
    out = []
    for p in (paths or COVER_FLOW):
        url = (p if p.startswith("http") else base + p).replace("{uid}", str(uid))
        try:
            r = sess.get(url, timeout=20)
            out.append((r.status_code, len(r.content), p))
        except Exception as e:
            out.append(("ERR", str(e)[:60], p))
    return out


def explain(body, status=None):
    v = RiskGuard().classify(status, body)
    if v["level"] != "OK":
        return "[%s] %s" % (v["level"], v["reason"])
    b = (body or "")[:300]
    for k, msg in (("请先登录", "未登录：cookie 缺失/过期"),
                   ("statusCode", "通道 A 回包：300 成功 / 306 enc 错 / 307 过期 / 308 无此 id"),
                   ("success", "提交被接受")):
        if k in b:
            return msg
    if status == 403:
        return "403：网关/WAF 拦截（头、频率或 TLS 指纹）"
    return "未识别回包：%s" % b


# ---------------- CLI ----------------
def doctor(uid="", cookie=None, probe_url="https://mobilelearn.chaoxing.com/"):
    print("=== 伪装层体检 ===")
    dev = Device.load_or_create(uid=uid)
    checks = []
    checks.append(("1 身份一致性", "OK" if not dev.check_consistency() else "WARN",
                   "; ".join(dev.check_consistency()) or "uid=%s phoneId=%s %s/%s Android%s" %
                   (dev.uid or "-", dev.phone_id, dev.brand, dev.model, dev.android)))
    checks.append(("2 TLS 指纹", "OK" if HAVE_CFFI else "WARN",
                   "curl_cffi 可用(impersonate=chrome120)" if HAVE_CFFI else "缺 curl_cffi：pip install curl_cffi，否则 JA3 是 Python"))
    ua_txt = ("okhttp/4.12.0(与样本 App 一致)" if dev.ua == OKHTTP_UA else dev.ua[:48])
    ua_txt += " + WebView:%s" % dev.webview_ua[:38]
    checks.append(("3 头部", "OK", "UA=%s；X-Requested-With/Cookie/Referer 齐全" % ua_txt))
    g = RateGovernor()
    ok, need, why = g.check()
    checks.append(("4 限速", "OK" if ok else "COOLDOWN",
                   "放行" if ok else why))
    rg = RiskGuard()
    blk, rwhy = rg.blocked()
    checks.append(("5 风控状态", "OK" if not blk else "HALT", rwhy or "无停机/冷却；hard=%d" % rg.state["hard"]))
    os_ok = os.path.exists(AUDIT_PATH)
    checks.append(("6 审计", "OK", ("已有 %d 行 %s" % (sum(1 for _ in open(AUDIT_PATH, encoding='utf-8')), AUDIT_PATH)) if os_ok else "首次运行会创建 " + AUDIT_PATH))
    for name, lv, msg in checks:
        print("  [%s] %s | %s" % (lv, name, msg))
    if cookie is not None or True:
        try:
            ss = StealthSession(cookie=cookie, device=dev, uid=uid, guard=True, audit=False)
            r = ss.session.get(probe_url, timeout=20)
            print("  连线自测: HTTP %s %dB  TLS=%s" % (r.status_code, len(r.content or b""),
                                                    "curl_cffi" if ss.use_tls else "requests"))
        except Exception as e:
            print("  连线自测: 失败 %s" % str(e)[:120])
    print("提示：写操作受限速 + 风控熔断约束；静默时段 %s 不提交。" % str(g.quiet))
    return checks


def simulate(n=6, uid="10000000"):
    print("=== 干跑 %d 次提交流水（不联网） ===" % n)
    dev = Device.load_or_create(uid=uid)
    ss = StealthSession(device=dev, uid=uid, audit=False)
    ss.rate.min_interval, ss.rate.per_hour = 8.0, 100
    t = 0.0
    prev = 0.0
    for i in range(n):
        gap = max(0.0, random.gauss(14, 6))
        reads = random.choice([1, 2])
        prev = prev + gap + reads * random.uniform(1.5, 5.0)
        print("  #%d  %s  掩护读 %d 次 → 提交（间隔 %.1fs）" %
              (i + 1, "%02d:%02d:%02d" % (int(prev // 3600) % 24, int(prev // 60) % 60, int(prev) % 60), reads, gap))
    print("  总耗时 %.1f 分钟；无固定秒数、无整点、无突发" % (prev / 60))


def tail_audit(n=20):
    if not os.path.exists(AUDIT_PATH):
        print("暂无审计：", AUDIT_PATH)
        return
    lines = open(AUDIT_PATH, encoding="utf-8").read().splitlines()[-n:]
    for l in lines:
        try:
            d = json.loads(l)
            print("%s %-4s %-3s %6sms %-8s %s  | %s" % (d["t"][11:], d["m"], d["code"], d["ms"],
                                                        d["verdict"], d["url"][:70], d["why"][:40]))
        except Exception:
            print(l[:160])


def main():
    ap = argparse.ArgumentParser(description="学习通伪装层 + 风控层（身份/指纹/头/时序/流量/熔断）")
    ap.add_argument("--doctor", action="store_true", help="六维体检（推荐第一条命令）")
    ap.add_argument("--show", action="store_true", help="打印设备档案")
    ap.add_argument("--new-device", action="store_true", help="重新生成设备档案（换身份）")
    ap.add_argument("--uid", default="")
    ap.add_argument("--cookie", default=None)
    ap.add_argument("--probe", nargs="?", const="https://mobilelearn.chaoxing.com/")
    ap.add_argument("--warmup", action="store_true", help="跑一遍学习动线掩护流量")
    ap.add_argument("--simulate", nargs="?", const=6, type=int, help="干跑提交流水打印时序")
    ap.add_argument("--audit", nargs="?", const=20, type=int, help="打印最近 N 条审计")
    ap.add_argument("--risk", action="store_true", help="风控状态")
    ap.add_argument("--reset-risk", action="store_true", help="清空冷却/停机标记")
    ap.add_argument("--max-writes-per-hour", type=int, default=6, help="每小时写配额")
    ap.add_argument("--min-interval", type=float, default=8.0, help="两次写最小间隔秒")
    ap.add_argument("--quiet-hours", default="1-7", help="静默时段 如 1-7 / 22-6；none 关闭")
    ap.add_argument("--no-tls", action="store_true", help="不用 curl_cffi TLS 指纹（不推荐）")
    a = ap.parse_args()

    if a.new_device:
        dev = Device.load_or_create(uid=a.uid, rotate=True)
        print("新档案:", json.dumps(dev.to_dict(), ensure_ascii=False))
        return
    if a.show:
        dev = Device.load_or_create(uid=a.uid)
        print(json.dumps(dev.to_dict(), ensure_ascii=False, indent=2))
        print("一致性问题:", dev.check_consistency() or "无")
        print("curl_cffi:", HAVE_CFFI)
        return
    if a.doctor:
        doctor(uid=a.uid, cookie=a.cookie)
        return
    if a.simulate:
        simulate(a.simulate, uid=a.uid or "10000000")
        return
    if a.audit is not None and not a.warmup and not a.probe:
        tail_audit(a.audit)
        return
    if a.risk:
        rg = RiskGuard()
        print(json.dumps(rg.state, ensure_ascii=False, indent=2)[:2500])
        return
    if a.reset_risk:
        RiskGuard().reset()
        RateGovernor().cooldown(-10 ** 6)   # 清冷却
        print("已清空风控标记与冷却")
        return
    if a.warmup or a.probe:
        ss = StealthSession(cookie=a.cookie, uid=a.uid, tls=not a.no_tls,
                            max_writes_per_hour=a.max_writes_per_hour,
                            min_interval=a.min_interval, quiet=parse_quiet(a.quiet_hours))
        if a.warmup:
            ss.warmup(quiet=False)
            print("掩护流量完成。")
        if a.probe:
            r = ss.session.get(a.probe, timeout=25)
            print("HTTP %s %dB  TLS=%s" % (r.status_code, len(r.content or b""),
                                           "curl_cffi" if ss.use_tls else "requests"))
            print("解读:", ss.explain(r))
        return
    ap.print_help()


if __name__ == "__main__":
    main()
