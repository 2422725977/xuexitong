# -*- coding: utf-8 -*-
"""学生页面/接口里到底藏没藏「签到码 / 手势 / 位置坐标」——决定能否纯远程签成。"""
import json, os, re, sys, time
import requests
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cx_pipeline as C
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

UA_APP = ('Mozilla/5.0 (Linux; Android 13; SM-G975F Build/TQ3A.230901.001) AppleWebKit/537.36 (KHTML, like Gecko) '
          'Version/4.0 Chrome/120.0.0.0 Mobile Safari/537.36 (schild:26f6a66da55ad239903fba6f674e8c66) (device:SM-G975F) '
          'Language/zh_CN com.ssreader.ChaoXingStudy/ChaoXingStudy_3_6_2_android_phone_20230101')
MOBILE = "https://mobilelearn.chaoxing.com"
COURSE, CLAZZ, SUID = "269282723", "159926750", "[学生PUID]"
CODE_AID, GEST_AID, LOC_AID = "4000182047286", "4000182047307", "4000182047327"
CODE_VAL, GEST_VAL = "246810", "147258"
TEACH_LAT, TEACH_LON = "30.71142640936642", "103.868397592583"
sck = open("ck.txt", encoding="utf-8").read().strip()
S = requests.Session(); S.headers.update({"Cookie": sck, "User-Agent": UA_APP})
out = {"ts": time.strftime("%Y-%m-%d %H:%M:%S"), "pages": {}, "api": {}}
os.makedirs("out/stupages_remote", exist_ok=True)

PAGES = {
  "code_presSign_newsign": (MOBILE + "/newsign/preSign", {"activePrimaryId": CODE_AID, "sys": "1", "ls": "1", "appType": "15", "courseId": COURSE, "classId": CLAZZ, "uid": SUID}),
  "code_presSign_ppt": (MOBILE + "/pptSign/preSign", {"activePrimaryId": CODE_AID, "sys": "1", "appType": "15", "courseId": COURSE, "classId": CLAZZ, "uid": SUID}),
  "gest_presSign_newsign": (MOBILE + "/newsign/preSign", {"activePrimaryId": GEST_AID, "sys": "1", "ls": "1", "appType": "15", "courseId": COURSE, "classId": CLAZZ, "uid": SUID}),
  "loc_presSign_newsign": (MOBILE + "/newsign/preSign", {"activePrimaryId": LOC_AID, "sys": "1", "ls": "1", "appType": "15", "courseId": COURSE, "classId": CLAZZ, "uid": SUID}),
  "loc_teaview": (MOBILE + "/widget/active/teaActiveView", {"activeId": LOC_AID}),
  "code_gettasksign": (MOBILE + "/pptSign/gotasksign", {"courseId": COURSE, "classId": CLAZZ, "uid": SUID, "activePrimaryId": CODE_AID, "appType": "15"}),
}
for name, (url, params) in PAGES.items():
    try:
        r = S.get(url, params=params, timeout=30)
        html = r.text
        p = "out/stupages_remote/%s.html" % name
        open(p, "w", encoding="utf-8").write(html)
        sig = {}
        for label, pat in [("signCode_hidden", r'id="signCode"[^>]*value="([^"]*)"'),
                           ("signCode_var", r'signCode\s*[=:]\s*[\'"]?([0-9A-Za-z]{3,})'),
                           ("code_246810", re.escape(CODE_VAL)),
                           ("code_147258", re.escape(GEST_VAL)),
                           ("teach_lat", re.escape(TEACH_LAT[:10])),
                           ("teach_lon", re.escape(TEACH_LON[:10])),
                           ("locationLatitude", r"locationLatitude[^,;]{0,40}"),
                           ("locationText", r"locationText[^,;]{0,50}"),
                           ("enc_hex", r'encs*=s*"([0-9A-Fa-f]{16,64})"')]:
            m = re.findall(pat, html)
            if m:
                sig[label] = (m[:3] if isinstance(m[0], str) else m[:3])
        out["pages"][name] = {"http": r.status_code, "len": len(html), "sig": sig, "file": p}
        print("%-24s HTTP %s len=%-7d %s" % (name, r.status_code, len(html), json.dumps(sig, ensure_ascii=False)[:300]))
    except Exception as e:
        out["pages"][name] = {"err": str(e)}; print("%-24s ERR %s" % (name, e))

print()
print("===== 活动内容接口 =====")
API = [
    ("pptgetActiveDataV2", "ppt/taskAPI/getActiveDataV2", {"activeId": LOC_AID}),
    ("pptgetActiveDataV2_code", "ppt/taskAPI/getActiveDataV2", {"activeId": CODE_AID}),
    ("stuActivelist_all", "v2/apis/active/student/activelist", {"fid": "0", "courseId": COURSE, "classId": CLAZZ, "showNotStartedActive": "1", "_": str(int(time.time()*1000))}),
]
for name, path, p in API:
    try:
        r = S.get(MOBILE + "/" + path, params=p, timeout=30)
        t = r.text
        open("out/stupages_remote/%s.json" % name, "w", encoding="utf-8").write(t)
        d = {}
        try: d = r.json()
        except Exception: pass
        hit = {}
        if name.startswith("pptget"):
            data = d.get("data") or {}
            hit = {k: data[k] for k in data if re.search(r"loc|lat|lon|code|enc|range|addr", str(k), re.I)}
        out["api"][name] = {"http": r.status_code, "len": len(t), "hit": hit}
        print("%-22s HTTP %s len=%-7d %s" % (name, r.status_code, len(t), json.dumps(hit, ensure_ascii=False)[:400]))
    except Exception as e:
        out["api"][name] = {"err": str(e)}; print("%-22s ERR %s" % (name, e))

json.dump(out, open("out/stu_read_secret2.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print()
print("[saved] out/stu_read_secret2.json")
