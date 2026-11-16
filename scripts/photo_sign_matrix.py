#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""拍照签到最后一跳矩阵实验（学习通 6.7.8 / com.chaoxing.mobile）

背景：
  学生端纯 HTTP 提交 ifPhoto=1 的活动时，服务端恒返回 photoAuthError_PCR007（HTTP 200）。
  已排除：objectId 形状 / validate / 图片内容 / resid 换 objectId。
  外部情报（scqwq/xxt-sign-in-help CLAUDE.md）指认「填入手机端 UA」修复 PCR007；
  H5 拍照页 out/stupages_puphoto_4000180998737.html 里 useragent= 参数是空串，
  真正被服务端看到的是 HTTP 头 User-Agent —— 我们此前用 python-requests 默认 UA 提交。

本脚本做矩阵：
  1) 教师侧新建 ifPhoto=1 的拍照签到（other_id=0, if_photo=1, face=0）取 activeId
  2) 三条上传通道拿 objectId（pan-yz token+_from / 裸 upload / 老 uploadfile）
  3) 逐变体提交（UA 头 / useragent 参数 / deviceCode / photoResult 嵌套形状 / fid / GET|POST），
     首个含 success 的变体即停。

deviceCode 还原（来自 out/smali/xp_b.smali + s9_b.smali + Ciphertext.smali）：
  deviceCode = Base64_NO_WRAP( AES/ECB/PKCS5Padding( uniqueId , I() 的 16 字节 key ) )
  uniqueId = OAID，空或 ^0{16,64}$ 时回退 an/b->d

用法：
  python3 photo_sign_matrix.py                 # 建活动 + 全矩阵（首个成功即停）
  python3 photo_sign_matrix.py --aid 4000xxx   # 复用已有拍照活动
  python3 photo_sign_matrix.py --only V01,V03  # 只跑指定变体
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
PANFILE = "https://pan-yz.chaoxing.com/upload/uploadfile"
PANTOKEN = "https://pan-yz.chaoxing.com/api/token/uservalid"

COURSE = "269282723"
CLAZZ = "159926750"
TUID = "401537379"
SID = "493228247"

# 设备指纹 AES key（out/smali/xp_b.smali 的 I() 常量）
DEVKEY = "QrCbNY@MuK1X8HGw"
OAID = "b1c2d3e4f5a60718"

UA_APP = ("Mozilla/5.0 (Linux; Android 10; SM-G975F Build/QP1A.190711.020; wv) "
          "AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/80.0.3987.99 "
          "Mobile Safari/537.36")
UA_DEX = ("Mozilla/5.0 (Linux; U; Android 10; SM-G975F Build/QP1A.190711.020) "
          "AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1")
UA_PY = None  # requests 默认

LOG = []


def log(tag, msg):
    line = "[%s] %s" % (tag, msg)
    print(line, flush=True)
    LOG.append(line)


def load_ck(v):
    """cookie 可以是文件路径，也可以是整串。返回可直接当 Cookie 头用的原始串。"""
    if v and os.path.exists(v):
        with open(v, "r", encoding="utf-8", errors="ignore") as f:
            return f.read().strip()
    return (v or "").strip()


def device_code(unique_id):
    """Base64_no_wrap(AES-ECB-PKCS5(unique_id))；唯一实现见 s9_b.smali。"""
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    key = DEVKEY.encode()
    if len(key) != 16:
        raise SystemExit("DEVKEY 不是 16 字节：%d" % len(key))
    raw = unique_id.encode()
    pad = 16 - (len(raw) % 16)
    buf = raw + bytes([pad]) * pad
    enc = Cipher(algorithms.AES(key), modes.ECB()).encryptor()
    ct = enc.update(buf) + enc.finalize()
    return base64.b64encode(ct).decode()


def _dump(name, data):
    try:
        os.makedirs("out", exist_ok=True)
        with open(os.path.join("out", name), "w", encoding="utf-8") as f:
            f.write(data if isinstance(data, str) else json.dumps(data, ensure_ascii=False, indent=2))
    except Exception:
        pass


# ---------------- 上传通道 ----------------
def pan_token(ck, ua=None):
    h = {"Cookie": ck}
    if ua:
        h["User-Agent"] = ua
    try:
        r = requests.get(PANTOKEN, headers=h, timeout=20)
        j = r.json()
    except Exception as e:
        log("!", "取 pan token 失败 -> %r" % (e,))
        return ""
    for k in ("_token", "token", "_Token"):
        if j.get(k):
            return str(j[k])
    log("!", "pan token 响应无 token 字段：%s" % json.dumps(j, ensure_ascii=False)[:200])
    return ""


def pan_upload_token(ck, ua, path, token):
    url = PANUPLOAD + "?_from=mobilelearn&_token=" + urllib.parse.quote(token)
    return _multipart(url, ck, ua, path, extra={"puid": SID})


def pan_upload_plain(ck, ua, path):
    return _multipart(PANUPLOAD, ck, ua, path, extra={"puid": SID})


def pan_upload_uploadfile(ck, ua, path):
    url = PANFILE + "?puid=" + SID + "&fid=0&type=1"
    return _multipart(url, ck, ua, path, extra={"puid": SID, "fid": "0"})


def _multipart(url, ck, ua, path, extra=None, filename="1.png"):
    h = {"Cookie": ck}
    if ua:
        h["User-Agent"] = ua
    with open(path, "rb") as f:
        data = f.read()
    files = {"file": (filename, data, "image/png")}
    form = dict(extra or {})
    try:
        r = requests.post(url, headers=h, files=files, data=form, timeout=60)
    except Exception as e:
        log("!", "上传失败 %s -> %r" % (url[:70], e))
        return {}
    body = (r.text or "").strip()
    try:
        j = r.json()
    except Exception:
        log("!", "上传非 JSON (HTTP %s)：%s" % (r.status_code, body[:200]))
        return {"_raw": body[:300]}
    j["_url"] = url
    log("U", "%s -> %s" % (url[:60], json.dumps(j, ensure_ascii=False)[:220]))
    return j


def pick_object_id(j):
    if not isinstance(j, dict):
        return "", ""
    oid = j.get("objectId") or j.get("objectid") or j.get("objectID") or ""
    fid = str(j.get("fid") or "")
    if not oid and isinstance(j.get("data"), dict):
        d = j["data"]
        oid = d.get("objectId") or d.get("objectid") or ""
        fid = fid or str(d.get("fid") or "")
    return str(oid), fid


# ---------------- 提交 ----------------
def submit(ck, ua, aid, params, method="GET", extra_headers=None):
    q = urllib.parse.urlencode(params)
    h = {"Cookie": ck}
    if ua:
        h["User-Agent"] = ua
    h.update(extra_headers or {})
    url = MOBILE + "pptSign/stuSignajax?" + q
    try:
        if method == "POST":
            r = requests.post(MOBILE + "pptSign/stuSignajax", headers=h, data=params, timeout=30)
        else:
            r = requests.get(url, headers=h, timeout=30)
    except Exception as e:
        return {"ok": False, "status": -1, "body": repr(e), "url": url}
    body = (r.text or "").strip()
    low = body.lower()
    ok = ("success" in low) or ("签到成功" in body)
    return {"ok": ok, "status": r.status_code, "body": body[:400], "url": url}


def photo_result(files_obj):
    """H5 真实形状：{"files":"<内层 JSON 字符串>"}"""
    return json.dumps({"files": json.dumps(files_obj, separators=(",", ":"))}, separators=(",", ":"))


def build_variants(aid, oid_a, oid_b, oid_c, fid_c, dc):
    """返回 [(vid, desc, params, method, ua, extra_headers)]"""
    def base(o, ua_param, fid, extra=None):
        p = [("activeId", str(aid)), ("courseId", COURSE), ("uid", SID), ("clientip", ""),
             ("useragent", ua_param), ("latitude", "-1"), ("longitude", "-1"),
             ("appType", "15"), ("fid", fid), ("objectId", o),
             ("name", "1.png"), ("validate", ""), ("deviceCode", "")]
        if extra:
            p += extra
        return p

    files_a = [{"name": "1.png", "objectid": oid_a, "type": "png"}]
    files_b = [{"name": "1.png", "objectid": oid_b, "type": "png"}]

    out = []
    out.append(("V01", "photo.ts 精确复刻：UA头=UA_APP / useragent参数=UA_APP / fid=0 / 无 photoResult / GET / 通道1",
                base(oid_a, UA_APP, "0"), "GET", UA_APP, None))
    out.append(("V02", "同 V01 但 objectId 来自通道2（裸 upload，无 _from/_token）",
                base(oid_b, UA_APP, "0"), "GET", UA_APP, None))
    out.append(("V03", "V01 + photoResult（files 为字符串的双层嵌套）",
                base(oid_a, UA_APP, "0", [("photoResult", photo_result(files_a))]), "GET", UA_APP, None))
    out.append(("V04", "V01 + deviceCode（AES-ECB(OAID) 真值）",
                base(oid_a, UA_APP, "0", [("deviceCode", dc)]), "GET", UA_APP, None))
    out.append(("V05", "V03 + V04 合并",
                base(oid_a, UA_APP, "0", [("photoResult", photo_result(files_a)), ("deviceCode", dc)]),
                "GET", UA_APP, None))
    out.append(("V06", "UA 头换成 dex 里 WebView 模板 UA，其余同 V01",
                base(oid_a, UA_DEX, "0"), "GET", UA_DEX, None))
    out.append(("V07", "同 V05 但 UA 头 = dex 模板 UA",
                base(oid_a, UA_DEX, "0", [("photoResult", photo_result(files_a)), ("deviceCode", dc)]),
                "GET", UA_DEX, None))
    out.append(("V08", "V05 改 POST（form body）",
                base(oid_a, UA_APP, "0", [("photoResult", photo_result(files_a)), ("deviceCode", dc)]),
                "POST", UA_APP, None))
    out.append(("V09", "useragent 参数留空、只靠 UA 头（当前项目旧行为）+ photoResult",
                base(oid_a, "", "0", [("photoResult", photo_result(files_a))]), "GET", UA_APP, None))
    out.append(("V10", "objectId 来自老 uploadfile 通道（resid 系）；fid 用响应里的真 fid",
                base(oid_c, UA_APP, fid_c or "0"), "GET", UA_APP, None))
    out.append(("V11", "V05 + X-Requested-With + Accept: application/json 头",
                base(oid_a, UA_APP, "0", [("photoResult", photo_result(files_a)), ("deviceCode", dc)]),
                "GET", UA_APP, {"X-Requested-With": "XMLHttpRequest", "Accept": "application/json, text/plain, */*"}))
    out.append(("V12", "V05 + Referer=拍照签到页 + Origin",
                base(oid_a, UA_APP, "0", [("photoResult", photo_result(files_a)), ("deviceCode", dc)]),
                "GET", UA_APP, {"Referer": MOBILE + "newsign/preSign?activePrimaryId=" + str(aid) + "&appType=15"}))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--aid", default="", help="复用已有拍照活动 id（不新建）")
    ap.add_argument("--only", default="", help="只跑指定变体，如 V01,V05")
    ap.add_argument("--img", default="/tmp/cx29/lena.jpg")
    ap.add_argument("--teacher-ck", default="ck_tch.txt")
    ap.add_argument("--student-ck", default="ck.txt")
    ap.add_argument("--time-long", default="1800000")
    a = ap.parse_args()

    tck = load_ck(a.teacher_ck)
    sck = load_ck(a.student_ck)
    if not tck or not sck:
        raise SystemExit("缺 cookie 文件")

    # 1) 活动
    aid = a.aid
    if not aid:
        t = C.TeacherSide(tck, TUID, quiet_hours=None, max_writes_per_hour=40, min_interval=0.5)
        aid = t.create_sign(COURSE, CLAZZ, other_id="0", if_photo="1", face="0",
                            time_long=a.time_long, start=True, title="拍照签到矩阵")
        if not aid:
            raise SystemExit("建拍照活动失败")
    log("+", "拍照活动 activeId=%s" % aid)

    # 2) 上传
    tk = pan_token(sck, UA_APP)
    log("+", "pan token = %s" % (tk[:12] + ".." if tk else "(空)"))
    j1 = pan_upload_token(sck, UA_APP, a.img, tk) if tk else {}
    j2 = pan_upload_plain(sck, UA_APP, a.img)
    j3 = pan_upload_uploadfile(sck, UA_APP, a.img)
    oid_a, _ = pick_object_id(j1)
    oid_b, _ = pick_object_id(j2)
    oid_c, fid_c = pick_object_id(j3)
    log("+", "objectId 通道1=%s 通道2=%s 通道3=%s fid3=%s" % (oid_a or "-", oid_b or "-", oid_c or "-", fid_c or "-"))
    if not (oid_a or oid_b or oid_c):
        raise SystemExit("三条上传通道都没拿到 objectId")

    dc = device_code(OAID)
    log("+", "deviceCode(OAID=%s) = %s" % (OAID, dc))

    # 3) 矩阵
    only = set(x.strip().upper() for x in a.only.split(",") if x.strip())
    variants = build_variants(aid, oid_a or oid_b, oid_b or oid_a, oid_c, fid_c, dc)
    results = []
    winner = None
    for vid, desc, params, method, ua, eh in variants:
        if only and vid not in only:
            continue
        res = submit(sck, ua, aid, params, method, eh)
        results.append({"vid": vid, "desc": desc, "method": method, "ua": (ua or "python-default")[:40],
                        "ok": res["ok"], "http": res["status"], "body": res["body"]})
        log("=", "%s %s -> HTTP %s %s" % (vid, method, res["status"], res["body"][:160]))
        time.sleep(1.2)
        if res["ok"]:
            winner = vid
            break

    _dump("photo_matrix.json", {"aid": aid, "oid_a": oid_a, "oid_b": oid_b, "oid_c": oid_c,
                                "fid_c": fid_c, "device_code": dc, "results": results,
                                "winner": winner, "log": LOG})
    log("*", "结果：%s" % ("成功变体 " + winner if winner else "全部失败（见 out/photo_matrix.json）"))
    return 0 if winner else 2


if __name__ == "__main__":
    sys.exit(main())
