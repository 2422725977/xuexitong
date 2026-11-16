# -*- coding: utf-8 -*-
"""拍照签到矩阵 v8 —— 直接照抄外部可用实现的三条硬配方：
  1) 2020 抓包版最终请求：GET /pptSign/stuSignajax?activeId&uid&clientip&useragent&latitude=-1&longitude=-1&appType=15&fid=<真值>&objectId&name=真实姓名
     —— 没有 courseId、没有 photoResult、没有 deviceCode
  2) cxsign(2026-11 校准) base_params：带 courseId/classId，GET，成功字面量 success
  3) Ru41(Rust)：photoResult = 整个上传响应 JSON 字符串
另外测：fid 取真值（学生 fid / cookie spaceFid / 教师 fid）、objectId 取上传响应 data.encryptedId、
上传时带 fid 表单字段、换上传主机 pan-yz.cldisk.com。
"""
import json, os, sys, time, random, re
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
PANALT = "https://pan-yz.cldisk.com/upload"
PANTOKEN = "https://pan-yz.chaoxing.com/api/token/uservalid"
USERINFO = "https://sso.chaoxing.com/apis/login/userLogin4Uname.do"
BACKCLAZZ = "https://mooc1-api.chaoxing.com/mycourse/backclazzdata"


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
    try:
        return r.json().get("msg", {}) or {}
    except Exception:
        return {"_http": r.status_code, "_body": r.text[:200]}


def pre_sign(s, aid, ext, uid):
    url = (MOBILE + "/newsign/preSign?courseId=%s&classId=%s&activePrimaryId=%s"
           "&general=1&sys=1&ls=1&appType=15&uid=%s&isTeacherViewOpen=0" % (COURSE, CLAZZ, aid, uid))
    return s.post(url, data={"ext": ext}, headers={"Content-Type": "application/x-www-form-urlencoded"})


def analysis(s, aid):
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


def upload(s, puid, path, fname, extra_qs="", fid=None, host=PANUPLOAD):
    tk = uptoken(s)
    url = host + "?_from=mobilelearn&_token=" + str(tk) + extra_qs
    with open(path, "rb") as f:
        files = {"file": (fname, f.read(), "image/jpeg")}
        data = {"puid": str(puid)}
        if fid is not None:
            data["fid"] = str(fid)
        r = s.post(url, files=files, data=data, timeout=60)
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
    tck, tcookie = load_ck("ck_tch.txt")
    smsg = userinfo(sck)
    tmsg = userinfo(tck)
    print("[student userinfo keys]", sorted(smsg.keys()))
    print("[student]", json.dumps({k: smsg.get(k) for k in ("uid", "puid", "fid", "name", "uname", "ppfid", "inputfid", "schoolname")}, ensure_ascii=False))
    print("[student unitConfigInfos]", json.dumps(smsg.get("unitConfigInfos"), ensure_ascii=False)[:400])
    print("[teacher]", json.dumps({k: tmsg.get(k) for k in ("uid", "puid", "fid", "name", "uname", "ppfid", "inputfid", "schoolname")}, ensure_ascii=False))
    print("[teacher unitConfigInfos]", json.dumps(tmsg.get("unitConfigInfos"), ensure_ascii=False)[:400])
    print("[cookie spaceFid] student=%s teacher=%s" % (scookie.get("spaceFid"), tcookie.get("spaceFid")))

    # 班级所属 unit（backclazzdata）
    class_fid = None
    try:
        rb = requests.get(BACKCLAZZ + "?view=json&rss=1", headers={"Cookie": sck, "User-Agent": UA_APP}, timeout=25)
        jb = rb.json()
        for c in (jb.get("channelList") or []):
            cj = json.dumps(c, ensure_ascii=False)
            if COURSE in cj:
                for k in ("fid", "schoolid", "schoolId", "unitId"):
                    if k in c:
                        class_fid = c[k]
                        break
                print("[backclazz matched keys]", sorted(c.keys()))
                print("[backclazz sample]", cj[:500])
                break
    except Exception as e:
        print("[backclazz] ERR", e)
    print("[class_fid]", class_fid)

    puid = str(smsg.get("puid") or scookie.get("_uid"))
    real_name = smsg.get("name") or ""
    s_fid = str(smsg.get("fid") if smsg.get("fid") is not None else 0)
    t_fid = str(tmsg.get("fid") if tmsg.get("fid") is not None else 0)

    t = C.TeacherSide(tck, TUID, quiet_hours=None, max_writes_per_hour=60, min_interval=0.3, per_day=2000)
    aid = t.create_sign(COURSE, CLAZZ, other_id="0", if_photo="1", face="0", time_long="1800000", title="拍照矩阵v8")
    print("[create] aid =", aid)
    if not aid:
        return

    r = requests.get(MOBILE + "/v2/apis/active/student/activelist?fid=0&showNotStartedActive=0&courseId=%s&classId=%s" % (COURSE, CLAZZ),
                     headers={"Cookie": sck, "User-Agent": UA_APP}, timeout=20)
    jj = r.json()
    ext = ((jj.get("data") or {}).get("ext") or {}).get("_from_", "")
    ent = {}
    for a in ((jj.get("data") or {}).get("activeList") or []):
        if str(a.get("id")) == str(aid):
            ent = a
    print("[ext]", ext, "| active ent keys:", sorted(ent.keys()) if ent else None)
    if ent:
        print("[active ent]", json.dumps(ent, ensure_ascii=False)[:400])

    s = requests.Session()
    s.headers.update({"Cookie": sck, "User-Agent": UA_APP})
    print("[preSign]", pre_sign(s, aid, ext, puid).status_code)
    print("[analysis]", json.dumps(analysis(s, aid), ensure_ascii=False))

    img = "out/photo_v8_%d.jpg" % int(time.time())
    wh = randomize("/tmp/cx29/lena.jpg", img)
    fname = os.path.basename(img)
    tk, up = upload(s, puid, img, fname)
    print("[upload plain]", json.dumps(up, ensure_ascii=False)[:260])
    oid = up.get("objectId")
    enc_id = ((up.get("data") or {}) if isinstance(up.get("data"), dict) else {}).get("encryptedId")
    if not oid:
        return
    tk2, up_fid = upload(s, puid, img, fname, fid=12)
    print("[upload fid=12]", json.dumps({k: up_fid.get(k) for k in ("result", "msg", "objectId")}, ensure_ascii=False))
    tk3, up_alt = upload(s, puid, img, fname, host=PANALT)
    print("[upload cldisk]", json.dumps({k: up_alt.get(k) for k in ("result", "msg", "objectId")}, ensure_ascii=False)[:200])

    raw_resp = json.dumps(up, ensure_ascii=False)

    def run(tag, pairs, pr=None, method="GET", hdr_extra=None):
        qs = "&".join("%s=%s" % (k, quote(str(v), safe="")) for k, v in pairs)
        data = {k: v for k, v in pairs}
        if pr is not None:
            data["photoResult"] = pr
            qs += "&photoResult=" + quote(pr, safe="")
        hdr = {"Referer": MOBILE + "/newsign/preSign?activePrimaryId=" + aid,
               "X-Requested-With": "XMLHttpRequest"}
        if hdr_extra:
            hdr.update(hdr_extra)
        url = MOBILE + "/pptSign/stuSignajax?" + qs
        try:
            rr = s.get(url, headers=hdr, timeout=30) if method == "GET" else s.post(MOBILE + "/pptSign/stuSignajax", data=data, headers=hdr, timeout=30)
            body = rr.text.strip()
            print("[%s] %s %s len=%d :: %s" % (tag, method, rr.status_code, len(rr.text), body[:160]))
            return body
        except Exception as e:
            print("[%s] ERR %s" % (tag, e))
            return "EXC"

    def p2020(fid, objid=oid, name=None):
        # 逐字复刻 2020 抓包：没有 courseId / photoResult / deviceCode
        return [("activeId", aid), ("uid", puid), ("clientip", ""), ("useragent", ""),
                ("latitude", "-1"), ("longitude", "-1"), ("appType", "15"),
                ("fid", fid), ("objectId", objid), ("name", real_name if name is None else name)]

    def pcxsign(fid, objid=oid, name=None):
        return [("activeId", aid), ("uid", puid), ("fid", fid), ("courseId", COURSE), ("classId", CLAZZ),
                ("clientip", ""), ("appType", "15"), ("name", real_name if name is None else name),
                ("useragent", ""), ("objectId", objid), ("latitude", "-1"), ("longitude", "-1")]

    fids = []
    for cand in (s_fid, "12", t_fid, str(class_fid) if class_fid else None):
        if cand is not None and cand not in fids:
            fids.append(cand)
    print("[fid candidates]", fids)

    variants = []
    for f in fids:
        variants.append(("A2020_fid%s" % f, p2020(f), None, "GET"))
    variants += [
        ("B_2020_nameFile", p2020(fids[0], name=fname), None, "GET"),
        ("C_2020_noObjectId", p2020(fids[0], objid=""), None, "GET"),
        ("D_cxsign_fid%s" % fids[0], pcxsign(fids[0]), None, "GET"),
        ("E_ru41_wholeResp", pcxsign(fids[0]), raw_resp, "GET"),
        ("F_objectId_encryptedId", p2020(fids[0], objid=enc_id or oid), None, "GET"),
        ("G_2020_POST", p2020(fids[0]), None, "POST"),
        ("H_cxsign_POST_wholeResp", pcxsign(fids[0]), raw_resp, "POST"),
        ("I_2020_ua_dalvik", p2020(fids[0]), None, "GET"),
    ]

    results = {}
    for item in variants:
        tag, pairs, pr, meth = item
        he = {"User-Agent": "Dalvik/2.1.0 (Linux; U; Android 13; SM-G975F Build/TQ3A.230901.001) com.chaoxing.mobile/ChaoXingStudy_6.7.8_android_phone"} if tag.endswith("dalvik") else None
        body = run(tag, pairs, pr, meth, he)
        results[tag] = body[:300]
        if body.strip().lower() in ("success", "success2"):
            print("*** 命中成功：", tag)
            break

    with open("out/photo_matrix8.json", "w", encoding="utf-8") as f:
        json.dump({"aid": aid, "oid": oid, "encryptedId": enc_id, "img": img, "ext": ext,
                   "student": {k: smsg.get(k) for k in ("uid", "puid", "fid", "name")},
                   "teacher": {k: tmsg.get(k) for k in ("uid", "puid", "fid", "name")},
                   "class_fid": class_fid, "fids": fids, "upload": up, "results": results}, f,
                  ensure_ascii=False, indent=1)
    print("[saved] out/photo_matrix8.json")


if __name__ == "__main__":
    main()
