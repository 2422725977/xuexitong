#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""拍照签到矩阵 v3：补上真实学生端缺的那一步 —— preSign（预签到）

来源（oines/xxt-sign-android, net/CxApi.kt:249-286 原注释）：
  「真实学生端是在 newsign/preSign 页面完成的：页面加载先带一遍参数请求，
    服务端把「本次签到上下文」记在这个会话上，之后提交才认。」

提交参数（CxApi.kt:334-358）与我们的差异：
  - **没有 useragent 参数**；有 fid=schoolId、name=realName、signCode、deviceCode
  - POST 表单 + query 都带同一份；headers: X-Requested-With + Referer=/newsign/preSign?activePrimaryId=0
  - UA 模板（Http.kt）：... Mobile Safari/537.36 (schild:%SCHILD%) (device:%MODEL%) Language/zh_CN
    com.ssreader.ChaoXingStudy/ChaoXingStudy_3_6_2_android_phone_20230101
"""
import argparse
import base64
import json
import os
import re
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
COURSE, CLAZZ, SID, TUID = "269282723", "159926750", "493228247", "401537379"
DEVKEY = "QrCbNY@MuK1X8HGw"
SCHILD = "b1c2d3e4f5a60718"
MODEL = "SM-G975F"


def ua(model=MODEL, schild=SCHILD):
    return ("Mozilla/5.0 (Linux; Android 13; %s Build/TQ3A.230901.001) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Version/4.0 Chrome/120.0.0.0 Mobile Safari/537.36 "
            "(schild:%s) (device:%s) Language/zh_CN "
            "com.ssreader.ChaoXingStudy/ChaoXingStudy_3_6_2_android_phone_20230101"
            % (model, schild, model))


LOG = []


def log(t, m):
    s = "[%s] %s" % (t, m)
    print(s, flush=True)
    LOG.append(s)


def ck_raw(p):
    with open(p, "r", encoding="utf-8", errors="ignore") as f:
        return f.read().strip()


def ck_dict(p):
    d = {}
    for part in ck_raw(p).split(";"):
        part = part.strip()
        if "=" in part:
            k, v = part.split("=", 1)
            d[k.strip()] = v.strip()
    return d


def aes_device_code(unique_id, ) :
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    key = DEVKEY.encode()
    raw = unique_id.encode()
    pad = 16 - (len(raw) % 16)
    enc = Cipher(algorithms.AES(key), modes.ECB()).encryptor()
    return base64.b64encode(enc.update(raw + bytes([pad]) * pad) + enc.finalize()).decode()


def pre_sign(ck, aid, app_type=15, dump="out/preSign_photo_v3.html"):
    h = {"Cookie": ck, "User-Agent": ua()}
    url = (MOBILE + "newsign/preSign?courseId=%s&classId=%s&activePrimaryId=%s"
           "&general=1&sys=1&ls=1&appType=%s&uid=%s&isTeacherViewOpen=0"
           % (COURSE, CLAZZ, aid, app_type, SID))
    r = requests.get(url, headers=h, timeout=30)
    body = r.text or ""
    try:
        open(dump, "w", encoding="utf-8").write(body)
    except Exception:
        pass
    m = re.search(r'id="statuscontent"[^>]*>(.*?)<', body, re.S)
    status = re.sub(r"\s", "", re.sub(r"<[^>]+>", "", m.group(1))) if m else ""
    return {"http": r.status_code, "len": len(body), "status": status, "url": url}


def upload(ck, path, token):
    url = PANUPLOAD + "?_from=mobilelearn&_token=" + urllib.parse.quote(token)
    with open(path, "rb") as f:
        data = f.read()
    form = {"puid": SID, "_token": token}
    r = requests.post(url, headers={"Cookie": ck, "User-Agent": ua()},
                      files={"file": ("1.png", data, "image/png")}, data=form, timeout=60)
    j = r.json()
    log("U", "upload -> %s" % json.dumps(j, ensure_ascii=False)[:180])
    return str(j.get("objectId") or "")


def submit(ck, aid, fid, name, dc, oid, pr_mode, use_query=True, method="POST", extra_headers=None):
    params = {
        "activeId": str(aid), "courseId": COURSE, "uid": SID, "clientip": "",
        "latitude": "-1", "longitude": "-1", "appType": "15", "fid": fid,
        "name": name, "signCode": "", "deviceCode": dc, "location": "",
    }
    if oid:
        params["objectId"] = oid
    if pr_mode == "nested":
        inner = [{"name": "1.png", "objectid": oid, "type": "png"}]
        params["photoResult"] = json.dumps({"files": json.dumps(inner, separators=(",", ":"))},
                                           separators=(",", ":"))
    elif pr_mode == "flat":
        params["photoResult"] = json.dumps({"files": [{"name": "1.png", "objectid": oid, "type": "png"}]},
                                           separators=(",", ":"))
    q = urllib.parse.urlencode(params)
    h = {"Cookie": ck, "User-Agent": ua(),
         "X-Requested-With": "XMLHttpRequest",
         "Referer": MOBILE + "newsign/preSign?activePrimaryId=0"}
    h.update(extra_headers or {})
    url = MOBILE + "pptSign/stuSignajax"
    if use_query:
        url += "?" + q
    try:
        if method == "POST":
            r = requests.post(url, headers=h, data=params, timeout=30)
        else:
            r = requests.get(url, headers=h, timeout=30)
    except Exception as e:
        return {"ok": False, "http": -1, "body": repr(e)}
    body = (r.text or "").strip()
    return {"ok": ("success" in body.lower()) or ("签到成功" in body), "http": r.status_code, "body": body[:300]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--aid", default="")
    ap.add_argument("--img", default="/tmp/cx29/lena.jpg")
    ap.add_argument("--time-long", default="1800000")
    a = ap.parse_args()
    tck, sck = ck_raw("ck_tch.txt"), ck_raw("ck.txt")
    cd = ck_dict("ck.txt")
    log("+", "cookie 关键项：fid=%r spaceFid=%r uname=%r vc3=%s" %
        (cd.get("fid"), cd.get("spaceFid"), cd.get("uname"), (cd.get("vc3") or "")[:12]))

    aid = a.aid
    if not aid:
        t = C.TeacherSide(tck, TUID, quiet_hours=None, max_writes_per_hour=40, min_interval=0.5)
        aid = t.create_sign(COURSE, CLAZZ, other_id="0", if_photo="1", face="0",
                            time_long=a.time_long, start=True, title="拍照矩阵v3")
        if not aid:
            raise SystemExit("建活动失败")
    log("+", "activeId=%s" % aid)

    r = requests.get(PANTOKEN, headers={"Cookie": sck, "User-Agent": ua()}, timeout=20).json()
    token = str(r.get("_token") or "")
    oid = upload(sck, a.img, token) if token else ""
    log("+", "objectId=%s" % (oid or "(空)"))
    if not oid:
        raise SystemExit("上传失败")

    dc_aes = aes_device_code(SCHILD)
    pre = pre_sign(sck, aid)
    log("+", "preSign -> HTTP %s len=%d statuscontent=%r" % (pre["http"], pre["len"], pre["status"][:120]))

    fid_cookie = cd.get("fid") or cd.get("spaceFid") or "0"
    cases = [
        ("X01", "preSign + POST(oines 参数) + fid=%s + name='' + deviceCode=schild + photoResult 嵌套" % fid_cookie,
         fid_cookie, "", SCHILD, "nested", True, "POST"),
        ("X02", "同 X01 但 deviceCode=AES(OAID)", fid_cookie, "", dc_aes, "nested", True, "POST"),
        ("X03", "同 X01 但 fid=0", "0", "", SCHILD, "nested", True, "POST"),
        ("X04", "同 X01 但无 photoResult", fid_cookie, "", SCHILD, None, True, "POST"),
        ("X05", "同 X01 但 name=1.png（旧行为）", fid_cookie, "1.png", SCHILD, "nested", True, "POST"),
        ("X06", "同 X01 但 GET（query only）", fid_cookie, "", SCHILD, "nested", True, "GET"),
        ("X07", "同 X01 但 photoResult 非嵌套", fid_cookie, "", SCHILD, "flat", True, "POST"),
    ]
    results, winner = [], ""
    for tag, desc, fid, name, dc, pr, uq, method in cases:
        # 每个变体前重新 preSign（服务端上下文可能与 appType/时间相关）
        pre_sign(sck, aid, dump="out/preSign_photo_v3.html")
        res = submit(sck, aid, fid, name, dc, oid, pr, uq, method)
        log("=", "%s %s -> HTTP %s %s" % (tag, method, res["http"], res["body"][:150]))
        results.append({"tag": tag, "desc": desc, "ok": res["ok"], "http": res["http"], "body": res["body"]})
        time.sleep(1.2)
        if res["ok"]:
            winner = tag
            break
    try:
        with open("out/photo_matrix3.json", "w", encoding="utf-8") as f:
            json.dump({"aid": aid, "oid": oid, "pre": pre, "results": results, "winner": winner},
                      f, ensure_ascii=False, indent=2)
    except Exception:
        pass
    log("*", "结果：%s" % ("成功 " + winner if winner else "全部失败"))
    return 0 if winner else 2


if __name__ == "__main__":
    sys.exit(main())
