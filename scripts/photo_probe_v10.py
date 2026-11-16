# -*- coding: utf-8 -*-
"""v10 诊断：探测 photoAuthError_PCR007 的判定顺序（活动解析之前 / 之后）。
若伪造 activeId 也返 PCR007 -> 闸门在活动解析之前（纯请求形状）；
若返 活动不存在 -> 闸门在活动解析之后（活动配置/会话状态相关）。"""
import json, os, sys
from urllib.parse import quote
import requests

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
UA_APP = ('Mozilla/5.0 (Linux; Android 13; SM-G975F Build/TQ3A.230901.001) AppleWebKit/537.36 (KHTML, like Gecko) '
          'Version/4.0 Chrome/120.0.0.0 Mobile Safari/537.36 (schild:b1c2d3e4f5a60718) (device:SM-G975F) '
          'Language/zh_CN com.ssreader.ChaoXingStudy/ChaoxingStudy_3_6_2_android_phone_20230101')
MOBILE = "https://mobilelearn.chaoxing.com"
AID = "4000180999320"
OID = "943f4d2e543135b82012c341971e905c"
NORMAL_AID = "4000180998880"
ck = open("ck.txt", encoding="utf-8").read().strip()


def go(tag, pairs, cookie=True, hdr=True):
    url = MOBILE + "/pptSign/stuSignajax?" + "&".join("%s=%s" % (k, quote(str(v), safe="")) for k, v in pairs)
    h = {"User-Agent": UA_APP}
    if cookie:
        h["Cookie"] = ck
    if hdr:
        h["X-Requested-With"] = "XMLHttpRequest"
        h["Referer"] = MOBILE + "/newsign/preSign?activePrimaryId=" + AID
    try:
        r = requests.get(url, headers=h, timeout=25)
        print("[%-34s] %s len=%d :: %s" % (tag, r.status_code, len(r.text), r.text.strip()[:160]))
        return r.text.strip()
    except Exception as e:
        print("[%s] ERR %s" % (tag, e))
        return "EXC"


photo = lambda aid, uid, oid=OID: [("activeId", aid), ("uid", uid), ("clientip", ""), ("useragent", ""),
                                   ("latitude", "-1"), ("longitude", "-1"), ("appType", "15"), ("fid", "0"),
                                   ("objectId", oid), ("name", "学生示例")]

go("D1_no_cookie", photo(AID, "493228247"))
go("D2_bogus_aid", photo("9999999999999", "493228247"))
go("D3_bogus_uid", photo(AID, "1"))
go("D4_bogus_aid_uid", photo("9999999999999", "1"))
go("D5_normal_aid_photo_params", photo(NORMAL_AID, "493228247"))
go("D6_no_hdrs", photo(AID, "493228247"), hdr=False)
go("D7_only_aid", [("activeId", AID)])
go("D8_aid_uid_only", [("activeId", AID), ("uid", "493228247")])
go("D9_empty_objectId", photo(AID, "493228247", oid=""))
go("D10_old_photo_aid", photo("4000180999314", "493228247"))
