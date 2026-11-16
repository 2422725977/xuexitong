# -*- coding: utf-8 -*-
"""v17：上传带 fid / 只保存再启动 / validate 显式空 / 提名候选 photoAuth 端点。"""
import json, os, sys, time, random, hashlib
from urllib.parse import quote
import requests
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cx_pipeline as C
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
UA_APP = ('Mozilla/5.0 (Linux; Android 13; SM-G975F Build/TQ3A.230901.001) AppleWebKit/537.36 (KHTML, like Gecko) '
          'Version/4.0 Chrome/120.0.0.0 Mobile Safari/537.36 (schild:b1c2d3e4f5a60718) (device:SM-G975F) '
          'Language/zh_CN com.ssreader.ChaoXingStudy/ChaoXingStudy_3_6_2_android_phone_20230101')
MOBILE = "https://mobilelearn.chaoxing.com"
COURSE, CLAZZ, TUID = "269282723", "159926750", "401537379"
sck = open("ck.txt", encoding="utf-8").read().strip()
tck = open("ck_tch.txt", encoding="utf-8").read().strip()
S = requests.Session(); S.headers.update({"Cookie": sck, "User-Agent": UA_APP})
T = C.TeacherSide(tck, TUID, quiet_hours=None, max_writes_per_hour=60, min_interval=0.3, per_day=2000)

def pre(aid):
    S.get(MOBILE + "/newsign/preSign?courseId=%s&classId=%s&activePrimaryId=%s&general=1&sys=1&ls=1&appType=15&uid=493228247&isTeacherViewOpen=0" % (COURSE, CLAZZ, aid), timeout=25)

def img_prep():
    from PIL import Image
    im = Image.open("/tmp/cx29/lena.jpg"); w, h = im.size
    f = 0.9 + random.random() * 0.09
    cx, cy = int(w*(1-f)/2), int(h*(1-f)/2)
    im = im.crop((cx, cy, w-cx, h-cy))
    p = "out/photo_v17_%d.jpg" % int(time.time()); im.save(p, "JPEG", quality=random.randint(85, 95))
    return p, open(p, "rb").read()

def upload(blob, fname, fid=None, extra=None):
    tk = S.get("https://pan-yz.chaoxing.com/api/token/uservalid", timeout=20).json()["_token"]
    form = {"puid": "493228247"}
    if fid is not None:
        form["fid"] = str(fid)
    if extra:
        form.update(extra)
    r = S.post("https://pan-yz.chaoxing.com/upload?_from=mobilelearn&_token=" + tk,
               files={"file": (fname, blob, "image/jpeg")}, data=form, timeout=60)
    j = r.json(); print("   [upload fid=%s extra=%s] oid=%s resid=%s" % (fid, extra, j.get("objectId"), j.get("resid")))
    return j.get("objectId") or "", j

def submit(tag, aid, oid, fid="0", extra=None, pr=None, method="GET"):
    pairs = [("activeId", aid), ("courseId", COURSE), ("uid", "493228247"), ("clientip", ""), ("useragent", ""),
             ("latitude", "-1"), ("longitude", "-1"), ("appType", "15"), ("fid", str(fid)), ("name", "学生示例")]
    if oid:
        pairs.append(("objectId", oid))
    if extra:
        pairs += extra
    data = dict(pairs)
    if pr:
        data["photoResult"] = pr
    qs = "&".join("%s=%s" % (k, quote(str(v), safe="")) for k, v in pairs) + ("&photoResult=" + quote(pr, safe="") if pr else "")
    h = {"Referer": MOBILE + "/newsign/preSign?activePrimaryId=" + str(aid), "X-Requested-With": "XMLHttpRequest"}
    r = S.get(MOBILE + "/pptSign/stuSignajax?" + qs, headers=h, timeout=25) if method == "GET" else \
        S.post(MOBILE + "/pptSign/stuSignajax", data=data, headers=h, timeout=25)
    print("[%-26s] %s :: %s" % (tag, r.status_code, r.text.strip()[:100]))
    return r.text.strip()

res = {}
# ---- 端点存在性探测
print("== endpoint probe ==")
for p in ["pptSign/uploadPhoto", "pptSign/photoAuth", "pptSign/photoauth", "pptSign/photo", "pptSign/photoresult",
          "newsign/uploadPhoto", "sign/uploadPhoto", "pptSign/getPhotoAuth", "pptSign/photoTask",
          "widget/sign/api/photoAuth", "v2/apis/sign/photoAuth", "pptSign/refreshQRCode", "v2/apis/sign/refreshQRCode"]:
    try:
        r = S.get(MOBILE + "/" + p + "?activeId=4000180999331", timeout=20)
        print("  %-34s %s len=%d %s" % (p, r.status_code, len(r.text), r.text.strip()[:60].replace("\n", " ")))
    except Exception as e:
        print("  %-34s ERR %s" % (p, e))

# ---- E1: 上传带 fid + 提交同 fid
print("== E1 ==")
aid1 = T.create_sign(COURSE, CLAZZ, other_id="0", if_photo="1", face="0", time_long="1800000", title="拍照E1", verbose=False)
pre(aid1); img1, blob1 = img_prep()
oid_f12, _ = upload(blob1, os.path.basename(img1), fid="12")
oid_f1022, _ = upload(blob1, os.path.basename(img1), fid="1022")
res["E1"] = submit("E1a_fid12", aid1, oid_f12, fid="12")
if res["E1"].lower() not in ("success", "success2"):
    res["E1b"] = submit("E1b_fid1022", aid1, oid_f1022, fid="1022")
    res["E1c"] = submit("E1c_fid0_oid_f12", aid1, oid_f12, fid="0")

# ---- E2: 先保存(不开始) 再 restartActive 启动
print("== E2 ==")
aid2 = T.create_sign(COURSE, CLAZZ, other_id="0", if_photo="1", face="0", time_long="1800000", title="拍照E2", start=False, verbose=False)
print("   saved aid=", aid2)
rr = S.get(MOBILE + "/widget/active/restartActive?activePrimaryId=%s&timeLong=1800000" % aid2, timeout=25)
print("   restart:", rr.status_code, rr.text.strip()[:120])
pre(aid2); img2, blob2 = img_prep()
oid2, _ = upload(blob2, os.path.basename(img2))
res["E2"] = submit("E2_after_restart", aid2, oid2)

# ---- E3: validate 显式空 + 参数全带
print("== E3 ==")
res["E3a"] = submit("E3a_validate_empty", aid2, oid2, extra=[("validate", ""), ("deviceCode", "5UpR078A5CXE0X9wckWZqco+3W2FKfGichnoLiFd2iU=")])
res["E3b"] = submit("E3b_validatename", aid2, oid2, extra=[("validate", "mySignCaptchaUtils.VALIDATE_CODE_STR")])

# ---- E4: 上传带 _from + fid + 用 preSign 抓到的 fid
print("== E4 ==")
aid4 = T.create_sign(COURSE, CLAZZ, other_id="0", if_photo="1", face="0", time_long="1800000", title="拍照E4", verbose=False)
pre(aid4); img4, blob4 = img_prep()
oid4, j4 = upload(blob4, os.path.basename(img4), fid="1022", extra={"srcAsHd": "1", "type": "1"})
res["E4"] = submit("E4_srcAsHd_upload", aid4, oid4, fid="1022", extra=[("srcAsHd", "1")])

json.dump({"aids": {"E1": aid1, "E2": aid2, "E4": aid4}, "res": res}, open("out/photo_matrix17.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("[saved] out/photo_matrix17.json")
