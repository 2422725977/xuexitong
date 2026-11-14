#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""学习通视频任务点（播放进度上报）协议客户端。

来源：解壳 dex 反编译（chaoxing/out/cvm.txt、out/video_b.txt、out/video_d.txt）。
链路三步：

  1) 章节卡片  GET https://mooc1-api.chaoxing.com/knowledge/cards
                 ?clazzid=&courseid=&knowledgeid=&num=&isPhone=1&control=&cpi=
  2) 视频任务  GET https://mooc1-api.chaoxing.com/ananas/job
                 ?jobid=&knowledgeid=&courseid=&clazzid=&jtoken=
     → JSON 字段：objectid / duration / reportUrl / rt / otherInfo /
                  vbegin / vend / jobid / clazzId / reportTimeInterval(默认60)
  3) 进度上报  GET {reportUrl}?otherInfo=&playingTime=&duration=&akid=null&jobid=
                 &clipTime=&clazzId=&objectId=&userid=&isdrag=&enc=&rt=&dtype=Video&view=json

  enc = md5( "[clazzId][puid][jobid][objectId][playingTime_ms][SALT][duration_ms][clipTime]" )
        playingTime_ms = floor(playing_ms/1000)*1000   （秒粒度再乘 1000）
        duration_ms    = duration * 1000
        clipTime       = "vbegin_vend"（vbegin>=0 且 vend>0）否则 "0_duration"
        playingTime 参数本身是**秒**（drag 时是 "clipStart秒-playingTime秒"）

  服务端判定（CourseDotRes，gson 反序列化）：
      result = 1    → 上报成功
      result = 203   → 成功，但服务端可能要求回退：
                        rollbackStatus=true 且 rollbackPoint>=0 时，客户端会把播放位置拉回该秒数
      result = 0    → 失败（网络异常，客户端显示重试容器）

用法示例：
  # 1) 先看这节课有哪些视频任务（要 cookie）
  python3 scripts/video_task.py --uid <puid> --cookie-file ck.txt \
      --course-id 233333 --clazz-id 666666 --knowledge-id 888888 --list

  # 2) 拿任务信息 + 干跑（不发请求，只打印 URL 与 enc）
  python3 scripts/video_task.py --uid <puid> --cookie-file ck.txt \
      --course-id 233333 --clazz-id 666666 --knowledge-id 888888 --job-id 1234567 --dry-run

  # 3) 真正上报（默认按 60 秒一格、与真实播放同速；--speed 2 则是两倍速）
  python3 scripts/video_task.py --uid <puid> --cookie-file ck.txt --job-json job.json \
      --stealth --speed 1.0

  # 4) 只在已知 reportUrl 时直报（例如从 frida 抓到）
  python3 scripts/video_task.py --uid <puid> --cookie-file ck.txt \
      --report-url 'https://...' --clazz-id K --object-id O --job-id J --duration 900 --rt 0.5

  # 5) 校验：把 frida 抓到的明文/enc 对喂进来，验证本地公式
  python3 scripts/video_task.py --verify-capture cap.json

风控/伪装：--stealth 走 stealth_session（设备档案 + TLS 指纹 + 拟人延迟 + 掩护流量），
并受写速率闸门约束；命中风控打印 [STOP]/[WAIT] 后停手。
"""
import argparse
import hashlib
import json
import os
import re
import sys
import time
from pathlib import Path
from urllib.parse import urlencode, quote

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

# ---- 默认值（可用 --salt / --salt-smali / --salt-apk 覆盖）-------------------
SALT_DEFAULT = "d_yHJ!$pdA~5"
FMT_QUERY = ("?otherInfo=%s&playingTime=%s&duration=%d&akid=null&jobid=%s&clipTime=%s"
             "&clazzId=%s&objectId=%s&userid=%s&isdrag=%d&enc=%s&rt=%s&dtype=Video&view=json")
HOST_API = "https://mooc1-api.chaoxing.com/"
PATH_CARDS = "knowledge/cards?clazzid=%s&courseid=%s&knowledgeid=%s&num=%s&isPhone=%d&control=%s&cpi=%s"
PATH_JOB = "ananas/job?jobid=%s&knowledgeid=%s&courseid=%s&clazzid=%s&jtoken=%s"

try:
    from stealth_session import (make_session, warmup, human_delay, explain as stealth_explain,
                                 HAVE_CFFI, RiskHalt, RiskCooldown, parse_quiet)
    HAVE_STEALTH = True
except Exception:  # 独立运行时的兜底
    HAVE_STEALTH = False
    HAVE_CFFI = False

    class RiskHalt(RuntimeError):
        pass

    class RiskCooldown(RuntimeError):
        pass

    def parse_quiet(s):
        return None

    def make_session(*a, **kw):
        import requests
        return requests.Session()

    def warmup(*a, **kw):
        return 0

    def human_delay(*a, **kw):
        return 0.0

    def stealth_explain(*a, **kw):
        return (0, "无伪装层")


# ---------------------------------------------------------------- 盐与 enc
def derive_salt_from_smali(text):
    """从 CourseViewModel.smali 的 S 方法里取出视频上报用的盐。

    方法体里 const-string 的候选只有 [、][、]、_、0_、查询模板和**盐**；
    盐的特征：长度 6-32、含非字母数字字符、且不是分隔符。
    """
    m = re.search(r"^\.method .*? S\(.*?$", text, re.M)
    if not m:
        return None
    end = text.find(".end method", m.start())
    body = text[m.start():end if end > 0 else len(text)]
    for c in re.findall(r"const-string(?:/jumbo)? v\d+, (.+)$", body, re.M):
        c = c.strip()
        if c in ("[", "][", "]", "_", "0_", "-", ""):
            continue
        if "akid=null" in c or c.startswith("?"):
            continue
        if 6 <= len(c) <= 32 and any(not ch.isalnum() for ch in c):
            return c
    return None


def salt_from_smali_file(path):
    try:
        return derive_salt_from_smali(Path(path).read_text(errors="replace"))
    except Exception:
        return None


def salt_from_apk(apk, droidasc="droidasc", cls="com.chaoxing.mobile.player.course.viewmodel.CourseViewModel"):
    """调用 droidasc 反编译出 smali，再抽取盐。"""
    import subprocess
    import tempfile
    try:
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "cvm.smali"
            with open(out, "w") as fh:
                subprocess.run([droidasc, "disassemble", apk, cls], stdout=fh,
                               stderr=subprocess.DEVNULL, check=False, timeout=600)
            smali = salt_from_smali_file(out)
            if smali:
                return smali
            # 退而求其次：整个 apk 里找唯一的 {{...}} 形态
            data = Path(apk).read_bytes()
            for m in re.finditer(rb"\{\{[ -~]{4,40}?\}\}", data):
                return m.group(0).decode()
    except Exception:
        return None
    return None


def md5_hex(s):
    return hashlib.md5(s.encode("utf-8")).hexdigest()


def enc_plain(clazz_id, puid, job_id, object_id, playing_sec, duration_sec, clip_time, salt):
    return "[%s][%s][%s][%s][%d][%s][%d][%s]" % (
        clazz_id, puid, job_id or "", object_id,
        int(playing_sec) * 1000, salt, int(duration_sec) * 1000, clip_time)


def make_enc(clazz_id, puid, job_id, object_id, playing_sec, duration_sec, clip_time, salt):
    return md5_hex(enc_plain(clazz_id, puid, job_id, object_id, playing_sec, duration_sec, clip_time, salt))


def clip_time_of(vbegin, vend, duration):
    if vbegin is None or vend is None:
        return "0_%d" % int(duration)
    if vbegin < 0 or vend <= 0:
        return "0_%d" % int(duration)
    return "%d_%d" % (int(vbegin), int(vend))


def build_report_url(report_url, other_info, playing_sec, duration, job_id, clip, clazz_id,
                     object_id, puid, isdrag, enc, rt, raw=False):
    """拼出上报 URL。raw=True 时复刻客户端的 String.format（不做 URL 编码）。"""
    if raw:
        return report_url + FMT_QUERY % (other_info or "", playing_sec, int(duration),
                                        job_id or "", clip, clazz_id, object_id, puid,
                                        int(isdrag), enc, rt)
    q = urlencode({
        "otherInfo": other_info or "",
        "playingTime": playing_sec,
        "duration": int(duration),
        "akid": "null",
        "jobid": job_id or "",
        "clipTime": clip,
        "clazzId": clazz_id,
        "objectId": object_id,
        "userid": puid,
        "isdrag": int(isdrag),
        "enc": enc,
        "rt": rt,
        "dtype": "Video",
        "view": "json",
    })
    return report_url + "?" + q


# ---------------------------------------------------------------- 任务信息
def _dig(obj, *names):
    if not isinstance(obj, dict):
        return None
    for n in names:
        if n in obj and obj[n] not in (None, ""):
            return obj[n]
    for key in ("data", "job", "result", "video", "courseVideo"):
        if isinstance(obj.get(key), dict):
            v = _dig(obj[key], *names)
            if v not in (None, ""):
                return v
    return None


def parse_job(payload):
    """把 ananas/job（或 knowledge/cards 里的 video 卡片）响应归一化成任务信息。"""
    if isinstance(payload, str):
        payload = json.loads(payload)
    if isinstance(payload, list):
        for it in payload:
            got = parse_job(it)
            if got.get("objectid"):
                return got
        return {}
    if not isinstance(payload, dict):
        return {}
    vbegin = _dig(payload, "vbegin")
    vend = _dig(payload, "vend")
    duration = int(_dig(payload, "duration") or 0)
    info = {
        "objectid": str(_dig(payload, "objectid", "objectId") or ""),
        "jobid": str(_dig(payload, "jobid", "jobId") or ""),
        "clazzid": str(_dig(payload, "clazzId", "clazzid") or ""),
        "courseid": str(_dig(payload, "courseid", "courseId") or ""),
        "knowledgeid": str(_dig(payload, "knowledgeid", "knowledgeId") or ""),
        "duration": duration,
        "reportUrl": _dig(payload, "reportUrl") or "",
        "otherInfo": _dig(payload, "otherInfo") or "",
        "rt": str(_dig(payload, "rt") if _dig(payload, "rt") is not None else "0.0"),
        "vbegin": int(vbegin) if vbegin is not None else -1,
        "vend": int(vend) if vend is not None else -1,
        "reportTimeInterval": int(_dig(payload, "reportTimeInterval") or 60),
        "playTime": int(_dig(payload, "playTime") or 0),
        "doublespeed": str(_dig(payload, "doublespeed") or ""),
        "fastforward": bool(_dig(payload, "fastforward") or False),
        "faceRecConfig": _dig(payload, "faceRecConfig") or "",
        "captureConfig": _dig(payload, "captureConfig") or "",
        "title": str(_dig(payload, "name", "title") or ""),
    }
    if not info["reportUrl"]:
        nested = payload.get("reportUrl") or _dig(payload, "reportUrl")
        info["reportUrl"] = nested or ""
    return info


def cards_url(clazzid, courseid, knowledgeid, num=0, is_phone=1, control="1", cpi="0"):
    return HOST_API + PATH_CARDS % (clazzid, courseid, knowledgeid, num, is_phone, control, cpi)


def job_url(jobid, knowledgeid, courseid, clazzid, jtoken=""):
    return HOST_API + PATH_JOB % (jobid, knowledgeid, courseid, clazzid, quote(str(jtoken)))


def get_json(sess, url, timeout=30):
    r = sess.get(url, timeout=timeout)
    txt = r.text
    try:
        return r.status_code, json.loads(txt)
    except Exception:
        return r.status_code, {"_raw": txt[:2000]}


# ---------------------------------------------------------------- 上报器
def plan_reports(duration, start=0, chunk=60, speed=1.0, isdrag=0, clip_start=None):
    """生成 (playing_sec, isdrag, clip_start_sec) 序列。

    客户端每个 reportTimeInterval（默认 60 秒）上报一次，playingTime 是**秒**；
    isdrag=1 只出现在用户拖动进度条那一刻，playingTime 是 "起点-终点" 形式。
    """
    seq = []
    dur = int(duration)
    pos = int(start)
    if isdrag:
        end = dur if clip_start is None else int(clip_start)
        seq.append((end, 1, pos))
        pos = end
    step = max(1, int(chunk))
    while pos < dur:
        pos = min(pos + step, dur)
        seq.append((pos, 0, None))
    return seq


def verdict_of(status, body):
    """解析 CourseDotRes（result / rollbackPoint / rollbackStatus / errorMsg）。"""
    v = {"http": status, "result": None, "rollbackPoint": -1, "rollbackStatus": False,
         "errorMsg": "", "raw": ""}
    if isinstance(body, dict):
        v["result"] = body.get("result")
        v["rollbackPoint"] = int(body.get("rollbackPoint", -1) or -1)
        v["rollbackStatus"] = bool(body.get("rollbackStatus", False))
        v["errorMsg"] = str(body.get("errorMsg", "") or "")
    else:
        step = (body or {}).get("_raw", "")
        v["raw"] = step
        if "登录" in step:
            v["errorMsg"] = step[:200]
    if status == 203:
        v["result"] = 203
    return v


class VideoTask(object):
    def __init__(self, args, salt):
        self.a = args
        self.salt = salt
        self.uid = args.uid
        self.job = {}
        self.sent = 0
        self.ok = 0
        self.rollbacks = 0
        self.session = None

    # ---- 会话
    def open(self):
        if self.session is not None:
            return self.session
        cookie = self.a.cookie or ""
        if self.a.cookie_file:
            cookie = Path(self.a.cookie_file).read_text().strip()
        if HAVE_STEALTH:
            self.session = make_session(
                cookie=cookie, uid=self.uid, referer=self.a.referer,
                max_writes_per_hour=self.a.max_writes_per_hour,
                min_interval=self.a.min_interval,
                quiet=parse_quiet(self.a.quiet_hours))
            if getattr(self.a, "stealth", False):
                try:
                    res = warmup(self.session, uid=self.uid)
                    ok = len([x for x in (res or []) if x and x[0] == 200])
                    print("[stealth] 掩护流量 %d/%d 条只读请求完成" % (ok, len(res or [])))
                except Exception as e:
                    print("[stealth] 掩护流量跳过：%s" % e)
        else:
            import requests
            self.session = requests.Session()
            self.session.headers.update({
                "User-Agent": "okhttp/4.12.0",
                "Accept": "*/*",
                "Accept-Language": "zh-CN,zh;q=0.9",
                "X-Requested-With": "com.chaoxing.mobile",
                "Referer": self.a.referer,
            })
            if cookie:
                self.session.headers["Cookie"] = cookie
        return self.session

    # ---- 取任务信息
    def load_job(self):
        a = self.a
        if a.job_json:
            self.job = parse_job(Path(a.job_json).read_text())
        elif a.course_id and a.knowledge_id and a.clazz_id and a.job_id:
            sess = self.open()
            url = job_url(a.job_id, a.knowledge_id, a.course_id, a.clazz_id, a.jtoken or "")
            st, data = get_json(sess, url)
            if st != 200 or not isinstance(data, dict):
                print("[warn] ananas/job 返回 %s：%s" % (st, str(data)[:200]))
            self.job = parse_job(data)
            if a.dump:
                Path(a.dump).write_text(json.dumps(data, ensure_ascii=False, indent=2))
        # CLI 参数补/覆盖
        over = {"reportUrl": a.report_url, "objectid": a.object_id, "jobid": a.job_id,
                "clazzid": a.clazz_id, "duration": a.duration, "rt": a.rt,
                "otherInfo": a.other_info, "vbegin": a.vbegin, "vend": a.vend}
        for k, v in over.items():
            if v not in (None, ""):
                self.job[k] = v
        self.job.setdefault("clazzid", a.clazz_id or "")
        self.job.setdefault("jobid", a.job_id or "")
        self.job.setdefault("objectid", a.object_id or "")
        self.job.setdefault("duration", int(a.duration or 0))
        self.job.setdefault("rt", str(a.rt or "0.0"))
        self.job.setdefault("otherInfo", a.other_info or "")
        self.job.setdefault("reportTimeInterval", 60)
        for k in ("vbegin", "vend"):
            if self.job.get(k) is None:
                self.job[k] = -1
        return self.job

    def list_cards(self):
        a = self.a
        sess = self.open()
        url = cards_url(a.clazz_id, a.course_id, a.knowledge_id, cpi=a.cpi or "0",
                        control=a.control or "1")
        st, data = get_json(sess, url)
        print("[cards] HTTP %s" % st)
        if a.dump:
            Path(a.dump).write_text(json.dumps(data, ensure_ascii=False, indent=2))
        found = []

        def walk(o):
            if isinstance(o, dict):
                if _dig(o, "objectid", "objectId"):
                    j = parse_job(o)
                    if j.get("objectid"):
                        found.append(j)
                for v in o.values():
                    walk(v)
            elif isinstance(o, list):
                for v in o:
                    walk(v)

        walk(data)
        if not found:
            print("(未解析出视频任务；原始响应前 400 字：%s)" % str(data)[:400])
        for j in found:
            print("- jobid=%s objectId=%s duration=%s reportUrl=%s title=%s"
                  % (j["jobid"], j["objectid"], j["duration"], (j["reportUrl"] or "")[:60], j["title"]))
        return found

    # ---- 上报
    def one_report(self, playing_sec, isdrag, clip_start):
        a, j = self.a, self.job
        clip = clip_time_of(j.get("vbegin"), j.get("vend"), j.get("duration") or 0)
        if isdrag and clip_start is not None:
            playing_param = "%d-%d" % (int(clip_start), int(playing_sec))
        else:
            playing_param = str(int(playing_sec))
        enc = make_enc(j.get("clazzid"), self.uid, j.get("jobid"), j.get("objectid"),
                       playing_sec, j.get("duration") or 0, clip, self.salt)
        url = build_report_url(j.get("reportUrl") or "", j.get("otherInfo"), playing_param,
                               j.get("duration") or 0, j.get("jobid"), clip, j.get("clazzid"),
                               j.get("objectid"), self.uid, isdrag, enc, j.get("rt") or "0.0",
                               raw=a.raw_fmt)
        if a.dry_run:
            print("[dry] %s" % url)
            print("      enc=%s  plain=%s" % (enc, enc_plain(j.get("clazzid"), self.uid, j.get("jobid"),
                                                             j.get("objectid"), playing_sec,
                                                             j.get("duration") or 0, clip, self.salt)))
            return {"result": None, "dry": True}
        sess = self.open()
        r = sess.get(url, timeout=a.timeout)
        try:
            body = json.loads(r.text)
        except Exception:
            body = {"_raw": r.text[:2000]}
        v = verdict_of(r.status_code, body)
        self.sent += 1
        if v["result"] == 1:
            self.ok += 1
        if v["rollbackStatus"] and v["rollbackPoint"] >= 0:
            self.rollbacks += 1
            print("[rollback] 服务端要求回退到 %s 秒（可信进度点）" % v["rollbackPoint"])
        print("[report] playingTime=%s isdrag=%d → HTTP %s result=%s%s%s"
              % (playing_param, isdrag, v["http"], v["result"],
                 " rollback=%s" % v["rollbackPoint"] if v["rollbackPoint"] >= 0 else "",
                 " err=%s" % v["errorMsg"] if v["errorMsg"] else ""))
        if a.audit:
            with open(a.audit, "a") as fh:
                fh.write(json.dumps({"t": time.time(), "playingTime": playing_param,
                                     "result": v["result"], "rollbackPoint": v["rollbackPoint"],
                                     "http": v["http"]}, ensure_ascii=False) + "\n")
        return v

    def run(self):
        a = self.a
        j = self.load_job()
        if not (j.get("reportUrl") and j.get("objectid")):
            print("[x] 缺少 reportUrl/objectId：先用 --list 取任务，或 --report-url/--object-id 直接给")
            return 2
        missing = [k for k in ("clazzid", "objectid", "duration") if not j.get(k)]
        if missing:
            print("[x] 缺少必要字段：%s" % ", ".join(missing))
            return 2
        seq = plan_reports(j.get("duration") or a.duration or 0, start=a.start, chunk=a.chunk,
                           speed=a.speed, isdrag=1 if a.isdrag else 0, clip_start=a.clip_start)
        if a.limit:
            seq = seq[:a.limit]
        print("[plan] %d 次上报，chunk=%ss speed=%s 起于 %ss" % (len(seq), a.chunk, a.speed, a.start))
        for i, (pos, isdrag, clip_start) in enumerate(seq, 1):
            try:
                v = self.one_report(pos, isdrag, clip_start)
            except RiskHalt as e:
                print("[STOP] 风控停机：%s" % e)
                return 3
            except RiskCooldown as e:
                print("[WAIT] %s" % e)
                return 4
            if v.get("rollbackStatus") and v.get("rollbackPoint", -1) >= 0 and a.stop_on_rollback:
                print("[x] 服务端回退，按 --stop-on-rollback 停止")
                return 5
            if i < len(seq) and not a.dry_run:
                nap = a.chunk / max(0.1, a.speed)
                if a.pace == "real":
                    time.sleep(min(nap, 300))
                elif a.pace == "jitter" and HAVE_STEALTH:
                    time.sleep(min(human_delay(nap * 0.6, nap * 1.4), 300))
        print("[done] 上报 %d 次，成功 %d，回退提示 %d" % (self.sent, self.ok, self.rollbacks))
        if HAVE_STEALTH and hasattr(self.session, "report"):
            try:
                print("[risk] %s" % json.dumps(self.session.report(), ensure_ascii=False)[:600])
            except Exception:
                pass
        return 0


# ---------------------------------------------------------------- 校验
def verify_capture(path, salt):
    """capture 文件支持两种形态：
      {"plain": "...", "enc": "..."} 或 {"clazzId":..,"puid":..,...}
    后者用公式重算再比。"""
    data = json.loads(Path(path).read_text())
    items = data if isinstance(data, list) else [data]
    bad = 0
    for it in items:
        plain = it.get("plain")
        if plain is None:
            clip = it.get("clipTime") or clip_time_of(it.get("vbegin", -1), it.get("vend", -1),
                                                       it.get("duration", 0))
            plain = enc_plain(it.get("clazzId"), it.get("puid"), it.get("jobid"),
                              it.get("objectId"), it.get("playingTime", 0),
                              it.get("duration", 0), clip, salt)
        got = md5_hex(plain)
        exp = it.get("enc")
        ok = (exp is None) or (got == exp)
        print("%s %s → %s%s" % ("[OK]" if ok else "[x]", got,
                                exp or "(未提供 enc)", "" if ok else " 期望 %s" % exp))
        if not ok:
            bad += 1
    return 1 if bad else 0


def selftest(salt):
    """自检：盐派生、公式、URL 结构、判定解析。不联网。"""
    ok = True
    cvm = HERE.parent / "out" / "cvm.smali"
    if cvm.exists():
        got = salt_from_smali_file(cvm)
        same = (got == salt)
        print("%s 盐派生：len=%d sha1=%s%s" % ("[OK]" if same else "[x]", len(got or ""),
                                              hashlib.sha1((got or "").encode()).hexdigest()[:10],
                                              "" if same else "（与内置不同，已改用派生值）"))
        if got:
            salt = got
        ok &= same
    else:
        print("[--] 未找到 %s，跳过盐派生" % cvm)
    p = enc_plain("666666", "12345678", "999", "abc123", 120, 900, "0_900", salt)
    exp_prefix = "[666666][12345678][999][abc123][120000]["
    exp_suffix = "][900000][0_900]"
    ok &= p.startswith(exp_prefix) and p.endswith(exp_suffix)
    print("%s enc 明文结构：%s" % ("[OK]" if p.startswith(exp_prefix) and p.endswith(exp_suffix) else "[x]",
                                    p[:28] + "…" + p[-22:]))
    ok &= (md5_hex(p) == make_enc("666666", "12345678", "999", "abc123", 120, 900, "0_900", salt))
    u = build_report_url("https://example.invalid/log", "oi", "120", 900, "999", "0_900",
                         "666666", "abc123", "12345678", 0, "deadbeef", "0.5")
    for key in ("playingTime=120", "isdrag=0", "enc=deadbeef", "dtype=Video", "view=json", "rt=0.5"):
        ok &= key in u
    print("%s URL 结构：%s" % ("[OK]" if ok else "[x]", u[:110] + "…"))
    v = verdict_of(200, {"result": 203, "rollbackStatus": True, "rollbackPoint": 42})
    ok &= (v["result"] == 203 and v["rollbackStatus"] and v["rollbackPoint"] == 42)
    print("%s 判定解析：result=%s rollbackPoint=%s" % ("[OK]" if ok else "[x]", v["result"], v["rollbackPoint"]))
    seq = plan_reports(180, chunk=60)
    ok &= [s[0] for s in seq] == [60, 120, 180]
    print("%s 上报序列：%s" % ("[OK]" if [s[0] for s in seq] == [60, 120, 180] else "[x]", seq))
    print("结果：%s" % ("全部通过" if ok else "有失败项"))
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser(description="学习通视频任务点（进度上报）客户端")
    ap.add_argument("--uid", help="puid（--verify-capture/--selftest 时可省）")
    ap.add_argument("--cookie-file")
    ap.add_argument("--cookie")
    ap.add_argument("--referer", default="https://mooc1-api.chaoxing.com/")
    ap.add_argument("--stealth", action="store_true", help="启用伪装层（设备档案+TLS指纹+掩护流量）")
    ap.add_argument("--max-writes-per-hour", type=int, default=90)
    ap.add_argument("--min-interval", type=float, default=5.0)
    ap.add_argument("--quiet-hours", default="1-7")
    # 任务来源
    ap.add_argument("--course-id")
    ap.add_argument("--clazz-id", required=False)
    ap.add_argument("--knowledge-id")
    ap.add_argument("--job-id")
    ap.add_argument("--jtoken", default="")
    ap.add_argument("--cpi", default="0")
    ap.add_argument("--control", default="1")
    ap.add_argument("--job-json", help="ananas/job 的原始响应（离线运行）")
    ap.add_argument("--dump", help="把响应写到这里")
    ap.add_argument("--list", action="store_true", help="只列出章节里的视频任务")
    # 直接给参数（frida 抓包后的直报）
    ap.add_argument("--report-url")
    ap.add_argument("--object-id")
    ap.add_argument("--duration", type=int)
    ap.add_argument("--rt")
    ap.add_argument("--other-info")
    ap.add_argument("--vbegin", type=int)
    ap.add_argument("--vend", type=int)
    # 上报行为
    ap.add_argument("--chunk", type=int, default=60, help="每次上报的秒步长（客户端默认 60）")
    ap.add_argument("--speed", type=float, default=1.0, help="相对真实播放的速度；>1 更快但更易被回退")
    ap.add_argument("--pace", choices=["real", "jitter", "fast"], default="real")
    ap.add_argument("--start", type=int, default=0, help="从第几秒开始报（续播）")
    ap.add_argument("--isdrag", type=int, default=0, help="1 表示先发一次拖动上报")
    ap.add_argument("--clip-start", type=int, default=0)
    ap.add_argument("--limit", type=int, help="最多上报几次")
    ap.add_argument("--stop-on-rollback", action="store_true")
    ap.add_argument("--raw-fmt", action="store_true", help="复刻客户端不做 URL 编码的拼法")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--timeout", type=int, default=30)
    ap.add_argument("--audit", help="把每次结果追加写 JSONL")
    ap.add_argument("--json", action="store_true")
    # 盐来源
    ap.add_argument("--salt", default=None)
    ap.add_argument("--salt-smali")
    ap.add_argument("--salt-apk")
    # 校验
    ap.add_argument("--verify-capture")
    ap.add_argument("--verify-enc", help="给明文，打印 md5（用来和抓包对比）")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()

    salt = a.salt
    src = "命令行"
    if not salt:
        if a.salt_smali:
            salt, src = salt_from_smali_file(a.salt_smali), "smali 文件"
        elif a.salt_apk:
            salt, src = salt_from_apk(a.salt_apk), "apk"
        else:
            local = HERE.parent / "out" / "cvm.smali"
            derived = salt_from_smali_file(local) if local.exists() else None
            salt, src = (derived, "本地 smali") if derived else (SALT_DEFAULT, "内置")
    print("[salt] 来源=%s len=%d sha1=%s" % (src, len(salt or ""),
                                             hashlib.sha1((salt or "").encode()).hexdigest()[:10]))

    if a.selftest:
        return selftest(salt)
    if a.verify_enc:
        print(md5_hex(a.verify_enc))
        return 0
    if a.verify_capture:
        return verify_capture(a.verify_capture, salt)

    task = VideoTask(a, salt)
    if a.list:
        return 0 if task.list_cards() is not None else 1
    if not a.uid:
        print("[x] 需要 --uid（puid）")
        return 2
    try:
        return task.run()
    except RiskHalt as e:
        print("[STOP] 风控停机：%s" % e)
        return 3
    except RiskCooldown as e:
        print("[WAIT] %s" % e)
        return 4


if __name__ == "__main__":
    sys.exit(main())
