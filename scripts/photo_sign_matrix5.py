#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""拍照签到矩阵 v5 —— 补上 preSign 的 ext（活动列表 data.ext._from_），并修正 uid/name/fid 来源

新证据：
  - GET /v2/apis/active/student/activelist?fid=0&showNotStartedActive=0&courseId=&classId=
      -> data.ext._from_ = "<courseId>_<classId>_<puid>_<md5>"   ← preSign POST 的 ext 参数
  - sso.chaoxing.com/apis/login/userLogin4Uname.do -> msg.name="学生示例" msg.puid=[学生PUID] msg.fid=0
      -> 提交参数 uid=puid、name=真实姓名、fid=该 fid（0）
"""
import json, os, random, re, sys, time, urllib.parse
import requests
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from photo_sign_matrix4 import (MOBILE, SIGN_URL, PRE_URL, ANALYSIS, ANALYSIS2, USERINFO, PANTOKEN,
                                PANUPLOAD, COURSE, CLAZZ, SID, TUID, UA, ck, randomize, user_info, upload, log)

ACTIVELIST = MOBILE + "/v2/apis/active/student/activelist"


def class_ext(cookies):
    r = requests.get(ACTIVELIST, params={"fid": "0", "showNotStartedActive": "0",
                                         "courseId": COURSE, "classId": CLAZZ},
                     headers={"Cookie": cookies, "User-Agent": UA}, timeout=25)
    try:
        return str(((r.json().get("data") or {}).get("ext") or {}).get("_from_") or "")
    except Exception:
        return ""


def pre_sign_ext(cookies, aid, uid, ext):
    r = requests.post(PRE_URL, params={"activePrimaryId": aid, "classId": CLAZZ, "courseId": COURSE, "uid": uid},
                      data={"ext": ext}, headers={"Cookie": cookies, "User-Agent": UA}, timeout=30)
    open("out/preSign_photo_v5.html", "w", encoding="utf-8").write(r.text or "")
    return {"http": r.status_code, "len": len(r.text or "")}


def analysis(cookies, aid):
    h = {"Cookie": cookies, "User-Agent": UA}
    r1 = requests.get(ANALYSIS, params={"aid": aid}, headers=h, timeout=30)
    m = re.search(r"code='\+'([a-f0-9]+)'", r1.text or "")
    code = m.group(1) if m else ""
    r2 = requests.get(ANALYSIS2, params={"code": code}, headers=h, timeout=30) if code else None
    return {"code": code, "http2": (r2.status_code if r2 else None), "body2": (r2.text[:60] if r2 else "")}


def submit(cookies, aid, extra):
    q = {"clientip": "", "appType": "15", "ifTiJiao": "1", "vpProbability": "-1", "vpStrategy": "",
         "activeId": aid, "latitude": "-1", "longitude": "-1"}
    q.update(extra)
    h = {"Cookie": cookies, "User-Agent": UA, "X-Requested-With": "XMLHttpRequest",
         "Referer": MOBILE + "/newsign/preSign?activePrimaryId=0"}
    r = requests.get(SIGN_URL, params=q, headers=h, timeout=30)
    b = (r.text or "").strip()
    return {"http": r.status_code, "body": b[:220], "ok": b.lower().startswith("success") or "签到成功" in b}


def main():
    sck, tck = ck("ck.txt"), ck("ck_tch.txt")
    ui = user_info(sck)
    ext = class_ext(sck)
    log("+", "userInfo name=%r puid=%r fid=%r" % (ui["name"], ui["puid"] or SID, ui["fid"]))
    log("+", "class ext = %s" % ext)
    pg = {"uid": ui["puid"] or SID, "name": ui["name"], "fid": ui["fid"] or "0", "signCode": "", "location": "",
          "deviceCode": "b1c2d3e4f5a6071823456789abcdef01"}

    t = C_TEACHER = None
    import cx_pipeline as C
    t = C.TeacherSide(tck, TUID, quiet_hours=None, max_writes_per_hour=40, min_interval=0.5)
    aid = t.create_sign(COURSE, CLAZZ, other_id="0", if_photo="1", face="0", time_long="1800000",
                        start=True, title="拍照矩阵v5")
    log("+", "activeId=%s" % aid)

    img = randomize("/tmp/cx29/face2.jpg", "out/photo_v5_%d.jpg" % int(time.time()))
    token = str(requests.get(PANTOKEN, headers={"Cookie": sck, "User-Agent": UA}, timeout=20).json().get("_token") or "")
    oid = upload(sck, img, token) if token else ""
    if not oid:
        return 2
    log("+", "objectId=%s" % oid)

    pre = pre_sign_ext(sck, aid, pg["uid"], ext)
    an = analysis(sck, aid)
    log("+", "preSign(POST ext=%s) -> %s ; analysis code=%s/%s" % (ext[:24], pre, an["code"][:16], an["body2"]))

    full_pr = json.dumps({"files": json.dumps([{
        "result": "1", "resid": "0", "objectid": oid, "thumbnail": "https://p.cldisk.com/star3/312_412c/%s.jpg" % oid,
        "name": os.path.basename(img), "fid": pg["fid"], "isMirror": "0", "mirrorConfig": "",
        "type": "jpg", "camera": "1", "camare": "5", "width": "0", "height": "0", "datasize": str(os.path.getsize(img))}]),
        "result": "1"})
    cases = [
        ("Z01", "ext preSign + analysis + objectId + name/fid/uid 真值", {"objectId": oid}),
        ("Z02", "同 Z01 但 photoResult=d$f 全字段形状", {"objectId": oid, "photoResult": full_pr}),
        ("Z03", "同 Z01 但无 objectId（对照）", {}),
        ("Z04", "同 Z01 但 fid=12（cookie spaceFid）", {"objectId": oid, "fid": "12"}),
        ("Z05", "同 Z01 但 name 空", {"objectId": oid, "name": ""}),
    ]
    res, win = [], ""
    for tag, desc, ex in cases:
        pre_sign_ext(sck, aid, pg["uid"], ext); analysis(sck, aid)
        q = dict(pg); q.update(ex)
        r = submit(sck, aid, q)
        log("=", "%s -> HTTP %s %s" % (tag, r["http"], r["body"]))
        res.append({"tag": tag, "desc": desc, **r})
        if r["ok"]:
            win = tag; break
        time.sleep(1.5)
    json.dump({"aid": aid, "oid": oid, "userinfo": ui, "ext": ext, "results": res, "winner": win},
              open("out/photo_matrix5.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    log("*", "结果：%s" % ("成功 " + win if win else "全部失败"))
    return 0 if win else 2


if __name__ == "__main__":
    sys.exit(main())
