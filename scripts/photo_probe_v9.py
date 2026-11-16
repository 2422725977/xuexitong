# -*- coding: utf-8 -*-
"""v9 探针：分辨 PCR007 是「账号侧」还是「请求侧」。
1) 打印学生 userinfo 的实名/单位类字段（isCertify / status / type / unitConfig / controlinfo / rights）
2) 用教师账号本人提交同一个拍照活动（puid=[教师PUID], fid=1022）→ 看错误码是否变化
3) 用带真 UA 参数 + 真姓名的组合再打一轮（此前的 v6/v7 里 name 真值 + useragent=AppUA 未同时命中）
"""
import json, os, sys, time, random, re
from urllib.parse import quote
import requests

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

UA_APP = ('Mozilla/5.0 (Linux; Android 13; SM-G975F Build/TQ3A.230901.001) '
          'AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/120.0.0.0 '
          'Mobile Safari/537.36 (schild:b1c2d3e4f5a60718) (device:SM-G975F) '
          'Language/zh_CN com.ssreader.ChaoXingStudy/ChaoxingStudy_3_6_2_android_phone_20230101')
UA_WEBVIEW = ('Mozilla/5.0 (Linux; U; Android 13; zh-cn; SM-G975F Build/TQ3A.230901.001) '
              'AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/120.0.0.0 Mobile Safari/537.36 '
              'com.chaoxing.mobile/ChaoXingStudy_6.7.8_android_phone')

COURSE = "269282723"
CLAZZ = "159926750"
AID = "4000180999320"          # v8 建的拍照活动
OID = "943f4d2e543135b82012c341971e905c"
MOBILE = "https://mobilelearn.chaoxing.com"
USERINFO = "https://sso.chaoxing.com/apis/login/userLogin4Uname.do"


def load_ck(path):
    ck = open(path, encoding="utf-8").read().strip()
    d = {}
    for part in ck.split(";"):
        if "=" in part:
            k, v = part.split("=", 1)
            d[k.strip()] = v.strip()
    return ck, d


def userinfo(ck, ua=UA_APP):
    r = requests.get(USERINFO, headers={"Cookie": ck, "User-Agent": ua}, timeout=20)
    try:
        return r.json().get("msg", {}) or {}
    except Exception:
        return {"_http": r.status_code, "_body": r.text[:200]}


def main():
    sck, scookie = load_ck("ck.txt")
    tck, tcookie = load_ck("ck_tch.txt")
    sm = userinfo(sck)
    tm = userinfo(tck)
    keep = ("isCertify", "status", "type", "roleid", "bindFanya", "codeInfo", "unitConfig",
            "controlinfo", "rights", "studentcode", "schoolname", "dxfid", "fid", "ppfid", "inputfid")
    print("[student acct]", json.dumps({k: sm.get(k) for k in keep}, ensure_ascii=False)[:900])
    print("[teacher acct]", json.dumps({k: tm.get(k) for k in keep}, ensure_ascii=False)[:900])

    def submit(tag, ck, ua_hdr, pairs, method="GET", extra_hdr=None):
        url = MOBILE + "/pptSign/stuSignajax?" + "&".join("%s=%s" % (k, quote(str(v), safe="")) for k, v in pairs)
        hdr = {"Cookie": ck, "User-Agent": ua_hdr, "Referer": MOBILE + "/newsign/preSign?activePrimaryId=" + AID,
               "X-Requested-With": "XMLHttpRequest"}
        if extra_hdr:
            hdr.update(extra_hdr)
        try:
            rr = requests.get(url, headers=hdr, timeout=30) if method == "GET" else requests.post(
                MOBILE + "/pptSign/stuSignajax", data=dict(pairs), headers=hdr, timeout=30)
            print("[%s] %s %s len=%d :: %s" % (tag, method, rr.status_code, len(rr.text), rr.text.strip()[:160]))
            return rr.text.strip()
        except Exception as e:
            print("[%s] ERR %s" % (tag, e))
            return "EXC"

    # 2) 教师本人提交（教师账号已绑定单位 1022/328749）
    t_pairs = [("activeId", AID), ("uid", "[教师PUID]"), ("clientip", ""), ("useragent", ""),
               ("latitude", "-1"), ("longitude", "-1"), ("appType", "15"), ("fid", "1022"),
               ("objectId", OID), ("name", "教师示例")]
    submit("T_teacher_as_signer", tck, UA_APP, t_pairs)
    submit("T_teacher_with_course", tck, UA_APP,
           [("activeId", AID), ("uid", "[教师PUID]"), ("fid", "1022"), ("courseId", COURSE), ("classId", CLAZZ),
            ("clientip", ""), ("appType", "15"), ("name", "教师示例"), ("useragent", ""), ("objectId", OID),
            ("latitude", "-1"), ("longitude", "-1")])

    # 3) 学生侧：真 UA 参数 + 真姓名组合
    for tag, ua_param, hdr_ua, name in (
        ("S_uaApp_param_realname", UA_APP, UA_APP, "学生示例"),
        ("S_uaWebview_param_realname", UA_WEBVIEW, UA_WEBVIEW, "学生示例"),
        ("S_uaApp_param_only", UA_APP, UA_APP, ""),
    ):
        pairs = [("activeId", AID), ("uid", "[学生PUID]"), ("clientip", ""), ("useragent", ua_param),
                 ("latitude", "-1"), ("longitude", "-1"), ("appType", "15"), ("fid", "0"),
                 ("objectId", OID), ("name", name), ("courseId", COURSE), ("classId", CLAZZ)]
        submit(tag, sck, hdr_ua, pairs)

    # cookie 里追加 fid / 学校 cookie 的变体
    pairs = [("activeId", AID), ("uid", "[学生PUID]"), ("clientip", ""), ("useragent", ""),
             ("latitude", "-1"), ("longitude", "-1"), ("appType", "15"), ("fid", "12"),
             ("objectId", OID), ("name", "学生示例")]
    submit("S_cookie_fid12", sck + "; fid=12", UA_APP, pairs)
    submit("S_cookie_spaceFid", sck, UA_APP, pairs)


if __name__ == "__main__":
    main()
