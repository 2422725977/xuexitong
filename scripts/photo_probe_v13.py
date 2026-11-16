# -*- coding: utf-8 -*-
"""v13：找 App 真正打开的那个签到页
1) 打印 activelist 条目全字段（看有没有 url/jurl 指向签到页）
2) 试 pptSign/preSign（dex 里唯一硬编码的签到页 URL，带 chatId）与 widget/sign/pcStuSignController
3) 保存页面并提取其 sign() 的参数集合
"""
import json, os, re
import requests
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
UA_APP = ('Mozilla/5.0 (Linux; Android 13; SM-G975F Build/TQ3A.230901.001) AppleWebKit/537.36 (KHTML, like Gecko) '
          'Version/4.0 Chrome/120.0.0.0 Mobile Safari/537.36 (schild:b1c2d3e4f5a60718) (device:SM-G975F) '
          'Language/zh_CN com.ssreader.ChaoXingStudy/ChaoXingStudy_3_6_2_android_phone_20230101')
MOBILE = "https://mobilelearn.chaoxing.com"
COURSE, CLAZZ, CHAT = "269282723", "159926750", "330606364917761"
AID = "4000180999320"
ck = open("ck.txt", encoding="utf-8").read().strip()
S = requests.Session(); S.headers.update({"Cookie": ck, "User-Agent": UA_APP})

r = S.get(MOBILE + "/v2/apis/active/student/activelist?fid=0&showNotStartedActive=0&courseId=%s&classId=%s" % (COURSE, CLAZZ), timeout=25)
jj = r.json()
for a in ((jj.get("data") or {}).get("activeList") or []):
    if str(a.get("id")) == AID:
        print("[activelist entry]", json.dumps(a, ensure_ascii=False))
        break
print("[list data keys]", sorted((jj.get("data") or {}).keys()))

def fetch(tag, url, method="GET", data=None):
    try:
        rr = S.post(url, data=data, timeout=25) if method == "POST" else S.get(url, timeout=25)
        t = rr.text
        print("[%s] %s len=%d" % (tag, rr.status_code, len(t)))
        if len(t) > 800 and "<" in t:
            open("out/page_%s.html" % tag, "w", encoding="utf-8").write(t)
            keys = ["newOpenPhoto", "objectId", "photoResult", "deviceCode", "CLIENT_CHOOSE_IMAGE", "enc",
                    "stuSignajax", "photoAuth", "camera", "camare", "signCode", "validate"]
            print("   marks:", json.dumps({k: t.count(k) for k in keys}))
            for m in re.finditer(r"url\s*=\s*[\"']([^\"']*stuSignajax[^\"']*)[\"']", t):
                print("   sign url:", m.group(1)[:400])
        else:
            print("   body:", t.strip()[:200])
        return t
    except Exception as e:
        print("[%s] ERR %s" % (tag, e)); return ""

fetch("pptSign_preSign_chatid", MOBILE + "/pptSign/preSign?activePrimaryId=%s&sys=1&chatId=%s&general=0&ls=1&appType=15&classId=%s&uid=493228247" % (AID, CHAT, CLAZZ))
fetch("pptSign_preSign_sys_tch", MOBILE + "/pptSign/preSign?activePrimaryId=%s&sys=1&chatId=%s&general=1&ls=1&appType=15&classId=%s&uid=493228247&isTeacherViewOpen=0" % (AID, CHAT, CLAZZ))
fetch("widget_pcStuSignController", MOBILE + "/widget/sign/pcStuSignController?activePrimaryId=%s&uid=493228247&courseId=%s&classId=%s&appType=15" % (AID, COURSE, CLAZZ))
fetch("newsign_preSign_GET", MOBILE + "/newsign/preSign?courseId=%s&classId=%s&activePrimaryId=%s&general=1&sys=1&ls=1&appType=15&uid=493228247&isTeacherViewOpen=0" % (COURSE, CLAZZ, AID))
