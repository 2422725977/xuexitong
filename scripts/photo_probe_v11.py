# -*- coding: utf-8 -*-
"""v11：两条新线索
A) 枚举学生所有课程/班级的活动 -> 找别人（真实教师）建的 ifPhoto=1 活动，试拍照签到（判断是不是我们 API 建的活
动本身缺服务端 photoAuth 供给）
B) 群聊路径 /sign/preStuSign + /sign/stuSignajax（CarryWS 成功案例与 cxsign CHAT_GROUP 用的路径）
"""
import json, os, re, sys
from urllib.parse import quote
import requests

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
UA_APP = ('Mozilla/5.0 (Linux; Android 13; SM-G975F Build/TQ3A.230901.001) AppleWebKit/537.36 (KHTML, like Gecko) '
          'Version/4.0 Chrome/120.0.0.0 Mobile Safari/537.36 (schild:b1c2d3e4f5a60718) (device:SM-G975F) '
          'Language/zh_CN com.ssreader.ChaoXingStudy/ChaoxingStudy_3_6_2_android_phone_20230101')
MOBILE = "https://mobilelearn.chaoxing.com"
AID = "4000180999320"
OID = "943f4d2e543135b82012c341971e905c"
ck = open("ck.txt", encoding="utf-8").read().strip()
S = requests.Session()
S.headers.update({"Cookie": ck, "User-Agent": UA_APP})

print("=== A. 课程/班级/活动枚举 ===")
r = S.get("https://mooc1-api.chaoxing.com/mycourse/backclazzdata?view=json&rss=1", timeout=25)
courses = []
try:
    for c in r.json().get("channelList") or []:
        content = c.get("content") or {}
        for cd in (content.get("course") or {}).get("data") or []:
            rec = {"courseId": str(cd.get("id")), "name": cd.get("name"), "school": cd.get("belongSchoolId"),
                   "classId": str(c.get("key")), "className": content.get("name"), "chatid": content.get("chatid")}
            courses.append(rec)
except Exception as e:
    print("parse err", e)
print("[courses]", json.dumps(courses, ensure_ascii=False)[:1200])

photo_acts = []
for co in courses:
    try:
        rr = S.get(MOBILE + "/v2/apis/active/student/activelist?fid=0&showNotStartedActive=0&courseId=%s&classId=%s"
                   % (co["courseId"], co["classId"]), timeout=25)
        jj = rr.json()
        for a in ((jj.get("data") or {}).get("activeList") or []):
            aid = str(a.get("id"))
            d = S.get(MOBILE + "/newsign/signDetail?activePrimaryId=%s&type=1" % aid, timeout=25)
            try:
                dj = d.json()
            except Exception:
                dj = {}
            if str(dj.get("ifPhoto")) == "1" or str(dj.get("ifphoto")) == "1":
                photo_acts.append({"aid": aid, "course": co["courseId"], "class": co["classId"],
                                   "name": a.get("nameOne"), "otherId": dj.get("otherId"),
                                   "status": dj.get("status"), "createUid": dj.get("createUid"),
                                   "startTime": dj.get("startTime"), "chatid": co["chatid"]})
    except Exception as e:
        print("[activelist err]", co["courseId"], e)
print("[photo activities found]", json.dumps(photo_acts, ensure_ascii=False)[:1500])

print("\n=== B. 群聊路径 ===")
def go(tag, url, data=None, method="GET"):
    try:
        rr = S.get(url, timeout=25) if method == "GET" else S.post(url, data=data, timeout=25)
        print("[%-30s] %s len=%d :: %s" % (tag, rr.status_code, len(rr.text), rr.text.strip().replace("\n", " ")[:200]))
        return rr
    except Exception as e:
        print("[%s] ERR %s" % (tag, e))
        return None

CHAT = courses[0]["chatid"] if courses and courses[0].get("chatid") else "330606364917761"
go("B1_preStuSign", MOBILE + "/sign/preStuSign?activeId=%s&chatId=%s&uid=[学生PUID]&courseId=%s&classId=%s"
   % (AID, CHAT, courses[0]["courseId"] if courses else "269282723", courses[0]["classId"] if courses else "159926750"))
base = [("activeId", AID), ("uid", "[学生PUID]"), ("clientip", ""), ("useragent", ""), ("latitude", "-1"),
        ("longitude", "-1"), ("appType", "15"), ("fid", "0"), ("objectId", OID), ("name", "学生示例")]
go("B2_chat_sign_GET", MOBILE + "/sign/stuSignajax?" + "&".join("%s=%s" % (k, quote(str(v), safe="")) for k, v in base))
go("B3_chat_sign_POST", MOBILE + "/sign/stuSignajax", dict(base), "POST")
go("B4_chat_sign_no_photo", MOBILE + "/sign/stuSignajax?activeId=%s&uid=[学生PUID]&fid=0&appType=15" % AID)
