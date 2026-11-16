# -*- coding: utf-8 -*-
"""拍照签到矩阵 v6 —— 关键修正：name 用真名（userLogin4Uname.do 在缺 App UA 时返回 403，
此前所有变体的 name 都是空串）。同时补：preSign(ext) -> analysis -> 上传 -> 提交 的顺序、
cookie fid、enc2/ifTiJiao/vpProbability 变体、GET 与 POST 表单两种提交方式。
"""
import json, os, sys, time, random, io, hashlib
from urllib.parse import quote, urlencode
import requests

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cx_pipeline as C

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

UA_APP = ('Mozilla/5.0 (Linux; Android 13; SM-G975F Build/TQ3A.230901.001) '
          'AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/120.0.0.0 '
          'Mobile Safari/537.36 (schild:b1c2d3e4f5a60718) (device:SM-G975F) '
          'Language/zh_CN com.ssreader.ChaoXingStudy/ChaoxingStudy_3_6_2_android_phone_20230101')

COURSE = "269282723"
CLAZZ = "159926750"
TUID = "401537379"

MOBILE = "https://mobilelearn.chaoxing.com"
PANUPLOAD = "https://pan-yz.chaoxing.com/upload"
PANTOKEN = "https://pan-yz.chaoxing.com/api/token/uservalid"
USERINFO = "https://sso.chaoxing.com/apis/login/userLogin4Uname.do"


def load_ck(path):
    ck = open(path, encoding="utf-8").read().strip()
    d = {}
    for part in ck.split(";"):
        if "=" in part:
            k, v = part.split("=", 1)
            d[k.strip()] = v.strip()
    return ck, d


def userinfo(ck):
    r = requests.get(USERINFO, headers={"Cookie": ck, "User-Agent": UA_APP}, timeout=20)
    j = r.json().get("msg", {})
    return {"uid": j.get("uid"), "puid": j.get("puid"), "fid": j.get("fid"),
            "name": j.get("name"), "uname": j.get("uname"),
            "unitConfigInfos": j.get("unitConfigInfos")}


def pre_sign(s, aid, ext="", uid=""):
    url = (MOBILE + "/newsign/preSign?courseId=%s&classId=%s&activePrimaryId=%s"
           "&general=1&sys=1&ls=1&appType=15&uid=%s&isTeacherViewOpen=0" % (COURSE, CLAZZ, aid, uid))
    r = s.post(url, data={"ext": ext}, headers={"Content-Type": "application/x-www-form-urlencoded"})
    return r


def analysis(s, aid):
    out = {}
    try:
        r = s.get(MOBILE + "/pptSign/analysis?vs=1&DB_STRATEGY=RANDOM&aid=%s" % aid, timeout=20)
        import re
        m = re.search(r"code='\+'([a-f0-9]+)'", r.text)
        out["code"] = m.group(1) if m else None
        if out["code"]:
            r2 = s.get(MOBILE + "/pptSign/analysis2?DB_STRATEGY=RANDOM&code=%s" % out["code"], timeout=20)
            out["a2"] = r2.text[:80]
    except Exception as e:
        out["err"] = str(e)
    return out


def uptoken(s):
    r = s.get(PANTOKEN, timeout=20)
    return r.json().get("_token")


def randomize(path_in, path_out):
    try:
        from PIL import Image
        im = Image.open(path_in)
        w, h = im.size
        f = 0.90 + random.random() * 0.09
        cx, cy = int(w * (1 - f) / 2), int(h * (1 - f) / 2)
        im = im.crop((cx, cy, w - cx, h - cy))
        q = random.randint(85, 95)
        im.save(path_out, "JPEG", quality=q)
        return path_out, q, im.size
    except Exception as e:
        return path_in, None, str(e)


def upload(s, puid, path, fname):
    tk = uptoken(s)
    url = PANUPLOAD + "?_from=mobilelearn&_token=" + str(tk)
    with open(path, "rb") as f:
        files = {"file": (fname, f.read(), "image/jpeg")}
        r = s.post(url, files=files, data={"puid": str(puid)}, timeout=60)
    try:
        j = r.json()
    except Exception:
        j = {"raw": r.text[:200]}
    return tk, j


def main():
    sck, scookie = load_ck("ck.txt")
    tck, _ = load_ck("ck_tch.txt")
    info = userinfo(sck)
    print("[userinfo]", json.dumps(info, ensure_ascii=False))
    puid = str(info["puid"] or scookie.get("_uid"))
    real_name = info["name"] or ""
    fid = str(info["fid"] if info["fid"] is not None else 0)

    t = C.TeacherSide(tck, TUID, quiet_hours=None, max_writes_per_hour=40, min_interval=0.5)
    aid = t.create_sign(COURSE, CLAZZ, other_id="0", if_photo="1", face="0", time_long="1800000",
                        title="拍照矩阵v6")
    print("[create] aid =", aid)
    if not aid:
        print("!! 创建失败"); return

    # 活动 ext（来自学生活动列表）
    ext = ""
    try:
        r = requests.get(MOBILE + "/v2/apis/active/student/activelist?fid=0&showNotStartedActive=0&courseId=%s&classId=%s" % (COURSE, CLAZZ),
                         headers={"Cookie": sck, "User-Agent": UA_APP}, timeout=20)
        ext = (r.json().get("data") or {}).get("ext", {}).get("_from_", "")
    except Exception as e:
        print("[ext] err", e)
    print("[ext]", ext)

    s = requests.Session()
    s.headers.update({"Cookie": sck, "User-Agent": UA_APP})

    print("[preSign]", pre_sign(s, aid, ext, puid).status_code)
    print("[analysis]", json.dumps(analysis(s, aid), ensure_ascii=False))

    img, q, size = randomize("/tmp/cx29/lena.jpg", "out/photo_v6_%d.jpg" % int(time.time()))
    print("[img]", img, q, size)
    tk, up = upload(s, puid, img, "%s.jpg" % hashlib.md5(str(time.time()).encode()).hexdigest()[:12])
    print("[upload]", json.dumps(up, ensure_ascii=False)[:300])
    oid = up.get("objectId")
    if not oid:
        print("!! 上传失败"); return

    fname = os.path.basename(img)
    pr_full = json.dumps({"files": json.dumps([{"name": fname, "objectid": oid, "type": "jpg"}])},
                         ensure_ascii=False)
    pr_flat = json.dumps({"files": [{"name": fname, "objectid": oid, "type": "jpg"}]}, ensure_ascii=False)

    base_pairs = [("activeId", aid), ("courseId", COURSE), ("uid", puid), ("clientip", ""),
                  ("useragent", ""), ("latitude", "-1"), ("longitude", "-1"), ("appType", "15"),
                  ("fid", fid), ("objectId", oid), ("deviceCode", "")]

    def run(tag, pairs, photo_result=None, method="GET", extra_headers=None, cookie_extra=None):
        qs = "&".join("%s=%s" % (k, quote(str(v), safe="")) for k, v in pairs if v is not None)
        data = dict(pairs)
        if photo_result is not None:
            data["photoResult"] = photo_result
            qs += "&photoResult=" + quote(photo_result, safe="")
        hdr = {"Referer": MOBILE + "/newsign/preSign?activePrimaryId=" + aid,
               "X-Requested-With": "XMLHttpRequest"}
        if extra_headers:
            hdr.update(extra_headers)
        if cookie_extra:
            hdr["Cookie"] = scookie and (sck + "; " + cookie_extra)
        url = MOBILE + "/pptSign/stuSignajax?" + qs
        try:
            if method == "GET":
                r = s.get(url, headers=hdr, timeout=30)
            else:
                r = s.post(MOBILE + "/pptSign/stuSignajax", data=data, headers=hdr, timeout=30)
            body = r.text.strip()
            print("[%s] %s %s len=%d :: %s" % (tag, method, r.status_code, len(r.text), body[:200]))
            return body
        except Exception as e:
            print("[%s] ERR %s" % (tag, e))
            return "EXC"

    variants = [
        ("A_name_real_get", [("name", real_name)] + base_pairs, None, "GET", None, None),
        ("B_name_real_prfull", [("name", real_name)] + base_pairs, pr_full, "GET", None, None),
        ("C_name_real_prfull_post", [("name", real_name)] + base_pairs, pr_full, "POST", None, None),
        ("D_name_real_prflat", [("name", real_name)] + base_pairs, pr_flat, "GET", None, None),
        ("E_name_file", [("name", fname)] + base_pairs, pr_full, "GET", None, None),
        ("F_name_real_ifTiJiao", [("name", real_name), ("ifTiJiao", "1"), ("vpProbability", "-1"), ("vpStrategy", "")] + base_pairs, pr_full, "GET", None, None),
        ("G_name_real_cookieFid", [("name", real_name)] + base_pairs, pr_full, "GET", None, "fid=" + fid),
        ("H_name_empty", [("name", "")] + base_pairs, pr_full, "GET", None, None),
        ("I_name_real_noobjid", [("name", real_name), ("objectId", ("", None)[0])] + base_pairs, pr_full, "GET", None, None),
    ]
    results = {}
    for tag, pairs, pr, meth, eh, ce in variants:
        if tag.startswith("I_"):
            pairs = [(k, v) for k, v in pairs if k != "objectId"]
        body = run(tag, pairs, pr, meth, eh, ce)
        results[tag] = body[:300]
        if body.strip().lower() in ("success", "success2"):
            print("*** 成功命中：", tag)
            break
    with open("out/photo_matrix6.json", "w", encoding="utf-8") as f:
        json.dump({"aid": aid, "oid": oid, "img": img, "userinfo": info, "ext": ext,
                   "token": tk, "upload": up, "results": results}, f, ensure_ascii=False, indent=1)
    print("[saved] out/photo_matrix6.json")


if __name__ == "__main__":
    main()
