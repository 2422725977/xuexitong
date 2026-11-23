#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""学习通刷网课总管：列课程 → 自走章节/任务点 → 按真实节奏上报视频进度。

与 video_task.py 的分工：video_task 只管「一个任务点」的协议与上报；本脚本负责
「我有哪几门课、每门课有哪些任务点、挨个刷」这一层。

关键接口（需要 mooc 域会话，即 fid 不为 0 的真实学校账号）：
  课程列表   GET https://mooc1-api.chaoxing.com/mycourse/backclazzdata?view=json&rss=1
  章节树     GET https://mooc1-api.chaoxing.com/mycourse/studentcourse?courseId=&clazzid=&personId=
  任务点     GET https://mooc1-api.chaoxing.com/knowledge/cards?clazzid=&courseid=&knowledgeid=
                    （响应里带 objectid/jobid/duration/reportUrl，正是上报要的字段）
章节 id 的来源不做假设：先试章节页，再从 cards 响应里递归抠 id（BFS 自走），全程
原始响应落 --dump-dir，拿到会话后按真机结果再收敛。

用法：
  python3 scripts/brush_course.py --cookie-file mooc.txt --uid <puid> --list-courses
  python3 scripts/brush_course.py --cookie-file mooc.txt --uid <puid> --course-id 269282723 --dry-run
  python3 scripts/brush_course.py --cookie-file mooc.txt --uid <puid> --pace real --speed 1.0
  python3 scripts/brush_course.py --selftest
"""
import argparse, json, os, re, sys, time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import video_task as vt  # 复用协议层

HOST_API = "https://mooc1-api.chaoxing.com/"
HOST_WEB = "https://mooc1.chaoxing.com/"
UA_APP = ("Mozilla/5.0 (Linux; Android 12; LM-G820N Build/SKQ1.210908.001; wv) "
          "AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/137.0.7151.115 "
          "Mobile Safari/537.36")
UA_WEB = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
          "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")


# ---------------------------------------------------------------- 解析（纯函数，可离线自检）
def parse_courses(payload):
    """backclazzdata → [{courseid, clazzid, cpi, name, teacher, chatid, roletype, school}]"""
    out = []
    chans = (payload or {}).get("channelList") or []
    for ch in chans:
        content = ch.get("content") or {}
        datas = ((content.get("course") or {}).get("data")) or []
        for d in datas:
            cid = d.get("id") or d.get("courseid")
            clz = ch.get("key") or d.get("clazzid")
            if not cid or not clz:
                continue
            out.append({
                "courseid": str(cid),
                "clazzid": str(clz),
                "cpi": str(ch.get("cpi") or content.get("cpi") or "0"),
                "name": d.get("name") or content.get("name") or "",
                "teacher": d.get("teacherfactor") or "",
                "chatid": content.get("chatid") or "",
                "roletype": content.get("roletype"),
                "school": d.get("belongSchoolId") or "",
            })
    return out


RE_IDS = [
    re.compile(r'"chapterId"\s*:\s*"?(\d{4,})'),
    re.compile(r'"knowledgeId"\s*:\s*"?(\d{4,})'),
    re.compile(r'"knowledgeid"\s*:\s*"?(\d{4,})'),
    re.compile(r'knowledgeId["\']?\s*[:=]\s*["\']?(\d{4,})'),
    re.compile(r'chapterId["\']?\s*[:=]\s*["\']?(\d{4,})'),
]


def extract_knowledge_ids(text, limit=200):
    """从 HTML/JSON 里抠章节 id；也吃 cards 响应里 nested 的 id 字段。"""
    ids = []
    for rx in RE_IDS:
        for m in rx.finditer(text or ""):
            v = m.group(1)
            if v not in ids:
                ids.append(v)
    # cards 响应里章节对象形如 {"id":12345678,"name":"1.1 ..."}，用 name 定位更稳
    for m in re.finditer(r'\{"id"\s*:\s*(\d{5,})[^{}]{0,200}?"name"\s*:\s*"', text or ""):
        v = m.group(1)
        if v not in ids:
            ids.append(v)
    return ids[:limit]


def walk_jobs(payload):
    """cards 响应 → 任务点列表（objectid 存在即算任务点）。"""
    found, seen = [], set()

    def walk(o):
        if isinstance(o, dict):
            j = vt.parse_job(o)
            key = (j.get("jobid"), j.get("objectid"))
            if j.get("objectid") and key not in seen:
                seen.add(key)
                found.append(j)
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)

    walk(payload)
    return found


# ---------------------------------------------------------------- 网络层
class Brush(object):
    def __init__(self, a):
        self.a = a
        self.sess = None
        self.courses = []
        self.done = {}
        self.uid = a.uid

    def open(self):
        if self.sess is None:
            import requests
            cookie = self.a.cookie or ""
            if self.a.cookie_file:
                cookie = Path(self.a.cookie_file).read_text(encoding="utf-8", errors="ignore").strip()
            s = requests.Session()
            s.headers.update({
                "Cookie": cookie,
                "User-Agent": UA_APP if self.a.ua_mode == "app" else UA_WEB,
                "Accept": "*/*",
                "Accept-Language": "zh-CN,zh;q=0.9",
                "Referer": HOST_API,
            })
            self.sess = s
        return self.sess

    def get(self, url, as_json=True, tag="", keep=True):
        s = self.open()
        try:
            r = s.get(url, timeout=self.a.timeout, allow_redirects=False)
        except Exception as e:
            print("[x] %s 请求失败 %s: %s" % (tag or url[:40], type(e).__name__, e))
            return None
        body = r.text
        if r.status_code in (301, 302):
            print("[!] %s HTTP %s → %s（会话没进 mooc 域，先去拿真 cookie）"
                  % (tag or url[:40], r.status_code, r.headers.get("Location", "")[:80]))
        if keep and self.a.dump_dir:
            d = Path(self.a.dump_dir)
            d.mkdir(parents=True, exist_ok=True)
            safe = re.sub(r"[^0-9A-Za-z_.-]", "_", (tag or "resp"))[:80]
            (d / (safe + ".txt")).write_text(body, encoding="utf-8", errors="ignore")
        if as_json:
            try:
                return r.status_code, r.json()
            except Exception:
                return r.status_code, body
        return r.status_code, body

    # ---- 课程
    def list_courses(self):
        st, payload = self.get(HOST_API + "mycourse/backclazzdata?view=json&rss=1",
                               tag="courses")
        if not isinstance(payload, dict) or not payload.get("channelList"):
            print("[x] 课程列表不可用（HTTP %s）：%s" % (st, str(payload)[:200]))
            return []
        self.courses = parse_courses(payload)
        print("[=] %d 门课：" % len(self.courses))
        for c in self.courses:
            print("    %-12s clazz=%-10s cpi=%-10s %s / %s" %
                  (c["courseid"], c["clazzid"], c["cpi"], c["name"][:24], c["teacher"][:12]))
        return self.courses

    # ---- 章节 id
    def seed_knowledge_ids(self, c):
        urls = [
            ("chapter_api", HOST_API + "mycourse/studentcourse?courseId=%s&clazzid=%s&personId=%s&ut=s&t=%d"
             % (c["courseid"], c["clazzid"], self.uid, int(time.time() * 1000))),
            ("chapter_web", HOST_WEB + "mycourse/studentcourse?courseId=%s&clazzid=%s&personId=%s&ut=s"
             % (c["courseid"], c["clazzid"], self.uid)),
        ]
        ids = []
        for tag, u in urls:
            st, body = self.get(u, as_json=False, tag=tag)
            if not isinstance(body, str):
                continue
            got = extract_knowledge_ids(body)
            print("[=] %s HTTP %s 抠到章节 id %d 个" % (tag, st, len(got)))
            for g in got:
                if g not in ids:
                    ids.append(g)
            if ids:
                break
        return ids

    def cards(self, c, kid):
        url = vt.cards_url(c["clazzid"], c["courseid"], kid, cpi=c["cpi"],
                           control=self.a.control)
        st, payload = self.get(url, tag="cards_%s_%s" % (c["courseid"], kid))
        if not isinstance(payload, (dict, list)):
            return []
        return walk_jobs(payload)

    # ---- 跑
    def run_course(self, c):
        print("\n=== %s (%s / %s) ===" % (c["name"], c["courseid"], c["clazzid"]))
        seeds = self.seed_knowledge_ids(c)
        if not seeds:
            print("[!] 没拿到章节 id —— 用 0 当种子试探（cards 有时忽略 knowledgeid 直接回全课程）")
            seeds = ["0"]
        queue, visited, total, brushed = list(seeds), set(), 0, 0
        while queue and len(visited) < self.a.max_chapters:
            kid = queue.pop(0)
            if kid in visited:
                continue
            visited.add(kid)
            jobs = self.cards(c, kid)
            vids = [j for j in jobs if (j.get("objectid") and (j.get("duration") or 0) > 0)]
            total += len(vids)
            print("[cards] knowledgeid=%s → 任务点 %d（其中视频/音频 %d）" % (kid, len(jobs), len(vids)))
            for more in extract_knowledge_ids(json.dumps(jobs, ensure_ascii=False)):
                if more not in visited and more not in queue:
                    queue.append(more)
            for j in vids:
                if self.a.only_unfinished and j.get("status") in (1, "1"):
                    continue
                if self.a.dry_run:
                    print("    [dry] jobid=%s duration=%ss objectId=%s %s"
                          % (j["jobid"], j["duration"], j["objectid"], (j.get("title") or "")[:30]))
                    continue
                rc = self.brush_job(c, kid, j)
                if rc == 0:
                    brushed += 1
                elif rc in (3, 4):
                    print("[STOP] 风控停机/冷却（rc=%s），本轮结束" % rc)
                    return brushed, total
        print("[课程完成] %s：扫描任务点 %d，上报完成 %d" % (c["name"], total, brushed))
        return brushed, total

    def brush_job(self, c, kid, j):
        ns = vt_args(
            uid=self.uid, cookie=self.a.cookie, cookie_file=self.a.cookie_file,
            course_id=c["courseid"], clazz_id=c["clazzid"], knowledge_id=kid,
            job_id=j.get("jobid"), cpi=c["cpi"], control=self.a.control,
            report_url=j.get("reportUrl"), object_id=j.get("objectid"),
            duration=int(j.get("duration") or 0), rt=j.get("rt"),
            other_info=j.get("otherInfo"), vbegin=j.get("vbegin"), vend=j.get("vend"),
            chunk=self.a.chunk, speed=self.a.speed, pace=self.a.pace, start=0,
            dry_run=self.a.dry_run, stealth=self.a.stealth,
            no_risk_center=self.a.no_risk_center, report_interval=self.a.report_interval,
            audit=self.a.audit, timeout=self.a.timeout,
        )
        salt = self.a.salt or vt.SALT_DEFAULT
        t = vt.VideoTask(ns, salt)
        try:
            return t.run()
        except Exception as e:
            print("[x] jobid=%s 上报异常 %s: %s" % (j.get("jobid"), type(e).__name__, e))
            return 9

    def run(self):
        if not self.list_courses():
            return 2
        sel = [c for c in self.courses
               if not self.a.course_id or str(c["courseid"]) == str(self.a.course_id)]
        if not sel:
            print("[x] --course-id %s 不在课程列表里" % self.a.course_id)
            return 3
        B = T = 0
        for c in sel:
            b, t = self.run_course(c)
            B += b
            T += t
        print("\n[总计] 课程 %d 门，扫描任务点 %d，上报完成 %d" % (len(sel), T, B))
        return 0


def vt_args(**kw):
    """造一个 video_task.VideoTask 能吃的 argparse.Namespace（补齐默认值）。"""
    import argparse as _ap
    base = dict(
        uid=None, cookie=None, cookie_file=None, referer=HOST_API, ua_mode="app",
        stealth=False, max_writes_per_hour=90, min_interval=5.0, quiet_hours="1-7",
        no_risk_center=False, report_interval=0, course_id=None, clazz_id=None,
        knowledge_id=None, job_id=None, jtoken="", cpi="0", control="1", job_json=None,
        dump=None, list=False, report_url=None, object_id=None, duration=None, rt=None,
        other_info=None, vbegin=None, vend=None, start=0, chunk=60, speed=1.0,
        isdrag=0, clip_start=None, limit=0, pace="real", stop_on_rollback=False,
        dry_run=False, audit=None, json=False, raw_fmt=vt.FMT_QUERY, timeout=30,
    )
    base.update({k: v for k, v in kw.items() if v is not None})
    return _ap.Namespace(**base)


# ---------------------------------------------------------------- 自检
def selftest():
    here = HERE.parent
    sample = here / "out" / "backclazzdata.json"
    assert sample.exists(), "缺样本 out/backclazzdata.json"
    cs = parse_courses(json.loads(sample.read_text(encoding="utf-8")))
    assert cs and cs[0]["courseid"].isdigit() and cs[0]["clazzid"].isdigit(), cs
    print("[+] 课程解析 OK：%s" % cs[0])
    html = '<script>var chapterList=[{"chapterId":991100,"name":"1.1"},{"chapterId":"991101"}]</script>'
    ids = extract_knowledge_ids(html)
    assert "991100" in ids and "991101" in ids, ids
    cards = {"data": [{"object": {"objectid": "abc", "jobid": "12345", "duration": 900,
                                  "reportUrl": "https://mooc1.chaoxing.com/mooc-ans/multimedia/log/a/1",
                                  "vbegin": 0, "vend": 900, "name": "视频A"}}]}
    jobs = walk_jobs(cards)
    assert len(jobs) == 1 and jobs[0]["objectid"] == "abc" and jobs[0]["duration"] == 900, jobs
    print("[+] cards 任务点解析 OK：%s" % jobs[0])
    ns = vt_args(uid="1", course_id="2", clazz_id="3", knowledge_id="4", job_id="5")
    t = vt.VideoTask(ns, vt.SALT_DEFAULT)
    t.job = {"clazzid": "3", "objectid": "abc", "jobid": "5", "duration": 900,
             "reportUrl": "https://x/y", "vbegin": 0, "vend": 900, "rt": "0.0",
             "reportTimeInterval": 60}
    seq = vt.plan_reports(900, chunk=60, speed=1.0)
    assert len(seq) == 15, len(seq)
    print("[+] 计划生成 OK：900 秒 → %d 次上报" % len(seq))
    print("[+] selftest PASS")
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cookie-file")
    ap.add_argument("--cookie")
    ap.add_argument("--uid", help="puid（mooc 域用得到）")
    ap.add_argument("--course-id", help="只刷这门课")
    ap.add_argument("--list-courses", action="store_true")
    ap.add_argument("--max-chapters", type=int, default=60)
    ap.add_argument("--chunk", type=int, default=60)
    ap.add_argument("--speed", type=float, default=1.0, help="1.0=真实速度；>1 更容易被回退")
    ap.add_argument("--pace", choices=["real", "fast", "jitter"], default="real")
    ap.add_argument("--stealth", action="store_true")
    ap.add_argument("--no-risk-center", action="store_true")
    ap.add_argument("--report-interval", type=int, default=0)
    ap.add_argument("--ua-mode", choices=["app", "browser"], default="app")
    ap.add_argument("--control", default="1")
    ap.add_argument("--only-unfinished", action="store_true", help="跳过 task status=1 的任务点")
    ap.add_argument("--dump-dir", default="out/brush_dump")
    ap.add_argument("--audit")
    ap.add_argument("--salt")
    ap.add_argument("--timeout", type=int, default=30)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not a.uid:
        print("[x] 需要 --uid（puid）")
        return 2
    b = Brush(a)
    if a.list_courses:
        return 0 if b.list_courses() else 2
    return b.run()


if __name__ == "__main__":
    sys.exit(main())
