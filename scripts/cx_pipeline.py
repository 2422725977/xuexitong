#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cx_pipeline.py --- 学习通「教师侧取二维码 -> 学生侧自动提交」一体化流水线

一条命令跑通中间过程：
    python3 scripts/cx_pipeline.py --mode watch \
        --tch-cookie-file ck_tch.txt --stu-cookie-file ck.txt --uid [学生PUID] \
        --course 269282723 --class 159926750 --stop-on-success --verbose

四段流水线（每段都有降级回退，任何一段失败都会落盘诊断）：
  1) 教师侧班级枚举  mycourse/backclazzdata?view=json&getTchClazzType=1&mcode=<puid>
  2) 教师侧活动定位  ppt/activeAPI/courseactivelist / taskactivelist -> 活跃二维码签到 activeId
  3) 教师侧取 enc     gotasksign(isTeacherViewOpen=1) -> preSign -> produceSignView
                      页面正则 + 二维码图片 cv2 解码（双路取候选）
  4) 学生侧提交       pptSign/stuSignajax?enc=..&activeId=..&uid=..  （响应纯文本 success/success2 即成功）

模式：
  --mode discover  只枚举并打印（教师班级 / 活跃活动 / enc 候选），不提交
  --mode once      取一次 enc，提交一次
  --mode watch     轮询：活动或 enc 变化就提交（默认），可选 --stop-on-success
  --mode submit-url  直接提交一段二维码内容（widget/sign/e?... 或 SIGNIN: 串）
"""
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import time
import urllib.parse
from datetime import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

try:
    from stealth_session import make_session, warmup, RiskHalt, RiskCooldown
except Exception as _e:
    make_session = None
    warmup = None
    RiskHalt = RiskCooldown = Exception

try:
    from stealth_session import parse_quiet
except Exception:
    def parse_quiet(v):
        return bool(v)

try:
    from qr_sign_remote import submit_url as _submit_url
except Exception:
    _submit_url = None

try:
    from qr_relay import decode_qr_bytes as _decode_qr
except Exception:
    _decode_qr = None

try:
    from autosign import walk_active as _walk_active, jget as _jget
except Exception:
    _walk_active = None
    _jget = None

MOBILE = "https://mobilelearn.chaoxing.com/"
MOOC1API = "https://mooc1-api.chaoxing.com/"
MOOC1 = "https://mooc1.chaoxing.com/"

UA_APP_WEBVIEW = ("Mozilla/5.0 (Linux; U; Android 13) AppleWebKit/533.1 (KHTML, like Gecko) "
                  "Version/4.0 ChaoXingStudy_10946Safari")

# ---------- 抽取用正则 ----------
RE_EWM_LINK = re.compile(r"widget/sign/e\?([^\"'\s<>\\]{4,400})")
RE_ENC_Q = re.compile(r"[?&]enc=([0-9A-Za-z_\-+/=]{8,160})")
RE_ENC_KV = re.compile(r'''["']?(?:enc|ewmEnc|signEnc|qrEnc)["']?\s*[:=]\s*["']([0-9A-Za-z_\-+/=]{8,160})["']''')
RE_SIGNCODE = re.compile(r"[\"']?signCode[\"']?\s*[:=]\s*[\"']?([0-9A-Za-z]{4,16})")
RE_REAL_AID = re.compile(r"^\d{10,}$")
# 明显是模板/占位/文档示例的 enc，直接丢掉（学生签到页里就有 widget/sign/e?...&enc=xxx 这种示例串）
PLACEHOLDER_ENC = {"xxx", "xxxx", "xxxxx", "test", "test123", "example", "null", "undefined", "nil",
                   "0", "1", "enc", "n/a", "none", "{{enc}}", "enc_value", "your_enc"}
RE_IMG = re.compile(r"""(?:src|data-src|background-image)\s*[:=]\s*[\"']([^\"']{4,300})[\"']""", re.I)
RE_DATAURI = re.compile(r"data:image/(?:png|jpe?g|webp);base64,([A-Za-z0-9+/=]{300,})")


def ts():
    return datetime.now().strftime("%H:%M:%S")


def log(tag, msg):
    print("[%s] [%s] %s" % (ts(), tag, msg), flush=True)


def load_cookie(arg, path):
    if arg:
        return arg.strip()
    if path and os.path.exists(path):
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read().strip()
    return ""


def qs_to_dict(s):
    out = {}
    for k, v in urllib.parse.parse_qsl(s, keep_blank_values=True):
        out[k] = v
    return out


class TeacherSide(object):
    """教师侧：班级枚举 -> 活动定位 -> enc 采集"""

    def __init__(self, ck, uid, ua_mode="h5", dump_dir="out/tch_probe", quiet_hours=None):
        if make_session is None:
            raise SystemExit("stealth_session 不可用")
        self.expired = False
        self.sess = make_session(cookie=ck, uid=uid, referer=MOBILE, ua_mode=ua_mode,
                                 xhr=True, quiet=quiet_hours)
        self.uid = uid
        self.dump_dir = dump_dir
        self.round = 0
        self.saved = 0
        os.makedirs(dump_dir, exist_ok=True)

    # ---- 基础请求 + 落盘 ----
    def get(self, url, tag="", save=False, sniff=True):
        try:
            r = self.sess.get(url, timeout=25, allow_redirects=True)
        except Exception as e:
            log("T", "GET 失败 %s -> %r" % (url[:110], e))
            return None
        body = r.text or ""
        final = getattr(r, "url", "") or ""
        if "passport2" in final or "请登录" in body[:600] or "请先登录" in body[:600]:
            self.expired = True
            log("!", "教师 cookie 疑似失效（%s）" % final[:80])
        if save or (self.saved < 200 and ("sign" in url or "active" in url)):
            self._save(tag or "req", url, r)
        if sniff:
            cands = self.sniff(body)
            if cands:
                log("T", "%s -> %d 个 enc 候选: %s" % (tag or url[:48], len(cands),
                                                       ", ".join(c["enc"][:10] + ".." for c in cands[:4])))
            else:
                log("T", "%s -> 无 enc 候选 (HTTP %s, %d B)" % (tag or url[:48], r.status_code, len(body)))
        return r

    def _save(self, tag, url, r):
        self.saved += 1
        name = "r%02d_%s_%d.html" % (self.round, re.sub(r"[^A-Za-z0-9_]", "_", tag)[:40], self.saved)
        p = os.path.join(self.dump_dir, name)
        try:
            with open(p, "w", encoding="utf-8", errors="ignore") as f:
                f.write("<!-- %s -->\n<!-- final: %s -->\n" % (url, getattr(r, "url", "")))
                f.write(r.text or "")
        except Exception:
            pass

    # ---- 页面嗅探 ----
    def sniff(self, body):
        out = []
        if not body:
            return out
        for m in RE_EWM_LINK.finditer(body):
            q = qs_to_dict(m.group(1).replace("&amp;", "&"))
            aid = q.get("id") or q.get("activeId") or ""
            enc = q.get("enc") or ""
            if enc:
                out.append({"enc": enc, "aid": aid, "c": q.get("c", ""), "src": "widget/sign/e"})
        for m in RE_ENC_Q.finditer(body):
            out.append({"enc": m.group(1), "aid": "", "c": "", "src": "query-enc"})
        for m in RE_ENC_KV.finditer(body):
            out.append({"enc": m.group(1), "aid": "", "c": "", "src": "kv-enc"})
        sc = RE_SIGNCODE.search(body)
        if sc:
            log("T", "  (页面 signCode=%s)" % sc.group(1))
        seen, uniq = set(), []
        for c in out:
            e = (c["enc"] or "").strip()
            low = e.lower()
            if not e or low in PLACEHOLDER_ENC or len(set(low)) <= 2:
                continue
            c["enc"] = e
            if e in seen:
                continue
            seen.add(e)
            uniq.append(c)
        return uniq

    def sniff_images(self, body, base_url, limit=4):
        """页面里的二维码图片 -> cv2 解码 -> 候选"""
        if _decode_qr is None or not body:
            return []
        cands = []
        urls = []
        for m in RE_IMG.finditer(body):
            u = m.group(1)
            if u.startswith("data:"):
                continue
            if re.search(r"(ewm|qr|qrcode|sign|erweima)", u, re.I):
                urls.append(urllib.parse.urljoin(base_url, u))
        # data uri 内联二维码
        for m in RE_DATAURI.finditer(body):
            try:
                import base64
                raw = base64.b64decode(m.group(1)[:2000000] + "==")
                txt = _decode_qr(raw)
                if txt:
                    cands.append({"enc_raw": txt, "src": "img:datauri"})
            except Exception:
                pass
        for u in urls[:limit]:
            if u.startswith("data:"):
                continue
            try:
                r = self.sess.get(u, timeout=20)
                if r.status_code == 200 and len(r.content) > 200:
                    txt = _decode_qr(r.content)
                    log("T", "  图片 %s -> %s" % (u[-44:], (txt or "解不出")[:90]))
                    if txt:
                        cands.append({"enc_raw": txt, "src": "img:" + u[-32:]})
            except Exception as e:
                log("T", "  图片下载失败 %s (%r)" % (u[-40:], e))
        # 从解出的二维码内容里再抽 enc/aid
        out = []
        for c in cands:
            d = qs_to_dict(urllib.parse.urlparse(c["enc_raw"]).query) if "?" in c["enc_raw"] else {}
            if d.get("enc"):
                out.append({"enc": d["enc"], "aid": d.get("id", ""), "c": d.get("c", ""), "src": c["src"]})
            else:
                out.append({"enc": c["enc_raw"], "aid": "", "c": "", "src": c["src"]})
        return out

    # ---- 1) 班级枚举 ----
    def classes(self):
        url = MOOC1API + "mycourse/backclazzdata?view=json&getTchClazzType=1&mcode=%s" % self.uid
        r = self.get(url, "tch_classes", save=True, sniff=False)
        if r is None:
            return []
        try:
            j = r.json()
        except Exception:
            log("T", "班级列表不是 JSON，已落盘原文")
            return []
        out = []
        self._walk_classes(j, out, {})
        # 去重
        uniq, seen = [], set()
        for c in out:
            k = (c.get("course"), c.get("clazz"))
            if k in seen:
                continue
            seen.add(k)
            uniq.append(c)
        log("T", "教师班级 %d 个" % len(uniq))
        for c in uniq[:20]:
            log("T", "  %s | course=%s class=%s role=%s" % (c.get("name", "?")[:24], c.get("course"),
                                                           c.get("clazz"), c.get("role")))
        return uniq

    def _walk_classes(self, obj, out, ctx):
        if isinstance(obj, list):
            for it in obj:
                self._walk_classes(it, out, ctx)
            return
        if not isinstance(obj, dict):
            return
        keys = {k.lower(): k for k in obj.keys()}
        course = None
        for k in ("courseid", "course_id", "id"):
            if k in keys and str(obj[keys[k]]).isdigit():
                course = str(obj[keys[k]])
                break
        clazz = None
        for k in ("clazzid", "classid", "clazz_id", "class_id", "clazzid_str"):
            if k in keys:
                clazz = str(obj[keys[k]])
                break
        if course and clazz:
            rid = None
            for k in ("roletype", "role", "role_type"):
                if k in keys:
                    rid = str(obj[keys[k]])
            name = obj.get(keys.get("coursename", ""), "") or obj.get(keys.get("name", ""), "") if keys.get("coursename") or keys.get("name") else ""
            out.append({"course": course, "clazz": clazz, "role": rid, "name": name or "?"})
        for v in obj.values():
            if isinstance(v, (dict, list)):
                self._walk_classes(v, out, ctx)

    # ---- 2) 活动定位 ----
    def activities(self, course=None, clazz=None):
        urls = []
        if course and clazz:
            urls.append(MOBILE + "ppt/activeAPI/taskactivelist?courseId=%s&classId=%s&uid=%s&cpi=&appType=15"
                        % (course, clazz, self.uid))
        urls.append(MOBILE + "ppt/activeAPI/courseactivelist?puid=%s&status=1&page=1&pageSize=20&appType=15" % self.uid)
        acts = []
        for u in urls:
            r = self.get(u, "activities", sniff=False)
            if r is None:
                continue
            try:
                j = r.json()
            except Exception:
                continue
            if _walk_active is not None:
                buf = []
                _walk_active(j, buf)
                acts += buf
            else:
                self._walk_active_local(j, acts)
        uniq, seen = [], set()
        for a in acts:
            k = str(a.get("id") or a.get("activeId") or id(a))
            if k in seen:
                continue
            seen.add(k)
            uniq.append(a)
        real = [x for x in uniq if RE_REAL_AID.match(str(x.get("id") or ""))]
        if real:
            uniq = real          # 丢掉 groupList 里的 "进行中(2)" 这类汇总行
        log("T", "活动 %d 条" % len(uniq))
        for a in uniq[:12]:
            log("T", "  aid=%s type=%s status=%s %s" % (a.get("id"), a.get("activeType"),
                                                        a.get("status"), str(a.get("name") or a.get("title") or "")[:26]))
        return uniq

    def _walk_active_local(self, obj, out, depth=0):
        if depth > 8:
            return
        if isinstance(obj, list):
            for it in obj:
                self._walk_active_local(it, out, depth + 1)
            return
        if not isinstance(obj, dict):
            return
        keys = {k.lower(): k for k in obj.keys()}
        aid = None
        for k in ("id", "activeid", "activeprimaryid"):
            if k in keys and str(obj[keys[k]]).isdigit() and len(str(obj[keys[k]])) > 8:
                aid = str(obj[keys[k]])
                break
        if aid:
            out.append({"id": aid, "activeType": obj.get(keys.get("activetype", ""), ""),
                        "status": obj.get(keys.get("status", ""), ""),
                        "name": obj.get(keys.get("title", ""), "") or obj.get(keys.get("name", ""), ""),
                        "_raw": obj})
        for v in obj.values():
            if isinstance(v, (dict, list)):
                self._walk_active_local(v, out, depth + 1)

    # ---- 3) 取 enc ----
    def sign_detail(self, aid):
        url = MOBILE + "newsign/signDetail?activePrimaryId=%s&type=1" % aid
        r = self.get(url, "signDetail_%s" % aid, sniff=False)
        if r is None:
            return {}
        try:
            return r.json()
        except Exception:
            return {}

    def qr_candidates(self, aid, course=None, clazz=None):
        """教师侧全路径扫一遍，返回 [{'enc','aid','c','src'}]"""
        urls = []
        if course and clazz:
            urls.append(MOBILE + "pptSign/gotasksign?courseId=%s&classId=%s&activePrimaryId=%s&source=1&isTeacherViewOpen=1"
                        % (course, clazz, aid))
            urls.append(MOBILE + "newsign/preSign?activePrimaryId=%s&sys=1&chatId=&general=&ls=1&appType=15"
                                 "&courseId=%s&classId=%s&uid=%s&isTeacherViewOpen=1" % (aid, course, clazz, self.uid))
        urls.append(MOBILE + "sign/produceSignView?tid=%s&uid=%s&appType=15" % (self.uid, self.uid))
        cands = []
        for u in urls:
            r = self.get(u, "qr_%s" % aid, save=True)
            if r is None:
                continue
            cands += self.sniff(r.text)
            if not cands:
                cands += self.sniff_images(r.text, getattr(r, "url", u))
        uniq, seen = [], set()
        for c in cands:
            if c["enc"] in seen:
                continue
            seen.add(c["enc"])
            uniq.append(c)
        return rank(uniq, aid)


def rank(cands, target_aid=""):
    """给 enc 候选打分排序：带 id 的二维码链接 > aid 匹配 > 十六进制长串。"""
    def sc(c):
        s = 0
        if c.get("src") == "widget/sign/e":
            s += 4
        if target_aid and str(c.get("aid") or "") == str(target_aid):
            s += 3
        if re.match(r"^[0-9A-Fa-f]{16,64}$", c.get("enc") or ""):
            s += 2
        if (c.get("enc") or "").startswith("{{"):
            s -= 6
        return s
    for c in cands:
        c["score"] = sc(c)
    return sorted(cands, key=lambda c: -c.get("score", 0))


class StudentSide(object):
    def __init__(self, ck, uid, ua_mode="h5", quiet_hours=None):
        self.sess = make_session(cookie=ck, uid=uid, referer=MOBILE, ua_mode=ua_mode,
                                 xhr=True, quiet=quiet_hours)
        self.uid = uid

    def submit(self, aid, enc, name="", fid="0", lat="-1", lon="-1", verbose=True):
        if _submit_url is not None:
            content = "https://x/?enc=%s&id=%s" % (urllib.parse.quote(enc), urllib.parse.quote(str(aid)))
            return _submit_url(self.sess, content, self.uid, name, fid, lat, lon, verbose=verbose)
        q = ("pptSign/stuSignajax?enc=%s&name=%s&activeId=%s&uid=%s&clientip=&useragent="
             "&latitude=%s&longitude=%s&fid=%s&appType=15" % (urllib.parse.quote(enc), urllib.parse.quote(name),
                                                              urllib.parse.quote(str(aid)), urllib.parse.quote(self.uid),
                                                              lat, lon, urllib.parse.quote(fid)))
        r = self.sess.get(MOBILE + q, timeout=20)
        body = (r.text or "").strip()
        if verbose:
            log("S", "GET %s" % (MOBILE + q))
            log("S", "HTTP %s  %s" % (r.status_code, body[:300]))
        ok = ("success" in body.lower()) or ("签到成功" in body)
        return {"ok": ok, "msg": body[:300]}


def tch_relogin(path, verbose=True):
    """教师 cookie 缺失/失效时，用环境变量 CX_TCH_PHONE / CX_TCH_PASS 走 cx_login.py 重新登录。"""
    ph = os.environ.get("CX_TCH_PHONE", "")
    pw = os.environ.get("CX_TCH_PASS", "")
    if not (ph and pw):
        log("!", "未设置 CX_TCH_PHONE / CX_TCH_PASS，无法自动重登教师账号")
        return False
    jar = os.path.splitext(path)[0] + ".json"
    if verbose:
        log("i", "教师账号登录中（手机号尾号 %s，密码长度 %d，不落日志）…" % (ph[-4:], len(pw)))
    try:
        p = subprocess.run([sys.executable, os.path.join(HERE, "cx_login.py"),
                            "--phone", ph, "--password", pw, "--out", path, "--jar", jar],
                           timeout=120, capture_output=True, text=True)
    except Exception as e:
        log("!", "重登异常 %r" % (e,))
        return False
    ok = p.returncode == 0 and os.path.exists(path) and os.path.getsize(path) > 100
    log("i" if ok else "!", "教师登录 %s（rc=%s, %dB）" % ("成功" if ok else "失败", p.returncode,
                                                         os.path.getsize(path) if os.path.exists(path) else 0))
    if not ok and verbose:
        tail = ((p.stdout or "") + (p.stderr or "")).strip().splitlines()[-4:]
        for line in tail:
            log("-", "  login: %s" % line[:160])
    return ok


def rec(path, obj):
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "a", encoding="utf-8") as f:
            f.write(json.dumps(obj, ensure_ascii=False) + "\n")
    except Exception:
        pass


def main():
    ap = argparse.ArgumentParser(description="学习通 教师侧取码 -> 学生侧提交 一体化流水线")
    ap.add_argument("--mode", default="watch", choices=["discover", "once", "watch", "submit-url"])
    ap.add_argument("--tch-cookie", default="")
    ap.add_argument("--tch-cookie-file", default="ck_tch.txt")
    ap.add_argument("--stu-cookie", default="")
    ap.add_argument("--stu-cookie-file", default="ck.txt")
    ap.add_argument("--uid", required=True, help="学生 puid（提交身份）")
    ap.add_argument("--tch-uid", default="", help="教师 puid（默认取教师 cookie 的 _uid）")
    ap.add_argument("--course", default="")
    ap.add_argument("--class", dest="clazz", default="")
    ap.add_argument("--aid", default="", help="指定活动 id（跳过自动定位）")
    ap.add_argument("--enc", default="", help="指定 enc（跳过教师侧采集）")
    ap.add_argument("--qr", default="", help="submit-url 模式：widget/sign/e?... 或 SIGNIN: 串")
    ap.add_argument("--name", default="")
    ap.add_argument("--fid", default="0")
    ap.add_argument("--interval", type=float, default=10.0)
    ap.add_argument("--rounds", type=int, default=0, help="0=无限")
    ap.add_argument("--max-submits", type=int, default=6)
    ap.add_argument("--stop-on-success", action="store_true")
    ap.add_argument("--want-type", default="2", help="目标 activeType，默认 2=二维码签到（逗号分隔可多值）")
    ap.add_argument("--ua-mode", default="h5", choices=["browser", "app", "h5"])
    ap.add_argument("--quiet-hours", default="1-7", help="凌晨静默时段 START-END，none=不静默")
    ap.add_argument("--dump-dir", default="out/tch_probe")
    ap.add_argument("--log", default="out/pipeline.jsonl")
    ap.add_argument("--tch-login", action="store_true", help="教师 cookie 缺失/失效时用 CX_TCH_PHONE/CX_TCH_PASS 自动登录")
    ap.add_argument("--dry-run", action="store_true", help="只到取 enc，不提交")
    ap.add_argument("--verbose", action="store_true")
    a = ap.parse_args()

    if (a.mode != "submit-url" and a.tch_login
            and not a.tch_cookie and not os.path.exists(a.tch_cookie_file)):
        tch_relogin(a.tch_cookie_file)
    tch_ck = load_cookie(a.tch_cookie, a.tch_cookie_file)
    stu_ck = load_cookie(a.stu_cookie, a.stu_cookie_file)
    want = set(x.strip() for x in a.want_type.split(",") if x.strip())
    log("i", "模式=%s uid=%s 教师cookie=%s 学生cookie=%s 目标类型=%s"
        % (a.mode, a.uid, "有(%dB)" % len(tch_ck) if tch_ck else "无", "有(%dB)" % len(stu_ck) if stu_ck else "无", sorted(want)))

    if a.mode == "submit-url":
        if not (a.qr and stu_ck):
            raise SystemExit("submit-url 需要 --qr 与 --stu-cookie-file")
        st = StudentSide(stu_ck, a.uid, a.ua_mode, quiet_hours=parse_quiet(a.quiet_hours))
        _submit_url(st.sess, a.qr, a.uid, a.name, a.fid, verbose=True)
        return 0

    tch_uid = a.tch_uid
    if not tch_uid and tch_ck:
        m = re.search(r"(?:^|;\s*)_uid=([0-9]+)", tch_ck)
        tch_uid = m.group(1) if m else ""
    qh = parse_quiet(a.quiet_hours)
    tch = TeacherSide(tch_ck, tch_uid or a.uid, a.ua_mode, a.dump_dir, quiet_hours=qh) if tch_ck else None
    stu = StudentSide(stu_ck, a.uid, a.ua_mode, quiet_hours=qh) if (stu_ck and not a.dry_run) else None

    if tch and warmup and not a.dry_run and a.mode == "watch":
        try:
            warmup(stu.sess if stu else tch.sess, uid=a.uid, quiet=True)
        except Exception:
            pass

    if a.mode == "discover":
        if not tch:
            log("!", "没有教师 cookie：只能做学生侧活动列表。请把教师浏览器 cookie 存成 ck_tch.txt")
        if tch:
            cls = tch.classes()
            for c in cls[:6]:
                tch.activities(c["course"], c["clazz"])
            if a.aid:
                tch.qr_candidates(a.aid, a.course or None, a.clazz or None)
        return 0

    last_key = ""
    n_submit = 0
    rnd = 0
    while True:
        rnd += 1
        if tch and tch.expired and a.tch_login:
            if tch_relogin(a.tch_cookie_file):
                tch_ck = load_cookie("", a.tch_cookie_file)
                tch = TeacherSide(tch_ck, tch_uid or a.uid, a.ua_mode, a.dump_dir, quiet_hours=qh)
        if tch:
            tch.round = rnd
        try:
            cands = []
            if a.enc and a.aid:
                cands = [{"enc": a.enc, "aid": a.aid, "c": "", "src": "cli"}]
            elif tch:
                aids = [a.aid] if a.aid else []
                if not aids:
                    acts = tch.activities(a.course or None, a.clazz or None)
                    live = [x for x in acts if str(x.get("activeType", "")) in want and str(x.get("status", "")) in ("1", "true")]
                    live = [x for x in live if str(x.get("id", "")).isdigit() and len(str(x.get("id"))) > 8]
                    if not live:
                        live = [x for x in acts if str(x.get("id", "")).isdigit() and len(str(x.get("id"))) > 8]
                    aids = [x.get("id") for x in live[:3]]
                    log("T", "本轮候选活动: %s" % aids)
                for aid in aids:
                    d = tch.sign_detail(aid)
                    log("T", "aid=%s status=%s isOver=%s signCode=%s attend=%s"
                        % (aid, d.get("status"), d.get("isOver"), d.get("signCode"), d.get("attendNum")))
                    if str(d.get("isOver")) == "1":
                        log("T", "  aid=%s 二维码展示会话已关闭(isOver=1)，继续尝试取 enc")
                    cands += tch.qr_candidates(aid, a.course or None, a.clazz or None)
            else:
                log("!", "无教师 cookie 且未给 --enc/--aid：无法取 enc")
            uniq, seen = [], set()
            for c in cands:
                if c["enc"] and c["enc"] not in seen:
                    seen.add(c["enc"])
                    uniq.append(c)
            uniq = rank(uniq, a.aid)
            if not uniq:
                log("!", "第 %d 轮未取到 enc 候选（诊断文件见 %s/）" % (rnd, a.dump_dir))
                rec(a.log, {"t": ts(), "round": rnd, "event": "no_enc"})
            else:
                log("+", "第 %d 轮 enc 候选 %d 个：%s" % (rnd, len(uniq),
                                                          ", ".join("%s..(score=%s,%s)" % (c["enc"][:12], c.get("score"),
                                                                                           c["src"]) for c in uniq[:5])))
                for c in uniq:
                    key = "%s|%s" % (c["aid"] or a.aid, c["enc"])
                    if key == last_key:
                        if a.verbose:
                            log("-", "与上轮相同，跳过")
                        continue
                    last_key = key
                    if a.dry_run or stu is None:
                        rec(a.log, {"t": ts(), "round": rnd, "event": "enc_found", "enc": c["enc"][:16],
                                    "aid": c["aid"] or a.aid, "src": c["src"], "dry_run": True})
                        continue
                    n_submit += 1
                    res = stu.submit(c["aid"] or a.aid, c["enc"], a.name, a.fid, verbose=True)
                    rec(a.log, {"t": ts(), "round": rnd, "event": "submit", "enc": c["enc"][:16],
                                "aid": c["aid"] or a.aid, "src": c["src"], "ok": res.get("ok"),
                                "msg": str(res.get("msg"))[:120]})
                    if res.get("ok"):
                        log("=", "签到成功！enc=%s aid=%s" % (c["enc"][:12], c["aid"] or a.aid))
                        if a.stop_on_success:
                            return 0
                    if a.max_submits and n_submit >= a.max_submits:
                        log("i", "已达 --max-submits %d，退出" % a.max_submits)
                        return 0
        except (RiskHalt, RiskCooldown) as e:
            log("!", "风控闸门: %r" % (e,))
            rec(a.log, {"t": ts(), "round": rnd, "event": "risk", "msg": repr(e)})
        except SystemExit:
            raise
        except Exception as e:
            log("!", "第 %d 轮异常: %r" % (rnd, e))
            rec(a.log, {"t": ts(), "round": rnd, "event": "error", "msg": repr(e)})

        if a.rounds and rnd >= a.rounds:
            log("i", "达到 --rounds %d，退出" % a.rounds)
            return 0
        time.sleep(a.interval)


if __name__ == "__main__":
    sys.exit(main())
