# -*- coding: utf-8 -*-
"""拍照签到矩阵 v7 —— 核心新发现：App 桥给 H5 的 CLIENT_CHOOSE_IMAGE_RESULT 外层对象是
webapp_d;->H(List<CloudDiskFile1>, int camera, a) 构建的：
    {"camera": <int>, "files": "<Gson(List<CloudDiskFile1>) 字符串>", "result": 1}
H5 的 PHOTO_RESULT = JSON.stringify(整个外层对象) -> photoResult 里除了 files 还有 camera 与 result。
此前我们只发了 {"files":"[...]"}，缺 camera/result。本矩阵专测该形状。
"""
import json, os, sys, time, random, hashlib
from urllib.parse import quote
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
TUID = "[教师PUID]"
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
    return r.json().get("msg", {})


def pre_sign(s, aid, ext, uid):
    url = (MOBILE + "/newsign/preSign?courseId=%s&classId=%s&activePrimaryId=%s"
           "&general=1&sys=1&ls=1&appType=15&uid=%s&isTeacherViewOpen=0" % (COURSE, CLAZZ, aid, uid))
    return s.post(url, data={"ext": ext}, headers={"Content-Type": "application/x-www-form-urlencoded"})


def analysis(s, aid):
    import re
    out = {}
    r = s.get(MOBILE + "/pptSign/analysis?vs=1&DB_STRATEGY=RANDOM&aid=%s" % aid, timeout=20)
    m = re.search(r"code='\+'([a-f0-9]+)'", r.text)
    out["code"] = m.group(1) if m else None
    if out["code"]:
        r2 = s.get(MOBILE + "/pptSign/analysis2?DB_STRATEGY=RANDOM&code=%s" % out["code"], timeout=20)
        out["a2"] = r2.text[:60]
    return out


def uptoken(s):
    return s.get(PANTOKEN, timeout=20).json().get("_token")


def upload(s, puid, path, fname, extra_qs=""):
    tk = uptoken(s)
    url = PANUPLOAD + "?_from=mobilelearn&_token=" + str(tk) + extra_qs
    with open(path, "rb") as f:
        files = {"file": (fname, f.read(), "image/jpeg")}
        r = s.post(url, files=files, data={"puid": str(puid)}, timeout=60)
    try:
        j = r.json()
    except Exception:
        j = {"raw": r.text[:300]}
    return tk, j


def randomize(path_in, path_out):
    from PIL import Image
    im = Image.open(path_in)
    w, h = im.size
    f = 0.90 + random.random() * 0.09
    cx, cy = int(w * (1 - f) / 2), int(h * (1 - f) / 2)
    im = im.crop((cx, cy, w - cx, h - cy))
    q = random.randint(85, 95)
    im.save(path_out, "JPEG", quality=q)
    return im.size


def main():
    sck, scookie = load_ck("ck.txt")
    tck, _ = load_ck("ck_tch.txt")
    msg = userinfo(sck)
    info = {k: msg.get(k) for k in ("uid", "puid", "fid", "name", "uname")}
    print("[userinfo]", json.dumps(info, ensure_ascii=False))
    puid = str(info["puid"] or scookie.get("_uid"))
    real_name = info["name"] or ""
    fid = str(info["fid"] if info["fid"] is not None else 0)

    t = C.TeacherSide(tck, TUID, quiet_hours=None, max_writes_per_hour=60, min_interval=0.3, per_day=2000)
    aid = t.create_sign(COURSE, CLAZZ, other_id="0", if_photo="1", face="0", time_long="1800000",
                        title="拍照矩阵v7")
    print("[create] aid =", aid)
    if not aid:
        return

    ext = ""
    r = requests.get(MOBILE + "/v2/apis/active/student/activelist?fid=0&showNotStartedActive=0&courseId=%s&classId=%s" % (COURSE, CLAZZ),
                     headers={"Cookie": sck, "User-Agent": UA_APP}, timeout=20)
    ext = (r.json().get("data") or {}).get("ext", {}).get("_from_", "")
    print("[ext]", ext)

    s = requests.Session()
    s.headers.update({"Cookie": sck, "User-Agent": UA_APP})
    print("[preSign]", pre_sign(s, aid, ext, puid).status_code)
    print("[analysis]", json.dumps(analysis(s, aid), ensure_ascii=False))

    img = "out/photo_v7_%d.jpg" % int(time.time())
    wh = randomize("/tmp/cx29/lena.jpg", img)
    fname = os.path.basename(img)
    tk, up = upload(s, puid, img, fname)
    print("[upload plain]", json.dumps(up, ensure_ascii=False)[:300])
    oid = up.get("objectId")
    resid = up.get("resid")
    if not oid:
        return
    tk2, up2 = upload(s, puid, img, fname, extra_qs="&srcAsHd=1")
    print("[upload srcAsHd]", json.dumps(up2, ensure_ascii=False)[:300])
    oid2 = up2.get("objectId") or oid

    size = os.path.getsize(img)
    inner_basic = {"name": fname, "objectid": oid, "type": "jpg"}
    inner_full = {"name": fname, "duration": 0, "width": wh[0], "height": wh[1], "thumbnail": "",
                  "objectid": oid, "resid": resid, "camare": "5", "camera": "5", "type": "jpg",
                  "datasize": size, "isMirror": 0, "result": 1}
    inner_basic2 = {"name": fname, "objectid": oid2, "type": "jpg"}

    def outer(camera, inner, as_str=True, oid_override=True):
        return {"camera": camera,
                "files": json.dumps([inner], ensure_ascii=False) if as_str else [inner],
                "result": 1}

    base_pairs = [("activeId", aid), ("courseId", COURSE), ("uid", puid), ("clientip", ""),
                  ("useragent", ""), ("latitude", "-1"), ("longitude", "-1"), ("appType", "15"),
                  ("fid", fid), ("objectId", oid)]

    def run(tag, pr, method="GET", name=fname, objid=oid, pairs_extra=None):
        pairs = list(base_pairs)
        pairs = [(k, (objid if k == "objectId" else v)) for k, v in pairs]
        pairs += [("name", name)]
        if pairs_extra:
            pairs += pairs_extra
        qs = "&".join("%s=%s" % (k, quote(str(v), safe="")) for k, v in pairs if v is not None)
        data = dict(pairs)
        if pr is not None:
            data["photoResult"] = pr
            qs += "&photoResult=" + quote(pr, safe="")
        hdr = {"Referer": MOBILE + "/newsign/preSign?activePrimaryId=" + aid,
               "X-Requested-With": "XMLHttpRequest"}
        url = MOBILE + "/pptSign/stuSignajax?" + qs
        try:
            if method == "GET":
                rr = s.get(url, headers=hdr, timeout=30)
            else:
                rr = s.post(MOBILE + "/pptSign/stuSignajax", data=data, headers=hdr, timeout=30)
            body = rr.text.strip()
            print("[%s] %s %s len=%d :: %s" % (tag, method, rr.status_code, len(rr.text), body[:200]))
            return body
        except Exception as e:
            print("[%s] ERR %s" % (tag, e))
            return "EXC"

    variants = [
        ("V01_outer_cam5_basic", json.dumps(outer(5, inner_basic), ensure_ascii=False), "GET", fname, oid),
        ("V02_outer_cam5_str", json.dumps(outer("5", inner_basic), ensure_ascii=False), "GET", fname, oid),
        ("V03_outer_cam5_full", json.dumps(outer(5, inner_full), ensure_ascii=False), "GET", fname, oid),
        ("V04_outer_cam5_basic_POST", json.dumps(outer(5, inner_basic), ensure_ascii=False), "POST", fname, oid),
        ("V05_nocam_justfiles", json.dumps({"files": json.dumps([inner_basic], ensure_ascii=False), "result": 1}, ensure_ascii=False), "GET", fname, oid),
        ("V06_outer_cam0_basic", json.dumps(outer(0, inner_basic), ensure_ascii=False), "GET", fname, oid),
        ("V07_outer_cam5_array", json.dumps(outer(5, inner_basic, as_str=False), ensure_ascii=False), "GET", fname, oid),
        ("V08_outer_cam5_nameRealName", json.dumps(outer(5, inner_basic), ensure_ascii=False), "GET", real_name, oid),
        ("V09_outer_cam5_srcAsHd", json.dumps(outer(5, inner_basic2), ensure_ascii=False), "GET", fname, oid2),
        ("V10_no_photoResult_control", None, "GET", fname, oid),
        ("V11_outer_cam5_full_POST", json.dumps(outer(5, inner_full), ensure_ascii=False), "POST", fname, oid),
    ]

    results = {}
    for tag, pr, meth, nm, oi in variants:
        body = run(tag, pr, meth, nm, oi)
        results[tag] = body[:300]
        if body.strip().lower() in ("success", "success2"):
            print("*** 命中成功：", tag)
            break
    with open("out/photo_matrix7.json", "w", encoding="utf-8") as f:
        json.dump({"aid": aid, "oid": oid, "oid2": oid2, "resid": resid, "img": img,
                   "userinfo": info, "ext": ext, "upload": up, "upload2": up2,
                   "results": results}, f, ensure_ascii=False, indent=1)
    print("[saved] out/photo_matrix7.json")


if __name__ == "__main__":
    main()
