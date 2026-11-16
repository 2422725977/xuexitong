# -*- coding: utf-8 -*-
"""v14：T1 教师能否签普通活动（判断教师 PCR007 是否有信息量）
T2 教师页里群聊签到的创建入口（chatId/groupId/sign 相关端点）"""
import json, os, re
from urllib.parse import quote
import requests
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
UA_APP = ('Mozilla/5.0 (Linux; Android 13; SM-G975F Build/TQ3A.230901.001) AppleWebKit/537.36 (KHTML, like Gecko) '
          'Version/4.0 Chrome/120.0.0.0 Mobile Safari/537.36 (schild:b1c2d3e4f5a60718) (device:SM-G975F) '
          'Language/zh_CN com.ssreader.ChaoXingStudy/ChaoxingStudy_3_6_2_android_phone_20230101')
MOBILE = "https://mobilelearn.chaoxing.com"
tck = open("ck_tch.txt", encoding="utf-8").read().strip()
TS = requests.Session(); TS.headers.update({"Cookie": tck, "User-Agent": UA_APP})

print("=== T1 教师签普通活动 / 拍照活动 ===")
for tag, aid in (("normal_4000180998880", "4000180998880"), ("photo_v8", "4000180999320")):
    url = MOBILE + "/pptSign/stuSignajax?" + "&".join("%s=%s" % (k, quote(str(v), safe="")) for k, v in
        [("activeId", aid), ("uid", "401537379"), ("clientip", ""), ("useragent", ""), ("latitude", "-1"),
         ("longitude", "-1"), ("appType", "15"), ("fid", "1022"), ("name", "教师示例"), ("courseId", "269282723"), ("classId", "159926750")])
    rr = TS.get(url, timeout=25)
    print("[%s] %s :: %s" % (tag, rr.status_code, rr.text.strip()[:120]))

print("\n=== T2 教师页里的签到/群聊端点 ===")
html = open("out/tchpages/v4_gotasksign_nocaid.html", encoding="utf-8").read()
print("len", len(html))
for pat in (r'/sign/[a-zA-Z0-9_/?=&.%-]{2,80}', r'chatId[^,;]{0,60}', r'groupId[^,;]{0,40}', r'newTaskSign[^"\\\']{0,60}'):
    hits = sorted(set(re.findall(pat, html)))[:20]
    print("--", pat, "->", json.dumps(hits, ensure_ascii=False)[:900])
