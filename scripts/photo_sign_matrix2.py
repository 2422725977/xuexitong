#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""拍照签到矩阵 v2：把 fid 从 0 改成「用户自己的 fid」（H5 里 fid 来自 AppUtils.getUserInfo().fid）

新证据：out/stupages_puphoto_4000180998737.html
  - 第 132 行 $("#fid").val(object.fid)  ← AppUtils.getUserInfo('', cb) 的 object.fid（不是 0）
  - 第 88 行 hidden #fid 默认 "0"（仅在 getUserInfo 未回调时兜底）
  - 第 270-276 行 $.ajax({url:'/pptSign/stuSignajax', type:"post", data: params})  ← **真身是 POST 表单**
  - params.photoResult = PHOTO_RESULT（{"files":"<内层 json 字符串>"}）
  学生 cookie 里 spaceFid=12（教师 1022）→ 候选真实 fid。

用法：python3 photo_sign_matrix2.py [--aid X] [--fid 12]
"""
import argparse
import base64
import json
import os
import sys
import time
import urllib.parse

import requests

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cx_pipeline as C  # noqa: E402

MOBILE = "https://mobilelearn.chaoxing.com/"
PANUPLOAD = "https://pan-yz.chaoxing.com/upload"
PANTOKEN = "https://pan-yz.chaoxing.com/api/token/uservalid"
COURSE, CLAZZ = "269282723", "159926750"
TUID, SID = "[教师PUID]", "[学生PUID]"
DEVKEY = "QrCbNY@MuK1X8HGw"
OAID = "b1c2d3e4f5a60718"
UA_APP = ("Mozilla/5.0 (Linux; Android 10; SM-G975F Build/QP1A.190711.020; wv) "
          "AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/80.0.3987.99 Mobile Safari/537.36")
LOG = []


def log(t, m):
    s = "[%s] %s" % (t, m)
    print(s, flush=True)
    LOG.append(s)


def load_ck(v):
    if v and os.path.exists(v):
        with open(v, "r", encoding="utf-8", errors="ignore") as f:
            return f.read().strip()
    return (v or "").strip()


def device_code(uid_str):
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    key = DEVKEY.encode()
    raw = uid_str.encode()
    pad = 16 - (len(raw) % 16)
    enc = Cipher(algorithms.AES(key), modes.ECB()).encryptor()
    return base64.b64encode(enc.update(raw + bytes([pad]) * pad) + enc.finalize()).decode()


def upload(ck, path, token, extra):
    url = PANUPLOAD + "?_from=mobilelearn&_token=" + urllib.parse.quote(token)
    with open(path, "rb") as f:
        data = f.read()
    form = {"puid": SID}
    form.update(extra)
    try:
        r = requests.post(url, headers={"Cookie": ck, "User-Agent": UA_APP},
                          files={"file": ("1.png", data, "image/png")}, data=form, timeout=60)
        j = r.json()
    except Exception as e:
        log("!", "上传失败 extra=%s -> %r" % (extra, e))
        return {}
    log("U", "extra=%s -> %s" % (extra, json.dumps(j, ensure_ascii=False)[:200]))
    return j


def submit(ck, aid, params, method):
    url = MOBILE + "pptSign/stuSignajax"
    h = {"Cookie": ck, "User-Agent": UA_APP}
    if method == "POST":
        h["X-Requested-With"] = "XMLHttpRequest"
        r = requests.post(url, headers=h, data=params, timeout=30)
    else:
        r = requests.get(url + "?" + urllib.parse.urlencode(params), headers=h, timeout=30)
    body = (r.text or "").strip()
    ok = ("success" in body.lower()) or ("签到成功" in body)
    return {"ok": ok, "http": r.status_code, "body": body[:300]}


def params_for(aid, oid, fid, dc, ua_param, with_pr, name="1.png", pr_shape="nested"):
    p = [("activeId", str(aid)), ("courseId", COURSE), ("uid", SID), ("clientip", ""),
         ("useragent", ua_param), ("latitude", "-1"), ("longitude", "-1"),
         ("appType", "15"), ("fid", fid), ("objectId", oid), ("name", name),
         ("validate", ""), ("deviceCode", dc if dc else "")]
    if with_pr:
        inner = [{"name": name, "objectid": oid, "type": "png"}]
        if pr_shape == "nested":
            p.append(("photoResult", json.dumps({"files": json.dumps(inner, separators=(",", ":"))},
                                                separators=(",", ":"))))
        else:
            p.append(("photoResult", json.dumps({"files": inner}, separators=(",", ":"))))
    return p


def run_variant(tag, desc, ck, aid, params, method):
    res = submit(ck, aid, params, method)
    log("=", "%s [%s] %s -> HTTP %s %s" % (tag, method, desc, res["http"], res["body"][:150]))
    time.sleep(1.2)
    return {"tag": tag, "desc": desc, "method": method, "ok": res["ok"],
            "http": res["http"], "body": res["body"]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--aid", default="")
    ap.add_argument("--fid", default="12")
    ap.add_argument("--img", default="/tmp/cx29/lena.jpg")
    ap.add_argument("--teacher-ck", default="ck_tch.txt")
    ap.add_argument("--student-ck", default="ck.txt")
    a = ap.parse_args()

    tck, sck = load_ck(a.teacher_ck), load_ck(a.student_ck)
    aid = a.aid
    if not aid:
        t = C.TeacherSide(tck, TUID, quiet_hours=None, max_writes_per_hour=40, min_interval=0.5)
        aid = t.create_sign(COURSE, CLAZZ, other_id="0", if_photo="1", face="0",
                            time_long="1800000", start=True, title="拍照矩阵v2")
        if not aid:
            raise SystemExit("建活动失败")
    log("+", "activeId=%s  fid(候选)=%s" % (aid, a.fid))

    rt = requests.get(PANTOKEN, headers={"Cookie": sck, "User-Agent": UA_APP}, timeout=20).json()
    token = str(rt.get("_token") or rt.get("token") or "")
    log("+", "pan token ok=%s" % bool(token))

    u_plain = upload(sck, a.img, token, {})                        # 基线（puid only）
    u_fid = upload(sck, a.img, token, {"fid": a.fid})              # 带 fid
    u_full = upload(sck, a.img, token, {"fid": a.fid, "srcAsHd": "1"})  # 带 fid + srcAsHd
    oid_plain = str(u_plain.get("objectId") or "")
    oid_fid = str(u_fid.get("objectId") or "") or oid_plain
    oid_full = str(u_full.get("objectId") or "") or oid_plain
    log("+", "objectId: plain=%s fid=%s full=%s" % (oid_plain, oid_fid, oid_full))
    if not oid_plain:
        raise SystemExit("上传未拿到 objectId")

    dc = device_code(OAID)
    fid = a.fid
    cases = [
        ("W01", "fid=%s + GET + 无 photoResult（photo.ts 风格 + 真 fid）" % fid,
         params_for(aid, oid_plain, fid, "", UA_APP, False), "GET"),
        ("W02", "fid=%s + POST 表单 + photoResult 嵌套 + deviceCode（H5 原样）" % fid,
         params_for(aid, oid_plain, fid, dc, "", True), "POST"),
        ("W03", "fid=%s + GET + photoResult 嵌套 + deviceCode" % fid,
         params_for(aid, oid_plain, fid, dc, UA_APP, True), "GET"),
        ("W04", "fid=%s + POST 表单 + 无 photoResult" % fid,
         params_for(aid, oid_plain, fid, "", "", False), "POST"),
        ("W05", "fid=%s + POST + photoResult 非嵌套（files 为数组）" % fid,
         params_for(aid, oid_plain, fid, dc, "", True, pr_shape="flat"), "POST"),
        ("W06", "objectId 来自带 fid 的上传 + POST + photoResult 嵌套" % (),
         params_for(aid, oid_fid, fid, dc, "", True), "POST"),
        ("W07", "objectId 来自带 fid+srcAsHd 的上传 + POST + photoResult 嵌套",
         params_for(aid, oid_full, fid, dc, "", True), "POST"),
        ("W08", "fid=0 对照（H5 形状但 fid 默认）",
         params_for(aid, oid_plain, "0", dc, "", True), "POST"),
    ]
    results, winner = [], ""
    for tag, desc, params, method in cases:
        r = run_variant(tag, desc, sck, aid, params, method)
        results.append(r)
        if r["ok"]:
            winner = tag
            break

    try:
        with open("out/photo_matrix2.json", "w", encoding="utf-8") as f:
            json.dump({"aid": aid, "fid": fid, "oid_plain": oid_plain, "oid_fid": oid_fid,
                       "oid_full": oid_full, "device_code": dc, "results": results,
                       "winner": winner, "log": LOG}, f, ensure_ascii=False, indent=2)
    except Exception:
        pass
    log("*", "结果：%s" % ("成功 " + winner if winner else "全部失败（out/photo_matrix2.json）"))
    return 0 if winner else 2


if __name__ == "__main__":
    sys.exit(main())
