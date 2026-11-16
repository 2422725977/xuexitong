#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""教师侧「签到状态改写」工具：把迟到/缺勤改回已签（正常），或反向改。

实测依据（学习通 6.7.8 / 2026-11-16）
  1) 学生提交响应的语义（学生页 JS，out/preSign_*.html:349）
       res == "success"   -> 按时签到，计入「已签」
       res == "success2"  -> 已过教师设置的截止时间（迟到），客户端 Toast
                             「已过教师设置的截止时间」，记录仍入库但
                             落到「未签」名单里 status=9
  2) 教师页修改状态提交（out/tchpages/gotasksign.html:1972）
       GET /pptSign/updateSignStatus
           ?attendids=<attendId[,attendId...]>&status=<N>&remark=<备注>&activeId=<aid>
       成功判定 res == "success"
  3) 状态码全表（同上页面 .statelist）
       1=已签(正常) 2=已签(代签) 5=缺勤 9=迟到 10=早退
       7=病假 8=事假 12=公假 39331=实习 39332=实训 39333=免修 39334=参赛
  4) 前端 overLateEndTime() 的真实判断被注释、恒 return true —— 页面不挡
     「活动结束后改状态」；服务端该接口也没有时间窗参数。

用法
  # 看名单（迟到记录在未签名单里 status=9）
  python3 flip_attend_status.py --active-id 4000180997892 --list
  # 把某人的迟到记录改成正常已签
  python3 flip_attend_status.py --active-id 4000180997892 --uid-filter [学生PUID] --status 1
  # 直接按 attendId 批量改
  python3 flip_attend_status.py --active-id 4000180997892 --attend-ids 4001549259183 --status 9
"""
import argparse
import json
import os
import re
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from stealth_session import make_session  # noqa: E402

BASE = "https://mobilelearn.chaoxing.com"
LIST_URL = BASE + "/pptSign/refeashSignList4Json2"
AUTO_URL = BASE + "/pptSign/autoRefeashSignList4Json2"
UPD_URL = BASE + "/pptSign/updateSignStatus"

STATUS_NAME = {
    0: "未知/已删", 1: "已签(正常)", 2: "已签(代签)", 5: "缺勤", 7: "病假",
    8: "事假", 9: "迟到", 10: "早退", 12: "公假", 39331: "实习",
    39332: "实训", 39333: "免修", 39334: "参赛",
}


def name_of(v):
    try:
        return STATUS_NAME.get(int(v), "状态%s" % v)
    except Exception:
        return "状态%s" % v


class Flipper(object):
    def __init__(self, cookie, teacher_uid, referer=None, max_writes_per_hour=120,
                 min_interval=1.0, ua_mode="h5"):
        self.sess = make_session(
            cookie=cookie, uid=teacher_uid,
            referer=referer or (BASE + "/"), ua_mode=ua_mode, xhr=True,
            guard=False, max_writes_per_hour=max_writes_per_hour,
            min_interval=min_interval)
        self.uid = teacher_uid

    def list_rows(self, active_id, ty="0", top_mode=False):
        """ty: 0=已签名单 1=未签名单（迟到记录在未签名单里，status=9）"""
        params = {"activeId": str(active_id), "appType": "15"}
        if top_mode:
            params.update({"topTime": "0", "topId": "0"})
        else:
            params.update({"lastTime": "0", "lastId": "0", "pageNo": "1",
                           "type": str(ty), "denc": ""})
        url = AUTO_URL if top_mode else LIST_URL
        r = self.sess.get(url, params=params, timeout=25)
        try:
            j = r.json()
        except Exception:
            return {"raw": (r.text or "")[:200], "list": []}
        return j

    def scan(self, active_id, uid_filter=""):
        """把四条名单查询并起来，去重后返回记录列表（迟到行也在内）"""
        seen, rows = set(), []
        for tag, ty, top in (("未签", "1", False), ("未签top", "1", True),
                             ("已签", "0", False), ("已签top", "0", True)):
            jj = self.list_rows(active_id, ty=ty, top_mode=top)
            if jj.get("raw"):
                continue
            if jj.get("yiqianNum") is not None or jj.get("weiqianNum") is not None:
                print("[名单 %s] 已签=%s 未签=%s" % (tag, jj.get("yiqianNum"), jj.get("weiqianNum")))
            for r0 in (jj.get("list") or []):
                key = str(r0.get("id"))
                if key in seen:
                    continue
                seen.add(key)
                r0 = dict(r0)
                r0["_src"] = tag
                rows.append(r0)
        if uid_filter:
            rows = [r0 for r0 in rows if str(r0.get("uid")) == str(uid_filter)]
        return rows

    def update(self, active_id, attend_ids, status, remark=""):
        ids = attend_ids if isinstance(attend_ids, str) else ",".join(str(x) for x in attend_ids)
        r = self.sess.get(UPD_URL, params={"attendids": ids, "status": str(status),
                                           "remark": remark, "activeId": str(active_id)},
                          timeout=25, headers={"X-Requested-With": "XMLHttpRequest"})
        return (r.text or "").strip()


def main():
    ap = argparse.ArgumentParser(description="教师侧签到状态改写（迟到<->已签）")
    ap.add_argument("--active-id", required=True, help="活动 id（activeId/activePrimaryId）")
    ap.add_argument("--cookie", default="ck_tch.txt", help="教师 cookie 文件（整串）")
    ap.add_argument("--teacher-uid", default="[教师PUID]")
    ap.add_argument("--course-id", default="", help="仅用于拼 referer，可空")
    ap.add_argument("--class-id", default="", help="仅用于拼 referer，可空")
    ap.add_argument("--list", action="store_true", help="只列名单不改")
    ap.add_argument("--uid-filter", default="", help="只处理该 uid 的记录")
    ap.add_argument("--attend-ids", default="", help="直接指定 attendId（逗号分隔）")
    ap.add_argument("--status", default="1", help="目标状态：1=已签(正常) 5=缺勤 9=迟到 2=代签 ...")
    ap.add_argument("--remark", default="", help="备注，最多 10 字")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    ck = a.cookie
    if os.path.exists(ck):
        ck = open(ck, encoding="utf-8").read().strip()
    ref = (BASE + "/pptSign/gotasksign?activePrimaryId=%s&courseId=%s&classId=%s&uid=%s&appType=15&isTeacherViewOpen=1"
           % (a.active_id, a.course_id, a.class_id, a.teacher_uid))
    f = Flipper(ck, a.teacher_uid, referer=ref)

    rows = f.scan(a.active_id, uid_filter=a.uid_filter)
    print("[名单] activeId=%s 命中记录 %d 条" % (a.active_id, len(rows)))
    for r0 in rows:
        print("   [%s] attendId=%s uid=%s status=%s(%s) submittime=%s name=%s"
              % (r0.get("_src"), r0.get("id"), r0.get("uid"), r0.get("status"),
                 name_of(r0.get("status")), r0.get("submittime"), r0.get("name")))
    if a.list:
        return 0

    ids = [x for x in re.split(r"[,\s]+", a.attend_ids) if x] or [str(r0.get("id")) for r0 in rows if r0.get("id")]
    if not ids:
        print("[!] 没找到要改的记录（可加 --uid-filter，或直接 --attend-ids）")
        return 1
    if a.dry_run:
        print("[dry-run] 将把 %s 改成 status=%s(%s)" % (ids, a.status, name_of(a.status)))
        return 0
    res = f.update(a.active_id, ids, a.status, a.remark)
    print("[改状态] attendids=%s status=%s(%s) -> %s" % (ids, a.status, name_of(a.status), res[:120]))
    time.sleep(2)
    after = f.scan(a.active_id, uid_filter=a.uid_filter)
    print("[复核] 状态改后命中 %d 条" % len(after))
    for r0 in after:
        print("   [%s] attendId=%s uid=%s status=%s(%s) submittime=%s"
              % (r0.get("_src"), r0.get("id"), r0.get("uid"), r0.get("status"),
                 name_of(r0.get("status")), r0.get("submittime")))
    return 0 if res == "success" else 1


if __name__ == "__main__":
    sys.exit(main())
