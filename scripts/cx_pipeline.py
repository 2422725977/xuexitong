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
import random
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

# ---------------------------------------------------------------------------
# 作用域白名单（用户明令 m02160：只允许「计算机二级」测试班级）
#   任何越界请求在发出之前就被拦下，不给服务端留记录。
# ---------------------------------------------------------------------------
ALLOW_COURSE = "269282723"      # 计算机二级
ALLOW_CLASS = "159926750"       # clazzId
ALLOW_ANY = False               # 设为 True 才放行其他班级（默认硬闸）


class ScopeViolation(SystemExit):
    pass


def guard_scope(course=None, clazz=None, what="操作", allow_course=None, allow_class=None):
    ac = str(allow_course or ALLOW_COURSE)
    ak = str(allow_class or ALLOW_CLASS)
    if ALLOW_ANY:
        return True
    if course and str(course) != ac:
        raise ScopeViolation("[scope] 拒绝越界：%s course=%s 不在白名单 %s（只允许计算机二级测试班）"
                             % (what, course, ac))
    if clazz and str(clazz) != ak:
        raise ScopeViolation("[scope] 拒绝越界：%s class=%s 不在白名单 %s（只允许计算机二级测试班）"
                             % (what, clazz, ak))
    return True

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

# 签到类型（教师发起签到页 otherId -> 标题；人脸仅二维码/位置支持）
SIGN_TYPE_TITLE = {"0": "普通签到", "1": "拍照签到", "2": "二维码签到", "3": "手势签到",
                   "4": "位置签到", "5": "签到码"}
# 明显是模板/占位/文档示例的 enc，直接丢掉（学生签到页里就有 widget/sign/e?...&enc=xxx 这种示例串）
PLACEHOLDER_ENC = {"xxx", "xxxx", "xxxxx", "test", "test123", "example", "null", "undefined", "nil",
                   "0", "1", "enc", "n/a", "none", "{{enc}}", "enc_value", "your_enc"}
RE_IMG = re.compile(r"""(?:src|data-src|background-image)\s*[:=]\s*[\"']([^\"']{4,300})[\"']""", re.I)
RE_DATAURI = re.compile(r"data:image/(?:png|jpe?g|webp);base64,([A-Za-z0-9+/=]{300,})")
# 真 enc 的形状：16~64 位十六进制（实测 A0314A30BDF5D498FE0D7774D1373894）。
# 页面里的 JS 模板串（如 "enc="+ewnEnc+"）会被 KV 正则误抓成 +ewnEnc+ —— 必须丢掉，不能拿去提交。
RE_ENC_OK = re.compile(r"^[0-9A-Fa-f]{16,64}$")


def _walk_active_any(obj, out, depth=0):
    """把活动列表 JSON 里所有长度>8 的纯数字 id 当作 activeId 收集（任务/分组汇总行会被 RE_REAL_AID 过滤）"""
    if depth > 8:
        return
    if isinstance(obj, list):
        for it in obj:
            _walk_active_any(it, out, depth + 1)
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
                    "name": obj.get(keys.get("title", ""), "") or obj.get(keys.get("name", ""), "")})
    for v in obj.values():
        if isinstance(v, (dict, list)):
            _walk_active_any(v, out, depth + 1)


def _list_activities(sess, uid, urls, tag="T"):
    """共用：GET 一批活动列表 URL -> 去重后的活动 dict 列表"""
    acts = []
    for u in urls:
        try:
            r = sess.get(u, timeout=25, allow_redirects=True)
        except Exception as e:
            log(tag, "活动列表请求失败 %s -> %r" % (u[:80], e))
            continue
        try:
            j = r.json()
        except Exception:
            continue
        if isinstance(j, dict) and j.get("errorMsg") == "请用学习通客户端打开活动列表":
            log(tag, "  (被客户端门禁拒：%s)" % u[:60])
            continue
        _walk_active_any(j, acts)
    uniq, seen = [], set()
    for a in acts:
        k = str(a.get("id"))
        if k in seen:
            continue
        seen.add(k)
        uniq.append(a)
    real = [x for x in uniq if RE_REAL_AID.match(str(x.get("id") or ""))]
    if real:
        uniq = real
    return uniq


def _teaview_activities(html):
    """解析教师活动页 widget/active/teaActiveView 里的 var jsonObject = {'activeList':[...]}。
    实测形状（2026-11-15）：每个活动形如
      {'activeId':4000180737792,'activeType':2,'typeTitle':'二维码签到','otherId':2,
       'content':'{\"openCheckFaceFlag\":1,\"locationLatitude\":\"30.7114...\",...}', ...}
    content 是**被转义的 JSON 串**，人脸开关 openCheckFaceFlag 与位置真值都在里面（signDetail 里没有）。"""
    i = html.find("var jsonObject")
    if i < 0:
        return []
    out = []
    for m in re.finditer(r"'activeId'\s*:\s*(\d+)(.*?)(?='activeId'\s*:|$)", html[i:], re.S):
        aid, seg = m.group(1), m.group(2)
        t = re.search(r"'typeTitle'\s*:\s*'([^']*)'", seg)
        at = re.search(r"'activeType'\s*:\s*(\d+)", seg)
        cm = re.search(r"'content'\s*:\s*'((?:[^'\\]|\\.)*)'", seg)
        content = {}
        if cm:
            raw = cm.group(1).replace('\\\\"', '"').replace("\\\\'", "'").replace('\\"', '"')
            try:
                content = json.loads(raw)
            except Exception:
                content = {}
        out.append({"aid": aid, "activeType": (at.group(1) if at else ""),
                    "typeTitle": (t.group(1) if t else ""), "content": content})
    return out


def build_location_json(geo, lat=None, lon=None, address=None):
    """按学生页 JS 的形状拼 location JSON：{"result":1,"address":..,"longitude":..,"latitude":..}
    实测：该串必须同时作为 location 与 locationResult 提交，缺一个 -> errorLocation3。"""
    if not geo:
        geo = {}
    la = str(lat if lat not in (None, "") else (geo.get("latitude") or "")).strip()
    lo = str(lon if lon not in (None, "") else (geo.get("longitude") or "")).strip()
    ad = address if address not in (None, "") else (geo.get("address") or "")
    if not (la and lo):
        return ""
    try:
        d = {"result": 1, "address": ad, "longitude": float(lo), "latitude": float(la)}
    except ValueError:
        return ""
    return json.dumps(d, ensure_ascii=False, separators=(",", ":"))


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


class RiskMixin(object):
    """反封号策略层接线：R1 只读先行 + 双配额 + 目标上限 + 分级熔断 + 全审计。

    rc 为 None 时所有 gate 直接放行（--no-risk-center）。写操作一律先 gate 后 note。
    """

    rc = None

    def risk_init(self, uid, risk=True):
        self.rc = None
        if not risk:
            log("i", "风控：策略层已关闭（--no-risk-center）")
            return
        try:
            from risk_center import RiskCenter
            self.rc = RiskCenter(uid=str(uid or ""))
        except Exception as e:
            log("!", "风控策略层不可用（%r），退回内置闸门" % (e,))

    def risk_probe(self, url, ok=True):
        """登记一次成功只读探针（R1）"""
        if self.rc and ok:
            self.rc.probe(url)

    def risk_gate(self, action, url, target="", progress=None, max_wait=0, quiet=True):
        """写操作前的准入。返回 (ok, why)"""
        if not self.rc:
            return True, ""
        ok, why = self.rc.allow(action, url=url, target=str(target or ""), progress=progress, quiet_check=quiet)
        if not ok and max_wait and any(k in why for k in ("距上次", "小时", "今日", "冷却")):
            log("i", "风控[%s]：%s → 等待放行" % (action, why))
            ok, why = self.rc.wait(action, url=url, target=str(target or ""), max_wait=max_wait, verbose=False)
        if not ok:
            log("!", "风控拦截[%s]：%s" % (action, why))
        return ok, why

    def risk_note(self, action, url, status, body, target="", progress=None, ok=None):
        """写操作后的判级/记账。返回 None 或 {level, reason, action}"""
        if not self.rc:
            return None
        v = self.rc.observe(action, url, status, body, target=str(target or ""), progress=progress, ok=ok)
        if v["action"] in ("HALT", "COOLDOWN"):
            log("!", "风控 %s：%s" % (v["action"], v["reason"][:140]))
        return v


class TeacherSide(RiskMixin):
    """教师侧：班级枚举 -> 活动定位 -> enc 采集"""

    def __init__(self, ck, uid, ua_mode="h5", dump_dir="out/tch_probe", quiet_hours=None,
                 max_writes_per_hour=None, min_interval=None, per_day=None, risk=True):
        if make_session is None:
            raise SystemExit("stealth_session 不可用")
        self.risk_init(uid, risk)
        self.expired = False
        kw = {}
        if max_writes_per_hour:
            kw["max_writes_per_hour"] = max_writes_per_hour
        if min_interval:
            kw["min_interval"] = min_interval
        if per_day:
            kw["per_day"] = per_day
        self.sess = make_session(cookie=ck, uid=uid, referer=MOBILE, ua_mode=ua_mode,
                                 xhr=True, quiet=quiet_hours, **kw)
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
        if r.status_code == 200:
            self.risk_probe(getattr(r, "url", "") or url)     # R1：成功只读 → 本域可写
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
        seen, uniq, dropped = set(), [], []
        for c in out:
            e = (c["enc"] or "").strip()
            low = e.lower()
            if not e or low in PLACEHOLDER_ENC or len(set(low)) <= 2:
                continue
            if not RE_ENC_OK.match(e):
                dropped.append(e[:20])          # JS 模板串/占位符，不是真 enc
                continue
            c["enc"] = e
            if e in seen:
                continue
            seen.add(e)
            uniq.append(c)
        if dropped:
            log("T", "  已丢弃 %d 个非十六进制候选：%s" % (len(dropped), ", ".join(dropped[:3])))
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

    def cpi_for(self, course, clazz):
        """教师在该班的 cpi（taskactivelist 需要；只有 backclazzdata 里有，缓存一次）"""
        if getattr(self, "_cls_cache", None) is None:
            try:
                self._cls_cache = self.classes()
            except Exception:
                self._cls_cache = []
        for c in self._cls_cache:
            if str(c.get("course")) == str(course) and str(c.get("clazz")) == str(clazz):
                return c.get("cpi") or ""
        return ""

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
        if not ALLOW_ANY:
            keep = [c for c in uniq if str(c.get("course")) == ALLOW_COURSE and str(c.get("clazz")) == ALLOW_CLASS]
            if len(keep) != len(uniq):
                log("T", "作用域白名单过滤：%d 个班级里只有 %d 个属于计算机二级测试班（course=%s class=%s），其余不请求"
                    % (len(uniq), len(keep), ALLOW_COURSE, ALLOW_CLASS))
            uniq = keep
        log("T", "教师班级 %d 个" % len(uniq))
        for c in uniq[:20]:
            log("T", "  %s | course=%s class=%s cpi=%s role=%s" % (c.get("name", "?")[:24], c.get("course"),
                                                                  c.get("clazz"), c.get("cpi"), c.get("role")))
        return uniq

    def _walk_classes(self, obj, out, ctx):
        """教师 backclazzdata 有两种形状：
        A) channelList[i].content = {dtype:"Course", id:<courseId>, cpi:<教师cpi>, name, clazz:[{clazzId,...}], person:{data:[{userid}]}}
        B) channelList[i].content = {cpi, chatid:<classId>, name, course:{data:[{id:<courseId>, teacherfactor,...}]}}
        共同的坑：courseId 与 clazzId 从不共存于同一个 dict，必须靠 ctx 向下继承。
        """
        if isinstance(obj, list):
            for it in obj:
                self._walk_classes(it, out, ctx)
            return
        if not isinstance(obj, dict):
            return
        keys = {k.lower(): k for k in obj.keys()}

        def _g(*names):
            for n in names:
                if n in keys:
                    v = obj[keys[n]]
                    if v not in (None, "", 0, "0"):
                        return v
            return None

        course, clazz = ctx.get("course"), ctx.get("clazz")
        cpi, name, role = ctx.get("cpi"), ctx.get("name"), ctx.get("role")

        # --- 课程号 ---
        v = _g("courseid", "course_id", "courseid_str")
        if v and str(v).isdigit():
            course = str(v)
        else:
            # 只有"长这样像课程"的 dict 才允许用裸 id 当 courseId（clazz/person 子 dict 里也有 id/userid）
            looks_course = ("dtype" in keys and str(obj[keys["dtype"]]).lower() == "course") or                            ("teacherfactor" in keys) or ("belongschoolid" in keys) or                            ("sectionid" in keys and "clazzid" not in keys)
            if looks_course and "id" in keys and str(obj[keys["id"]]).isdigit():
                course = str(obj[keys["id"]])
        # --- 班级号 ---
        v = _g("clazzid", "classid", "clazz_id", "class_id", "chatid", "chat_id")
        if v and str(v).isdigit():
            clazz = str(v)
        # --- 教师 cpi / 角色 / 名称 ---
        v = _g("cpi", "personid", "person_id")
        if v and str(v).isdigit():
            cpi = str(v)
        v = _g("roletype", "role", "role_type")
        if v is not None:
            role = str(v)
        v = _g("coursename", "clazzname", "classname")
        if v:
            name = str(v)
        elif not name and _g("name") and len(str(_g("name"))) <= 40:
            name = str(_g("name"))

        newctx = {"course": course, "clazz": clazz, "cpi": cpi, "name": name, "role": role}
        if course and clazz:
            out.append(dict(newctx))
        for v2 in obj.values():
            if isinstance(v2, (dict, list)):
                self._walk_classes(v2, out, newctx)

    # ---- 2) 活动定位 ----
    def activities(self, course=None, clazz=None, cpi=""):
        guard_scope(course, clazz, "活动列表")
        urls = []
        if course and clazz:
            urls.append(MOBILE + "ppt/activeAPI/taskactivelist?courseId=%s&classId=%s&uid=%s&cpi=%s&appType=15"
                        % (course, clazz, self.uid, cpi or ""))
        # 教师本人发起的活动（courseactivelist 的 puid 是发起人 uid；教师 cookie 下才非空）
        urls.append(MOBILE + "ppt/activeAPI/courseactivelist?puid=%s&status=1&page=1&pageSize=20&appType=15" % self.uid)
        urls.append(MOBILE + "ppt/activeAPI/courseactivelist?puid=%s&status=0&page=1&pageSize=20&appType=15" % self.uid)
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
            d = r.json()
        except Exception:
            return {}
        sc_course = d.get("courseId") or d.get("courseid")
        sc_clazz = d.get("clazzId") or d.get("clazzid") or d.get("classId")
        if not ALLOW_ANY and (sc_course or sc_clazz):
            guard_scope(sc_course, sc_clazz, "signDetail aid=%s" % aid)
        return d

    # ---- 定位类活动：位置真值只在活动列表页的 content JSON 里（signDetail 只有 latitude=-1）----
    def activity_geo(self, aid, course=None, clazz=None):
        """GET widget/active/teaActiveView -> 解析 var jsonObject = {'activeList':[...]} -> 取该 aid 的 content JSON
        content 里 locationText/locationLatitude/locationLongitude/locationRange/ifopenAddress 就是位置真值。
        返回 {'latitude','longitude','address','range','ifopenAddress','face'} 或 {}。"""
        guard_scope(course, clazz, "教师活动页 aid=%s" % aid)
        if not (course and clazz):
            return {}
        u = (MOBILE + "widget/active/teaActiveView?DB_STRATEGY=COURSEID&STRATEGY_PARA=courseId"
                     "&courseId=%s&classId=%s&uid=%s&appType=15" % (course, clazz, self.uid))
        try:
            r = self.sess.get(u, timeout=25)
        except Exception as e:
            log("T", "teaActiveView 失败 -> %r" % (e,))
            return {}
        html = r.text or ""
        for a in _teaview_activities(html):
            if str(a.get("aid")) == str(aid):
                c = a.get("content") or {}
                geo = {"latitude": c.get("locationLatitude"), "longitude": c.get("locationLongitude"),
                       "address": c.get("locationText"), "range": c.get("locationRange"),
                       "ifopenAddress": c.get("ifopenAddress"), "face": c.get("openCheckFaceFlag"),
                       "text": a.get("typeTitle")}
                log("T", "aid=%s type=%s ifopenAddress=%s face=%s range=%s addr=%s"
                    % (aid, a.get("typeTitle"), geo.get("ifopenAddress"), geo.get("face"),
                       geo.get("range"), str(geo.get("address"))[:24]))
                return geo
        log("T", "teaActiveView 里没找到 aid=%s（可能不在本班活动列表）" % aid)
        return {}

    # ---- ★ 创建签到（教师"发起签到"页 /pptSign/newTaskSign；type=0 保存 / type=1 立即开始）----
    def create_sign(self, course, clazz, other_id="2", face="0", ifopen_address="0", time_long="1800000",
                    start=True, title="", code="", location=None, if_need_vcode="0", late_minute="10",
                    if_photo=None,
                    if_refresh_ewm="1", ewm_refresh_time="5", verbose=True):
        """实测：POST /pptSign/newTaskSign，form 字段 60+ 个（来自教师页 var url = "/pptSign/newTaskSign"，
        与 /newsign/saveSign 同构；本机 /newsign/saveSign 返回 404）。
        返回 {"activeName":"","_activeId":4000180742552,...}；type=1 = 立即开始（type=0 只保存，refreshQRCode 会报"活动未开始"）。
        otherId：0 普通 / 1 拍照(ifPhoto=1) / 2 二维码 / 3 手势 / 4 位置 / 5 签到码。
        openCheckFaceFlag=0 即不扫脸；ifopenAddress=1 时需带 locationText/lat/lon/range。
        失败形状：{"result":0,"msg":"..."}（此时 log 并返回空串）。"""
        guard_scope(course, clazz, "创建签到")
        loc = location or {}
        if not title:
            title = SIGN_TYPE_TITLE.get(str(other_id), "二维码签到")
        if not code:
            code = str(random.randint(100000, 999999))
        p = {
            "classId": str(clazz), "courseId": str(course), "puid": self.uid, "source": "1",
            "type": "1" if start else "0", "otherId": str(other_id), "isResult": "0", "code": code,
            "latitude": "-1", "longitude": "-1", "activePrimaryId": "0", "timeLong": str(time_long),
            "ifSendMessage": "1", "ifGetRange": "0", "crnum": "", "planId": "", "appType": "15",
            "activePrimaryId1": "0", "clone": "0", "classIds": "",
            "ifPhoto": ("1" if str(if_photo) == "1" else "0") if if_photo is not None else ("1" if str(other_id) == "1" else "0"),
            "circleId": "", "tid": "", "uid": self.uid, "title": title,
            "ifRefreshEwm": str(if_refresh_ewm), "ewmRefreshTime": str(ewm_refresh_time),
            "asynKey": "0", "asynId": "", "foreignType": "", "classroomDataId": "", "foreignId": "",
            "picId": "", "isCourseware": "", "activityTranMode": "", "isPPTLibrary": "",
            "isTeachingCalendar": "", "classroomPlanId": "", "pageNum": "", "pageId": "",
            "ifOpenTimer": "0", "timerCron": "", "dateCron": "", "disposable_publishtime": "",
            "validity_begintime": "", "validity_endtime": "", "ifSkipWeek": "0",
            "ifopenAddress": str(ifopen_address), "locationText": loc.get("address", ""),
            "locationLatitude": loc.get("latitude", ""), "locationLongitude": loc.get("longitude", ""),
            "locationRange": loc.get("range", ""), "fromtype": "", "nowtimestamp": str(int(time.time() * 1000)),
            "ifSendToOtherClass": "0", "sendToOtherClassList": "", "fyktBigClassChatId": "",
            "ifNeedVCode": str(if_need_vcode), "onlyAttendForCurrentClass": "0", "lateMinute": str(late_minute),
            "openSignOutFlag": "0", "signOutRelativeTime": "", "signOutAbsoluteTime": "", "signOutDuration": "",
            "openCheckFaceFlag": str(face), "fykbParams": "", "openCheckWeChatFlag": "0",
        }
        wurl = MOBILE + "pptSign/newTaskSign"
        ok, why = self.risk_gate("tch_write", wurl, target=str(course), max_wait=60)
        if not ok and "R1" in why:
            try:      # 自愈：先补一次只读探针
                self.get(MOBILE + "pptSign/gotasksign?courseId=%s&classId=%s&uid=%s&appType=15"
                         % (course, clazz, self.uid), tag="riskprobe", sniff=False)
            except Exception:
                pass
            ok, why = self.risk_gate("tch_write", wurl, target=str(course), max_wait=60)
        if not ok:
            return ""
        try:
            r = self.sess.post(wurl, data=p, timeout=30,
                               headers={"X-Requested-With": "XMLHttpRequest"})
            body = (r.text or "").strip()
            j = r.json()
        except Exception as e:
            log("T", "创建签到失败 -> %r" % (e,))
            return ""
        self.risk_note("tch_write", wurl, getattr(r, "status_code", 0), body, target=str(course),
                       ok=bool(j.get("_activeId")))
        if str(j.get("result")) == "0" or not j.get("_activeId"):
            log("T", "创建签到被拒：%s" % body[:200])
            return ""
        aid = str(j.get("_activeId"))
        log("+", "已创建签到 aid=%s type=%s(立即开始=%s) 扫脸=%s 定位=%s 时长=%sms title=%s code=%s"
            % (aid, other_id, start, face, ifopen_address, time_long, title, code))
        return aid

    def refresh_qrcode(self, aid):
        """★ 教师侧权威接口：/v2/apis/sign/refreshQRCode?activeId=&time=  ->  {"result":1,"data":{"refresh":1,"enc":"...","signCode":"..."}}
        （来自教师签到页 JS updateEwm()，10s 轮换；旧名 /widget/sign/pcTeaSignController/getSignCode 已被注释掉）
        返回 {'enc','c','signCode','aid'} 或 {}。"""
        u = MOBILE + "v2/apis/sign/refreshQRCode?activeId=%s&time=%d" % (aid, int(time.time() * 1000))
        try:
            r = self.sess.get(u, timeout=25, allow_redirects=True)
        except Exception as e:
            log("T", "refreshQRCode 失败 aid=%s -> %r" % (aid, e))
            return {}
        body = (r.text or "").strip()
        try:
            j = r.json()
        except Exception:
            log("T", "refreshQRCode 非 JSON (HTTP %s): %s" % (r.status_code, body[:120]))
            return {}
        if str(j.get("result")) != "1" or not isinstance(j.get("data"), dict):
            log("T", "refreshQRCode aid=%s -> result=%s errorMsg=%s" % (aid, j.get("result"), j.get("errorMsg")))
            return {}
        d = j["data"]
        enc = (d.get("enc") or "").strip()
        if not enc:
            return {}
        return {"enc": enc, "c": str(d.get("signCode") or ""), "signCode": str(d.get("signCode") or ""),
                "aid": str(aid), "refresh": d.get("refresh"), "src": "refreshQRCode"}

    def qr_candidates(self, aid, course=None, clazz=None):
        """教师侧全路径扫一遍，返回 [{'enc','aid','c','src'}]"""
        guard_scope(course, clazz, "取 enc aid=%s" % aid)
        # ① 权威接口优先
        top = self.refresh_qrcode(aid)
        if top:
            log("+", "refreshQRCode aid=%s -> enc=%s.. signCode=%s refresh=%s"
                % (aid, top["enc"][:12], top.get("signCode"), top.get("refresh")))
        urls = []
        if course and clazz:
            urls.append(MOBILE + "pptSign/gotasksign?courseId=%s&classId=%s&activePrimaryId=%s&source=1&isTeacherViewOpen=1"
                        % (course, clazz, aid))
            urls.append(MOBILE + "newsign/preSign?activePrimaryId=%s&sys=1&chatId=&general=&ls=1&appType=15"
                                 "&courseId=%s&classId=%s&uid=%s&isTeacherViewOpen=1" % (aid, course, clazz, self.uid))
        urls.append(MOBILE + "sign/produceSignView?tid=%s&uid=%s&appType=15" % (self.uid, self.uid))
        cands = [top] if top else []
        for u in urls:
            if top:
                break                      # 已经拿到权威 enc，不必再把教师页面全抓一遍
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
        if c.get("src") == "refreshQRCode":
            s += 8                        # 服务端权威接口，胜过一切页面嗅探
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


class StudentSide(RiskMixin):
    def __init__(self, ck, uid, ua_mode="h5", quiet_hours=None,
                 max_writes_per_hour=None, min_interval=None, per_day=None, risk=True):
        self.risk_init(uid, risk)
        kw = {}
        if max_writes_per_hour:
            kw["max_writes_per_hour"] = max_writes_per_hour
        if min_interval:
            kw["min_interval"] = min_interval
        if per_day:
            kw["per_day"] = per_day
        self.sess = make_session(cookie=ck, uid=uid, referer=MOBILE, ua_mode=ua_mode,
                                 xhr=True, quiet=quiet_hours, **kw)
        self.uid = uid

    def touch(self):
        """只读探针（R1 只读先行）：GET 一次签到页，成功后本域才允许写。"""
        url = MOBILE + "pptSign/gotasksign?uid=%s&appType=15" % self.uid
        try:
            r = self.sess.get(url, timeout=20)
            self.risk_probe(getattr(r, "url", "") or url, ok=(r.status_code == 200))
            return r.status_code
        except Exception as e:
            log("T", "风控探针失败 -> %r" % (e,))
            return 0

    def risk_write_gate(self, action, url, target="", progress=None, max_wait=90):
        ok, why = self.risk_gate(action, url, target=target, progress=progress, max_wait=max_wait)
        if not ok and "R1" in why:
            self.touch()
            ok, why = self.risk_gate(action, url, target=target, progress=progress, max_wait=max_wait)
        return ok, why

    def submit(self, aid, enc, name="", fid="0", lat="-1", lon="-1", verbose=True, extra=None,
               location="", location_result=""):
        """提交签到。定位类活动必须**同时**带 location 与 locationResult（同一个 JSON 串）：
           实测只带 location -> errorLocation3；location+locationResult -> success。
           location JSON 形状（学生页 JS 原文）：{"result":1,"address":..,"longitude":..,"latitude":..}"""
        surl = MOBILE + "pptSign/stuSignajax"
        ok, why = self.risk_write_gate("sign_probe", surl, target=str(aid))
        if not ok:
            return {"status": "RISK_BLOCKED", "raw": why, "body": why}
        if _submit_url is not None and not extra and not location_result:
            content = "https://x/?enc=%s&id=%s" % (urllib.parse.quote(enc), urllib.parse.quote(str(aid)))
            res = _submit_url(self.sess, content, self.uid, name, fid, lat, lon, verbose=verbose)
            return _classify(res) if isinstance(res, dict) else res
        params = [("enc", enc), ("name", name), ("activeId", str(aid)), ("uid", self.uid),
                  ("clientip", ""), ("useragent", ""), ("latitude", lat), ("longitude", lon),
                  ("fid", fid), ("appType", "15")]
        if location:
            params.append(("location", location))
        if location_result:
            params.append(("locationResult", location_result))
        q = "pptSign/stuSignajax?" + urllib.parse.urlencode(params)
        if location_result:
            r = self.sess.post(MOBILE + "pptSign/stuSignajax", data=dict(params), timeout=20)
        else:
            r = self.sess.get(MOBILE + q, timeout=20)
        body = (r.text or "").strip()
        if verbose:
            log("S", "%s %s" % (r.request.method if getattr(r, "request", None) is not None else "GET", MOBILE + q))
            log("S", "HTTP %s  %s" % (r.status_code, body[:300]))
        ok = ("success" in body.lower()) or ("签到成功" in body)
        self.risk_note("sign_probe", surl, r.status_code, body, target=str(aid), ok=ok)
        return _classify({"ok": ok, "msg": body[:300]})

    # ---- 学生侧活动列表（扫码/普通/定位等活动的真实列表在学生视角下最全）----
    def activities(self, course=None, clazz=None, cpi=""):
        guard_scope(course, clazz, "学生活动列表")
        urls = []
        if course and clazz:
            urls.append(MOBILE + "ppt/activeAPI/taskactivelist?courseId=%s&classId=%s&uid=%s&cpi=%s&appType=15"
                        % (course, clazz, self.uid, cpi or ""))
            urls.append(MOBILE + "ppt/activeAPI/courseactivelist?puid=%s&status=1&page=1&pageSize=20&appType=15" % self.uid)
        else:
            urls.append(MOBILE + "ppt/activeAPI/courseactivelist?puid=%s&status=1&page=1&pageSize=20&appType=15" % self.uid)
        acts = _list_activities(self.sess, self.uid, urls, "S")
        log("S", "学生活动 %d 条" % len(acts))
        for x in acts[:12]:
            log("S", "  aid=%s type=%s status=%s %s" % (x.get("id"), x.get("activeType"), x.get("status"),
                                                        str(x.get("name") or "")[:26]))
        return acts

    # ---- 人脸闸门（checkFace_<enc2> 之后的两步）----
    def face_result(self, aid, face_result_json, verbose=True):
        """② POST /pptSign/check-face-result?DB_STRATEGY=PRIMARY_KEY&STRATEGY_PARA=activeId
        教师页/学生页 JS 里的调用：data={activeId, faceResult: JSON.stringify(faceResult)} -> 返回 {enc, code}
        faceResult 本体是 App 侧人脸 SDK（CLIENT_FACE_RECOGNITION_BLINK, funTag=3）的产物。"""
        u = MOBILE + "pptSign/check-face-result?DB_STRATEGY=PRIMARY_KEY&STRATEGY_PARA=activeId"
        try:
            r = self.sess.post(u, data={"activeId": str(aid), "faceResult": face_result_json}, timeout=25)
            body = (r.text or "").strip()
            if verbose:
                log("S", "POST check-face-result -> HTTP %s %s" % (r.status_code, body[:200]))
            return r.json() if body.startswith("{") else {}
        except Exception as e:
            log("!", "check-face-result 失败: %r" % (e,))
            return {}

    def submit_face(self, aid, enc, enc2, face_enc, face_code, current_face_id="", name="", fid="0",
                    course="", address="", verbose=True):
        """③ 带人脸结果重提：enc2 + faceEnc/faceCode/faceEncAid + currentFaceId + ifCFP=1"""
        q = ("pptSign/stuSignajax?enc=%s&name=%s&activeId=%s&uid=%s&clientip=&useragent="
             "&latitude=-1&longitude=-1&fid=%s&appType=15&enc2=%s&currentFaceId=%s&ifCFP=1"
             "&courseId=%s&faceEnc=%s&faceCode=%s&faceEncAid=%s"
             % (urllib.parse.quote(enc), urllib.parse.quote(name), urllib.parse.quote(str(aid)),
                urllib.parse.quote(self.uid), urllib.parse.quote(fid), urllib.parse.quote(enc2),
                urllib.parse.quote(current_face_id), urllib.parse.quote(str(course)),
                urllib.parse.quote(face_enc), urllib.parse.quote(face_code), urllib.parse.quote(str(aid))))
        if address:
            q += "&address=" + urllib.parse.quote(address)
        surl = MOBILE + "pptSign/stuSignajax"
        ok, why = self.risk_write_gate("sign", surl, target=str(aid))
        if not ok:
            return {"status": "RISK_BLOCKED", "raw": why, "body": why}
        r = self.sess.get(MOBILE + q, timeout=25)
        body = (r.text or "").strip()
        if verbose:
            log("S", "GET %s" % (MOBILE + q)[:230])
            log("S", "HTTP %s  %s" % (r.status_code, body[:200]))
        self.risk_note("sign", surl, r.status_code, body, target=str(aid),
                       ok=("success" in body.lower()))
        return _classify({"ok": ("success" in body.lower()), "msg": body[:300]})


def _classify(res):
    """把服务端的响应分成几种闸门：checkFace_/validate_ 都不是普通失败，而是
    'enc 已经过关，但还要过人脸/验证码'——这是本次实签能走到的最深一层。"""
    if not isinstance(res, dict):
        return res
    msg = str(res.get("msg") or res.get("body") or "").strip()
    if msg.startswith("checkFace_"):
        res["gate"] = "face"
        res["enc2"] = msg[len("checkFace_"):]
        res["ok"] = False
    elif msg.startswith("validate_"):
        res["gate"] = "captcha"
        res["enc2"] = msg[len("validate_"):]
        res["ok"] = False
    return res


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
    global ALLOW_COURSE, ALLOW_CLASS, ALLOW_ANY
    ap = argparse.ArgumentParser(description="学习通 教师侧取码 -> 学生侧提交 一体化流水线")
    ap.add_argument("--mode", default="watch", choices=["discover", "once", "watch", "submit-url", "create"])
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
    ap.add_argument("--allow-course", default=ALLOW_COURSE, help="作用域白名单：允许的 courseId")
    ap.add_argument("--allow-class", default=ALLOW_CLASS, help="作用域白名单：允许的 clazzId")
    ap.add_argument("--allow-any-class", action="store_true", help="解除班级白名单（默认禁止，需显式开启）")
    ap.add_argument("--create-type", default="", help="create 模式：otherId（0 普通/1 拍照/2 二维码/3 手势/4 位置/5 签到码），默认取 --want-type 第一个")
    ap.add_argument("--allow-no-enc", action="store_true",
                    help="允许在取不到 enc 时提交（位置/普通签到服务端不校验 enc；实测位置签到用空 enc 也能入库）")
    ap.add_argument("--no-face", dest="face", action="store_false", default=False, help="create 模式：openCheckFaceFlag=0（默认就是不扫脸）")
    ap.add_argument("--face", dest="face", action="store_true", help="create 模式：开启人脸")
    ap.add_argument("--sign-address", dest="sign_address", action="store_true", default=False,
                    help="create 模式：ifopenAddress=1（需要位置；位置取自 --lat/--lon/--address）")
    ap.add_argument("--time-long", type=int, default=1800000, help="create 模式：签到时长 ms（默认 30 分钟）")
    ap.add_argument("--save-only", action="store_true", help="create 模式：只保存不开始（type=0，此时取不到 enc）")
    ap.add_argument("--auto-create", action="store_true", help="没有可用活动时自动创建（用上面的 create 参数，不扫脸）")
    ap.add_argument("--geo", dest="geo", action="store_true", default=True,
                    help="定位类活动自动从活动 content 取位置并带 location/locationResult（默认开）")
    ap.add_argument("--no-geo", dest="geo", action="store_false", help="关闭位置自动填参")
    ap.add_argument("--lat", default="", help="覆盖纬度（默认取活动 content 的 locationLatitude）")
    ap.add_argument("--lon", default="", help="覆盖经度（默认取活动 content 的 locationLongitude）")
    ap.add_argument("--address", default="", help="覆盖地址文本（默认取活动 content 的 locationText）")
    ap.add_argument("--max-writes-per-hour", type=int, default=0, help="覆盖风控写配额（0=用默认 6/小时）")
    ap.add_argument("--min-interval", type=float, default=0, help="覆盖最小写间隔秒（0=用默认 8s）")
    ap.add_argument("--no-risk-center", action="store_true",
                    help="关闭反封号策略层（默认开启：只读先行/双配额/目标上限/熔断/审计）")
    ap.add_argument("--verbose", action="store_true")
    a = ap.parse_args()

    ALLOW_COURSE, ALLOW_CLASS = str(a.allow_course), str(a.allow_class)
    ALLOW_ANY = bool(a.allow_any_class)
    guard_scope(a.course, a.clazz, "命令行参数")     # 越界参数在联网前就拦下
    if not ALLOW_ANY:
        log("i", "作用域白名单生效：只允许 course=%s class=%s（--allow-any-class 可解除）"
            % (ALLOW_COURSE, ALLOW_CLASS))

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
        st = StudentSide(stu_ck, a.uid, a.ua_mode, quiet_hours=parse_quiet(a.quiet_hours),
                     max_writes_per_hour=a.max_writes_per_hour, min_interval=a.min_interval,
                          risk=not getattr(a, "no_risk_center", False))
        _submit_url(st.sess, a.qr, a.uid, a.name, a.fid, verbose=True)
        return 0

    tch_uid = a.tch_uid
    if not tch_uid and tch_ck:
        m = re.search(r"(?:^|;\s*)_uid=([0-9]+)", tch_ck)
        tch_uid = m.group(1) if m else ""
    if a.mode == "once" and not a.rounds:
        a.rounds = 1                      # once = 只跑一轮（否则会进 watch 无限循环）
    if not getattr(a, "no_risk_center", False):
        # 策略层开启时，把旧 stealth_session 的"全局 6 次/小时"放宽，
        # 让配额由 risk_center 按动作分档（sign 6/h、sign_probe 30/h、tch_write 30/h、read 600/h）
        if not a.max_writes_per_hour:
            a.max_writes_per_hour = 120
        if not a.min_interval:
            a.min_interval = 0
    qh = parse_quiet(a.quiet_hours)
    tch = TeacherSide(tch_ck, tch_uid or a.uid, a.ua_mode, a.dump_dir, quiet_hours=qh,
                       max_writes_per_hour=a.max_writes_per_hour, min_interval=a.min_interval,
                          risk=not getattr(a, "no_risk_center", False)) if tch_ck else None
    stu = StudentSide(stu_ck, a.uid, a.ua_mode, quiet_hours=qh,
                       max_writes_per_hour=a.max_writes_per_hour, min_interval=a.min_interval,
                          risk=not getattr(a, "no_risk_center", False)) if (stu_ck and not a.dry_run) else None
    stu_list = StudentSide(stu_ck, a.uid, a.ua_mode, quiet_hours=qh,
                            max_writes_per_hour=a.max_writes_per_hour, min_interval=a.min_interval,
                          risk=not getattr(a, "no_risk_center", False)) if stu_ck else None   # 只读的活动列表用

    if tch and warmup and not a.dry_run and a.mode == "watch":
        try:
            warmup(stu.sess if stu else tch.sess, uid=a.uid, quiet=True)
        except Exception:
            pass

    if a.mode == "create":
        if not tch:
            raise SystemExit("create 模式需要教师 cookie（--tch-cookie-file）")
        cid, cl = a.course, a.clazz
        if not (cid and cl):
            cls = tch.classes()
            if not cls:
                raise SystemExit("取不到班级：请加 --course/--class")
            cid, cl = cls[0]["course"], cls[0]["clazz"]
            tch.uid = tch.uid
        ctype = a.create_type or (sorted(want)[0] if want else "2")
        if a.sign_address:
            a.allow_no_enc = True          # 位置签到没有二维码，enc 取不到是正常的
        loc = {}
        if a.sign_address:
            loc = {"address": a.address, "latitude": a.lat, "longitude": a.lon,
                   "range": "500米"}
            if not (a.lat and a.lon):
                log("!", "位置签到需要 --lat/--lon（或先跑一次让它从活动 content 里取）")
        new_aid = tch.create_sign(cid, cl, other_id=ctype, face="1" if a.face else "0",
                                  ifopen_address="1" if a.sign_address else "0",
                                  time_long=a.time_long, start=not a.save_only, location=loc)
        if not new_aid:
            raise SystemExit("创建失败（看上面的服务端返回）")
        a.aid = new_aid
        log("i", "新建签到 aid=%s；进入取码+提交流程" % new_aid)

    if a.mode == "discover":
        if not tch:
            log("!", "没有教师 cookie：只能做学生侧活动列表。请把教师浏览器 cookie 存成 ck_tch.txt")
        if tch:
            cls = tch.classes()
            for c in cls[:6]:
                tch.activities(c["course"], c["clazz"], c.get("cpi") or "")
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
                tch = TeacherSide(tch_ck, tch_uid or a.uid, a.ua_mode, a.dump_dir, quiet_hours=qh,
                                       max_writes_per_hour=a.max_writes_per_hour, min_interval=a.min_interval,
                          risk=not getattr(a, "no_risk_center", False))
        if tch:
            tch.round = rnd
        try:
            cands = []
            if a.enc and a.aid:
                cands = [{"enc": a.enc, "aid": a.aid, "c": "", "src": "cli"}]
            elif tch:
                aids = [a.aid] if a.aid else []
                if a.auto_create and not aids and tch and a.course and a.clazz:
                    _na = tch.create_sign(a.course, a.clazz,
                                          other_id=(a.create_type or (sorted(want)[0] if want else "2")),
                                          face="1" if a.face else "0",
                                          ifopen_address="1" if a.sign_address else "0",
                                          time_long=a.time_long, start=True)
                    if _na:
                        aids = [_na]
                if not aids:
                    _cpi = tch.cpi_for(a.course, a.clazz) if (a.course and a.clazz) else ""
                    acts = tch.activities(a.course or None, a.clazz or None, _cpi)
                    if not acts and stu_list is not None:
                        log("i", "教师视角活动列表为空，改用学生视角（同一课程，真实列表在学生侧）")
                        acts = stu_list.activities(a.course or None, a.clazz or None, _cpi)
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
            if not uniq and a.allow_no_enc and a.aid and stu is not None:
                # 只有位置签到这类"没有二维码"的活动才不校验 enc；二维码签到空 enc 会被服务端拒（签到失败，请重新扫描）
                _geo_ok = True
                if tch:
                    try:
                        _g = tch.activity_geo(a.aid, a.course or None, a.clazz or None) or {}
                        _geo_ok = str(_g.get("ifopenAddress", "")) == "1"
                        if not _geo_ok:
                            log("!", "--allow-no-enc：活动 %s 不是位置签到（ifopenAddress=%s），二维码类必须有真 enc，跳过本轮"
                                % (a.aid, _g.get("ifopenAddress")))
                    except Exception as e:
                        log("-", "no-enc 前置检查失败：%r（按位置类继续）" % (e,))
                if _geo_ok:
                    log("i", "--allow-no-enc：该活动不校验 enc（位置类），用空 enc 提交 aid=%s" % a.aid)
                    uniq = [{"enc": "", "aid": a.aid, "c": "", "src": "no-enc"}]
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
                    _aid = c["aid"] or a.aid
                    # 定位类活动：位置真值只在活动列表页 content 里；location 与 locationResult 必须同值
                    loc_js = ""
                    if a.geo and tch:
                        try:
                            geo = tch.activity_geo(_aid, a.course or None, a.clazz or None)
                            loc_js = build_location_json(geo, a.lat, a.lon, a.address)
                            if loc_js:
                                log("i", "定位参数：location/locationResult=%s" % loc_js[:120])
                        except Exception as e:
                            log("-", "取位置失败：%r" % (e,))
                    res = stu.submit(_aid, c["enc"], a.name, a.fid, verbose=True,
                                     location=loc_js, location_result=loc_js)
                    if (not loc_js) and isinstance(res, dict) and "errorLocation" in str(res.get("msg") or "") and tch:
                        log("i", "服务端要位置（%s），改用活动 content 里的位置重提" % res.get("msg"))
                        try:
                            geo = tch.activity_geo(_aid, a.course or None, a.clazz or None)
                            loc_js = build_location_json(geo, a.lat, a.lon, a.address)
                        except Exception as e:
                            log("-", "取位置失败：%r" % (e,))
                        if loc_js:
                            n_submit += 1
                            log("i", "重提 location/locationResult=%s" % loc_js[:120])
                            res = stu.submit(_aid, c["enc"], a.name, a.fid, verbose=True,
                                             location=loc_js, location_result=loc_js)
                    rec(a.log, {"t": ts(), "round": rnd, "event": "submit", "enc": (c["enc"] or "(none)")[:16],
                                "aid": c["aid"] or a.aid, "src": c["src"], "ok": res.get("ok"),
                                "msg": str(res.get("msg"))[:120]})
                    if isinstance(res, dict) and res.get("gate") == "face":
                        log("!", "闸门=人脸：enc 已通过！服务端返回 checkFace_%s" % (res.get("enc2") or "")[:16])
                        log("i", "  后续两步：① App 人脸采集 -> ② POST /pptSign/check-face-result -> ③ submit_face(enc2, faceEnc, faceCode)")
                    if isinstance(res, dict) and res.get("gate") == "captcha":
                        log("!", "闸门=验证码：enc 已通过！服务端返回 validate_%s" % (res.get("enc2") or "")[:16])
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
