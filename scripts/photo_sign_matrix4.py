#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""拍照签到矩阵 v4 —— 照抄「真能跑通」的客户端配方（ASCII-58/cxsignfaker-hmos）

配方要点（源码逐字）：
  URL_SIGN   = https://mobilelearn.chaoxing.com/pptSign/stuSignajax?&clientip=&appType=15
               &ifTiJiao=1&vpProbability=-1&vpStrategy=
  URL_PRE_SIGN = https://mobilelearn.chaoxing.com/newsign/preSign?&general=1&sys=1&ls=1&appType=15
                 &isTeacherViewOpen=0   —— **POST 表单 ext=**
  preSign 之后必须回传行为分析：
    GET /pptSign/analysis?vs=1&DB_STRATEGY=RANDOM&aid=<aid>  ->  HTML 里 code='+'(hex)
    GET /pptSign/analysis2?DB_STRATEGY=RANDOM&code=<hex>
  提交参数 = {activeId,latitude,longitude,address,enc,objectId,signCode,location}
             + {uid, name=uname(真实姓名), fid=getUserInfo 的 fid} + {deviceCode}
  真姓名/单位：GET https://sso.chaoxing.com/apis/login/userLogin4Uname.do（仅带 Cookie）
  图片必须随机差异化（服务端有重复图片检测）：随机裁剪 90%~99% + 随机质量重编码（85~95）
"""
import argparse, json, os, random, re, sys, time, urllib.parse
import requests
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cx_pipeline as C  # noqa: E402

MOBILE = "https://mobilelearn.chaoxing.com"
SIGN_URL = MOBILE + "/pptSign/stuSignajax?&clientip=&appType=15&ifTiJiao=1&vpProbability=-1&vpStrategy="
PRE_URL = MOBILE + "/newsign/preSign?&general=1&sys=1&ls=1&appType=15&isTeacherViewOpen=0"
ANALYSIS = MOBILE + "/pptSign/analysis?vs=1&DB_STRATEGY=RANDOM"
ANALYSIS2 = MOBILE + "/pptSign/analysis2?DB_STRATEGY=RANDOM"
USERINFO = "https://sso.chaoxing.com/apis/login/userLogin4Uname.do"
PANTOKEN = "https://pan-yz.chaoxing.com/api/token/uservalid"
PANUPLOAD = "https://pan-yz.chaoxing.com/upload?_from=mobilelearn"
COURSE, CLAZZ, SID, TUID = "269282723", "159926750", "493228247", "401537379"
UA = ("Mozilla/5.0 (Linux; Android 13; SM-G975F Build/TQ3A.230901.001) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Version/4.0 Chrome/120.0.0.0 Mobile Safari/537.36 (schild:b1c2d3e4f5a60718) "
      "(device:SM-G975F) Language/zh_CN com.ssreader.ChaoXingStudy/ChaoXingStudy_3_6_2_android_phone_20230101")
LOG = []


def log(t, m):
    s = "[%s] %s" % (t, m); print(s, flush=True); LOG.append(s)


def ck(p): return open(p, encoding="utf-8", errors="ignore").read().strip()


def randomize(src, dst):
    """随机裁剪 90%~99% + 随机 JPEG 质量重编码"""
    im = Image.open(src).convert("RGB")
    W, H = im.size
    cw, ch = [max(1, int(v * random.uniform(0.90, 0.99))) for v in (W, H)]
    x, y = random.randrange(0, W - cw + 1), random.randrange(0, H - ch + 1)
    im.crop((x, y, x + cw, y + ch)).save(dst, "JPEG", quality=random.randint(85, 95))
    return dst


def user_info(cookies):
    r = requests.get(USERINFO, headers={"Cookie": cookies}, timeout=20)
    try:
        j = r.json(); m = j.get("msg") or {}
        return {"name": m.get("name") or "", "uid": str(m.get("uid") or ""), "fid": str(m.get("fid") or ""),
                "puid": str(m.get("puid") or ""), "clientId": m.get("clientId") or ""}
    except Exception:
        return {"name": "", "uid": "", "fid": "", "puid": "", "clientId": "", "raw": r.text[:200]}


def pre_sign(cookies, aid, uid, ext=""):
    h = {"Cookie": cookies, "User-Agent": UA}
    q = {"activePrimaryId": aid, "classId": CLAZZ, "courseId": COURSE, "uid": uid}
    r = requests.post(PRE_URL, params=q, data={"ext": ext}, headers=h, timeout=30)
    body = r.text or ""
    open("out/preSign_photo_v4.html", "w", encoding="utf-8").write(body)
    encs = []
    for p in (r'name="enc"[^>]*value="([^"]{8,})"', r'"enc"\s*:\s*"([^"]{8,})"', r"enc\s*=\s*'([A-Za-z0-9+/=_-]{10,})'"):
        m = re.search(p, body)
        if m:
            encs.append(m.group(1)); break
    return {"http": r.status_code, "len": len(body), "enc": encs[0] if encs else "", "ext_used": ext}


def analysis(cookies, aid):
    h = {"Cookie": cookies, "User-Agent": UA}
    r1 = requests.get(ANALYSIS, params={"aid": aid}, headers=h, timeout=30)
    m = re.search(r"code='\+'([a-f0-9]+)'", r1.text or "")
    code = m.group(1) if m else ""
    r2 = requests.get(ANALYSIS2, params={"code": code}, headers=h, timeout=30) if code else None
    return {"http": r1.status_code, "code": code, "http2": (r2.status_code if r2 else None),
            "body2": (r2.text[:120] if r2 else "")}


def upload(cookies, path, token):
    with open(path, "rb") as f: data = f.read()
    r = requests.post(PANUPLOAD + "&_token=" + urllib.parse.quote(token),
                      headers={"Cookie": cookies, "User-Agent": UA},
                      files={"file": (os.path.basename(path), data, "image/jpeg")},
                      data={"puid": SID}, timeout=60)
    j = r.json(); log("U", "upload rc=%s objectId=%s msg=%s" % (r.status_code, j.get("objectId"), j.get("msg")))
    return str(j.get("objectId") or "")


def submit(cookies, aid, ui, oid, if_ti_jiao=True, post=False, with_photo_result=False, dc="DEVICECODE"):
    q = {"clientip": "", "appType": "15", "vpProbability": "-1", "vpStrategy": "",
         "activeId": aid, "latitude": "-1", "longitude": "-1",
         "uid": ui["uid"], "name": ui["name"], "fid": ui["fid"], "deviceCode": dc}
    if if_ti_jiao:
        q["ifTiJiao"] = "1"
    if oid:
        q["objectId"] = oid
        if with_photo_result:
            q["photoResult"] = json.dumps({"files": json.dumps([{"name": "1.jpg", "objectid": oid, "type": "jpg"}])})
    h = {"Cookie": cookies, "User-Agent": UA, "X-Requested-With": "XMLHttpRequest",
         "Referer": MOBILE + "/newsign/preSign?activePrimaryId=0"}
    r = (requests.post(SIGN_URL, params=q, data=q, headers=h, timeout=30) if post
         else requests.get(SIGN_URL, params=q, headers=h, timeout=30))
    b = (r.text or "").strip()
    return {"http": r.status_code, "body": b[:200], "ok": b.lower().startswith("success") or "签到成功" in b}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--img", default="/tmp/cx29/face2.jpg")
    ap.add_argument("--aid", default="")
    ap.add_argument("--time-long", default="1800000")
    a = ap.parse_args()
    sck, tck = ck("ck.txt"), ck("ck_tch.txt")

    ui = user_info(sck)
    log("+", "userInfo: name=%r fid=%r puid=%r uid=%r clientId=%s" %
        (ui["name"], ui["fid"], ui["puid"], ui["uid"], (ui["clientId"] or "")[:16]))

    aid = a.aid
    if not aid:
        t = C.TeacherSide(tck, TUID, quiet_hours=None, max_writes_per_hour=40, min_interval=0.5)
        aid = t.create_sign(COURSE, CLAZZ, other_id="0", if_photo="1", face="0", time_long=a.time_long,
                            start=True, title="拍照矩阵v4")
    log("+", "activeId=%s" % aid)

    img = randomize(a.img, "out/photo_v4_%d.jpg" % int(time.time()))
    log("+", "随机差异化图片 -> %s (%d B)" % (img, os.path.getsize(img)))
    token = str(requests.get(PANTOKEN, headers={"Cookie": sck, "User-Agent": UA}, timeout=20).json().get("_token") or "")
    oid = upload(sck, img, token) if token else ""
    if not oid:
        return 2

    pre = pre_sign(sck, aid, ui["puid"] or ui["uid"])
    log("+", "preSign(POST ext) -> HTTP %s len=%d enc=%s" % (pre["http"], pre["len"], pre["enc"][:24]))
    an = analysis(sck, aid)
    log("+", "analysis -> HTTP %s code=%s analysis2=%s %s" % (an["http"], an["code"], an["http2"], an["body2"][:60]))

    cases = [
        ("Y01", "完整配方：preSign + analysis + ifTiJiao=1 + vpProbability=-1 + objectId（GET）", True, False, False),
        ("Y02", "同 Y01 但 ifTiJiao=0", False, False, False),
        ("Y03", "同 Y01 但带 photoResult", True, False, True),
        ("Y04", "同 Y01 但 POST 表单", True, True, False),
    ]
    res, win = [], ""
    for tag, desc, tiao, post, pr in cases:
        pre_sign(sck, aid, ui["puid"] or ui["uid"]); analysis(sck, aid)
        r = submit(sck, aid, ui, oid, tiao, post, pr)
        log("=", "%s -> HTTP %s %s" % (tag, r["http"], r["body"]))
        res.append({"tag": tag, "desc": desc, **r})
        if r["ok"]:
            win = tag; break
        time.sleep(1.5)
    json.dump({"aid": aid, "oid": oid, "img": img, "userinfo": ui, "pre": pre, "analysis": an,
               "results": res, "winner": win}, open("out/photo_matrix4.json", "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    log("*", "结果：%s" % ("成功 " + win if win else "全部失败"))
    return 0 if win else 2


if __name__ == "__main__":
    sys.exit(main())
