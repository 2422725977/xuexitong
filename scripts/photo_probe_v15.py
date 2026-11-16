# -*- coding: utf-8 -*-
"""v15：看照片页里的所有隐藏域与 enc 上下文；再取教师侧 showSignInfo（活动完整配置）"""
import json, os, re
import requests
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
UA_APP = ('Mozilla/5.0 (Linux; Android 13; SM-G975F Build/TQ3A.230901.001) AppleWebKit/537.36 (KHTML, like Gecko) '
          'Version/4.0 Chrome/120.0.0.0 Mobile Safari/537.36 (schild:b1c2d3e4f5a60718) (device:SM-G975F) '
          'Language/zh_CN com.ssreader.ChaoXingStudy/ChaoxingStudy_3_6_2_android_phone_20230101')
MOBILE = "https://mobilelearn.chaoxing.com"
AID = "4000180999320"
html = open("out/preSign_photo_v12_4000180999320.html", encoding="utf-8").read()
print("=== 页面隐藏域 ===")
for m in re.finditer(r"<input[^>]*>", html):
    print("  ", m.group(0)[:160])
print("=== enc 上下文 ===")
for m in re.finditer(r"enc", html):
    s = max(0, m.start() - 100)
    print("  ...", html[s:m.start() + 100].replace(chr(10), " ")[-200:])
print("=== 变量声明 ===")
for m in re.finditer(r"var\s+([A-Za-z_][A-Za-z0-9_]*)\s*=\s*([^;]{0,80});", html):
    print("  ", m.group(1), "=", m.group(2).strip()[:80])

tck = open("ck_tch.txt", encoding="utf-8").read().strip()
TS = requests.Session(); TS.headers.update({"Cookie": tck, "User-Agent": UA_APP})
print("\n=== 教师侧 showSignInfo ===")
for u in (MOBILE + "/sign/pcTeaSignController/showSignInfo?activeId=%s" % AID,
          MOBILE + "/sign/pcTeaSignController/showSignInfo?activeId=%s&appType=15" % AID):
    r = TS.get(u, timeout=25)
    print("[%s] %s len=%d" % (u.split("?")[-1][:60], r.status_code, len(r.text)))
    if len(r.text) > 500:
        open("out/tea_showSignInfo.html", "w", encoding="utf-8").write(r.text)
        print("   marks:", json.dumps({k: r.text.count(k) for k in ("photo", "Photo", "ifPhoto", "objectId", "content", "signCode", "auth")}))
        print("   body head:", r.text.strip()[:300].replace(chr(10), " "))
