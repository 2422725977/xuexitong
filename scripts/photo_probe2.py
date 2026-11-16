#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""拍照签到/photoAuth 探测：signDetail 全字段 + 服务端行为空间（缺参/换端点）。"""
import json
import os
import sys
import time
import urllib.parse

import requests

MOBILE = "https://mobilelearn.chaoxing.com/"
COURSE, CLAZZ, SID = "269282723", "159926750", "493228247"
UA_APP = ("Mozilla/5.0 (Linux; Android 10; SM-G975F Build/QP1A.190711.020; wv) "
          "AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/80.0.3987.99 Mobile Safari/537.36")


def load_ck(p):
    with open(p, "r", encoding="utf-8", errors="ignore") as f:
        return f.read().strip()


def main():
    aid = sys.argv[1] if len(sys.argv) > 1 else "4000180999257"
    oid = sys.argv[2] if len(sys.argv) > 2 else "3f2e616894df22b91b946c396d066c25"
    ck = load_ck("ck.txt")
    h = {"Cookie": ck, "User-Agent": UA_APP}

    print("=== signDetail 全字段 (aid=%s) ===" % aid)
    r = requests.get(MOBILE + "newsign/signDetail?activePrimaryId=%s&type=1" % aid, headers=h, timeout=25)
    try:
        j = r.json()
        print(json.dumps(j, ensure_ascii=False, indent=2)[:2500])
    except Exception:
        print("HTTP %s %s" % (r.status_code, (r.text or "")[:300]))

    print("=== 学生 preSign 页里与 photo/auth 有关的片段 ===")
    r = requests.get(MOBILE + "newsign/preSign?courseId=%s&classId=%s&activePrimaryId=%s&uid=%s&appType=15"
                     % (COURSE, CLAZZ, aid, SID), headers=h, timeout=25)
    body = r.text or ""
    open("out/preSign_photo_probe.html", "w", encoding="utf-8").write(body)
    print("HTTP %s len=%d" % (r.status_code, len(body)))
    for kw in ("photoAuth", "objectId", "ifPhoto", "uploadParams", "uploadConfig", "validate", "deviceCode"):
        n = body.count(kw)
        if n:
            print("  %-14s x%d" % (kw, n))

    print("=== 行为空间探测 ===")
    base = [("activeId", aid), ("courseId", COURSE), ("uid", SID), ("clientip", ""),
            ("useragent", ""), ("latitude", "-1"), ("longitude", "-1"), ("appType", "15"),
            ("fid", "12"), ("name", "1.png"), ("validate", "")]
    inner = [{"name": "1.png", "objectid": oid, "type": "png"}]
    pr = json.dumps({"files": json.dumps(inner, separators=(",", ":"))}, separators=(",", ":"))
    cases = [
        ("P1 无 objectId 无 photoResult", base, "pptSign/stuSignajax"),
        ("P2 objectId=garbage", base + [("objectId", "deadbeef")], "pptSign/stuSignajax"),
        ("P3 objectId 真值 无 photoResult", base + [("objectId", oid)], "pptSign/stuSignajax"),
        ("P4 objectId 真值 + photoResult", base + [("objectId", oid), ("photoResult", pr)], "pptSign/stuSignajax"),
        ("P5 老端点 /sign/stuSignajax + photoResult", base + [("objectId", oid), ("photoResult", pr)], "sign/stuSignajax"),
        ("P6 /newsign/stuSignajax + photoResult", base + [("objectId", oid), ("photoResult", pr)], "newsign/stuSignajax"),
        ("P7 /pptSign/stuSignajax 带 att 风格 objectid 小写", base + [("objectid", oid)], "pptSign/stuSignajax"),
    ]
    for desc, params, ep in cases:
        try:
            r = requests.post(MOBILE + ep, headers=h, data=params, timeout=25)
            body = (r.text or "").strip()
        except Exception as e:
            body = repr(e)
            r = None
        print("%-46s -> HTTP %s  %s" % (desc, getattr(r, "status_code", "-"), body[:140]))
        time.sleep(1.0)


if __name__ == "__main__":
    main()
