#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""拍照门 PCR007 —— 活动侧取证：signDetail / pptActiveInfo / 教师活动页 content 全字段对照"""
import json, re, sys, os
import requests

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
MOBILE = "https://mobilelearn.chaoxing.com/"
COURSE, CLAZZ, SID = "269282723", "159926750", "[学生PUID]"
UA = ("Mozilla/5.0 (Linux; Android 13; SM-G975F Build/TQ3A.230901.001) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Version/4.0 Chrome/120.0.0.0 Mobile Safari/537.36 (schild:b1c2d3e4f5a60718) "
      "(device:SM-G975F) Language/zh_CN com.ssreader.ChaoXingStudy/ChaoXingStudy_3_6_2_android_phone_20230101")


def ck(p):
    return open(p, encoding="utf-8", errors="ignore").read().strip()


sck, tck = ck("ck.txt"), ck("ck_tch.txt")
AIDS = ["4000180999265", "4000180998737", "4000180999255"]

for aid in AIDS:
    print("=" * 70)
    print("AID", aid)
    r = requests.get(MOBILE + "newsign/signDetail", params={"activePrimaryId": aid, "type": "1"},
                     headers={"Cookie": sck, "User-Agent": UA}, timeout=30)
    try:
        j = r.json()
        d = j.get("data") if isinstance(j, dict) and "data" in j else j
        keys = sorted(d.keys()) if isinstance(d, dict) else []
        print("  signDetail keys:", keys)
        pick = {k: d.get(k) for k in ("ifPhoto","otherId","status","isClone","parentId","pptPlanId","timeLong","ifRefreshEwm","openCheckFaceFlag","ifopenAddress","viewPicPath","createType","source","appType") if isinstance(d, dict) and k in d}
        print("  signDetail:", json.dumps(pick, ensure_ascii=False))
        par = d.get("parentId") if isinstance(d, dict) else None
    except Exception as e:
        print("  signDetail ERR", r.status_code, repr(e), r.text[:120]); par = None

    r2 = requests.get(MOBILE + "v2/apis/active/getPPTActiveInfo", params={"activeId": aid},
                      headers={"Cookie": sck, "User-Agent": UA}, timeout=30)
    try:
        j2 = r2.json()
        d2 = j2.get("data") if isinstance(j2, dict) else None
        print("  pptActiveInfo:", json.dumps(d2, ensure_ascii=False)[:700] if d2 else j2)
    except Exception as e:
        print("  pptActiveInfo ERR", r2.status_code, r2.text[:120])

    # 教师活动页 content（含活动真实设置）
    r3 = requests.get(MOBILE + "widget/active/teaActiveView", params={"activePrimaryId": aid, "courseId": COURSE, "classId": CLAZZ, "uid": "[教师PUID]", "appType": "15"},
                      headers={"Cookie": tck, "User-Agent": UA}, timeout=30)
    body = r3.text or ""
    print("  teaActiveView HTTP %s len=%d" % (r3.status_code, len(body)))
    m = re.search(r'id="content"[^>]*>(.*?)</', body, re.S)
    for pat in (r'"content"\s*:\s*"((?:[^"\\]|\\.)*)"', r'signContent\s*=\s*[\'"](.*?)[\'"]'):
        mm = re.search(pat, body, re.S)
        if mm:
            try:
                c = mm.group(1).encode().decode("unicode_escape")
            except Exception:
                c = mm.group(1)
            print("  content:", c[:1200])
            break
    else:
        # 直接找 flag 名
        for kw in ("ifPhoto", "openCheckFaceFlag", "ifopenAddress", "photo", "auth"):
            hits = [m.start() for m in re.finditer(kw, body, re.I)][:3]
            for h in hits:
                print("   hit %s: %s" % (kw, body[max(0, h-70):h+90].replace("\n", " ")))
    if par:
        print("  >>> parentId=%s" % par)
print("done")