#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""打印拍照活动的 configJson / editconfig / iphoneContent / url 与 pptActiveInfo 全文"""
import json, sys, os
import requests
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
MOBILE = "https://mobilelearn.chaoxing.com/"
UA = ("Mozilla/5.0 (Linux; Android 13; SM-G975F Build/TQ3A.230901.001) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Version/4.0 Chrome/120.0.0.0 Mobile Safari/537.36 (schild:b1c2d3e4f5a60718) "
      "(device:SM-G975F) Language/zh_CN com.ssreader.ChaoXingStudy/ChaoXingStudy_3_6_2_android_phone_20230101")
sck = open("ck.txt", encoding="utf-8", errors="ignore").read().strip()
aid = sys.argv[1] if len(sys.argv) > 1 else "4000180999265"
j = requests.get(MOBILE + "newsign/signDetail", params={"activePrimaryId": aid, "type": "1"},
                 headers={"Cookie": sck, "User-Agent": UA}, timeout=30).json()
d = j.get("data", j)
for k in ("configJson", "editconfig", "iphoneContent", "url", "name", "activeType", "activeSort", "activityTranMode", "bsid", "chartId", "sfdp", "sffxs", "showhide", "sxs", "zhjsid", "dpurl", "jurl"):
    print("--- %s ---" % k)
    print(json.dumps(d.get(k), ensure_ascii=False)[:2000])
print("=== pptActiveInfo 全文 ===")
j2 = requests.get(MOBILE + "v2/apis/active/getPPTActiveInfo", params={"activeId": aid},
                  headers={"Cookie": sck, "User-Agent": UA}, timeout=30).json()
print(json.dumps(j2.get("data", j2), ensure_ascii=False, indent=1)[:3000])