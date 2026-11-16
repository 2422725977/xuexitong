# -*- coding: utf-8 -*-
"""v16：上传侧上下文 + 提交侧附加字段（crc/resid/size/suffix）矩阵。首个 success 即停。"""
import json, os, re, sys, time, random, hashlib
from urllib.parse import quote
import requests
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cx_pipeline as C
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
UA_APP = ('Mozilla/5.0 (Linux; Android 13; SM-G975F Build/TQ3A.230901.001) AppleWebKit/537.36 (KHTML, like Gecko) '
          'Version/4.0 Chrome/120.0.0.0 Mobile Safari/537.36 (schild:b1c2d3e4f5a60718) (device:SM-G975F) '
          'Language/zh_CN com.ssreader.ChaoXingStudy/ChaoXingStudy_3_6_2_android_phone_20230101')
MOBILE = "https://mobilelearn.chaoxing.com"
PANTOKEN = "https://pan-yz.chaoxing.com/api/token/uservalid"
PANUPLOAD = "https://pan-yz.chaoxing.com/upload"
CRC = "https://pan-yz.chaoxing.com/api/crcstatus"
COURSE, CLAZZ, TUID = "269282723", "159926750", "[教师PUID]"
sck = open("ck.txt", encoding="utf-8").read().strip()
tck = open("ck_tch.txt", encoding="utf-8").read().strip()
S = requests.Session(); S.headers.update({"Cookie": sck, "User-Agent": UA_APP})

# 教师建新活动（干净）
T = C.TeacherSide(tck, TUID, quiet_hours=None, max_writes_per_hour=60, min_interval=0.3, per_day=2000)
AID = T.create_sign(COURSE, CLAZZ, other_id="0", if_photo="1", face="0", time_long="1800000", title="拍照矩阵v16", verbose=False)
print("[create] aid =", AID)
if not AID:
    raise SystemExit("create failed")
S.get(MOBILE + "/newsign/preSign?courseId=%s&classId=%s&activePrimaryId=%s&general=1&sys=1&ls=1&appType=15&uid=[学生PUID]&isTeacherViewOpen=0" % (COURSE, CLAZZ, AID), timeout=25)

# 图片
from PIL import Image
src = "/tmp/cx29/lena.jpg"
im = Image.open(src); w, h = im.size
f = 0.9 + random.random() * 0.09
cx, cy = int(w * (1 - f) / 2), int(h * (1 - f) / 2)
im = im.crop((cx, cy, w - cx, h - cy))
img = "out/photo_v16_%d.jpg" % int(time.time())
im.save(img, "JPEG", quality=random.randint(85, 95))
fname = os.path.basename(img)
blob = open(img, "rb").read()
crc = hashlib.md5(blob).hexdigest()
tk = S.get(PANTOKEN, timeout=20).json()["_token"]
print("[img] %s size=%d crc=%s" % (img, len(blob), crc))

def upload(tag, qs="", form_extra=None, do_crc=False, ref=None):
    if do_crc:
        rc = S.get(CRC + "?puid=[学生PUID]&crc=%s&_token=%s" % (crc, tk), timeout=20)
        print("   [crcstatus]", rc.text.strip()[:120])
    url = PANUPLOAD + "?_from=mobilelearn&_token=" + tk + qs
    form = {"puid": "[学生PUID]"}
    if form_extra:
        form.update(form_extra)
    hd = {"Referer": ref} if ref else None
    r = S.post(url, files={"file": (fname, blob, "image/jpeg")}, data=form, headers=hd, timeout=60)
    try:
        j = r.json()
    except Exception:
        j = {"raw": r.text[:200]}
    oid = j.get("objectId") or ""
    print("   [%s] oid=%s %s" % (tag, oid, str({k: j.get(k) for k in ("result", "msg", "resid")})[:120]))
    return oid, j

def submit(tag, oid, extra=None, pr=None, method="GET"):
    pairs = [("activeId", AID), ("courseId", COURSE), ("uid", "[学生PUID]"), ("clientip", ""), ("useragent", ""),
             ("latitude", "-1"), ("longitude", "-1"), ("appType", "15"), ("fid", "0"), ("name", "学生示例")]
    if oid:
        pairs.append(("objectId", oid))
    if extra:
        pairs += extra
    data = dict(pairs)
    qs = "&".join("%s=%s" % (k, quote(str(v), safe="")) for k, v in pairs)
    if pr:
        data["photoResult"] = pr; qs += "&photoResult=" + quote(pr, safe="")
    h = {"Referer": MOBILE + "/newsign/preSign?activePrimaryId=" + AID, "X-Requested-With": "XMLHttpRequest"}
    url = MOBILE + "/pptSign/stuSignajax?" + qs
    r = S.get(url, headers=h, timeout=25) if method == "GET" else S.post(MOBILE + "/pptSign/stuSignajax", data=data, headers=h, timeout=25)
    body = r.text.strip()
    print("[%-30s] %s :: %s" % (tag, r.status_code, body[:120]))
    return body

results = {}
def record(tag, body):
    results[tag] = body[:200]

oid_base, up_base = upload("base", "")
oid_act, _ = upload("activeId_in_upload", "&activeId=" + AID)
oid_act_f, _ = upload("activeId_form", "", {"activeId": AID})
oid_ctx, _ = upload("course_ctx", "&courseId=%s&classId=%s&activeId=%s" % (COURSE, CLAZZ, AID))
oid_crc, _ = upload("crc_then_upload", "", None, do_crc=True)
oid_ref, _ = upload("referer_presign", "", None, False, ref=MOBILE + "/newsign/preSign?activePrimaryId=" + AID)

cases = [
    ("U1_base", oid_base, None, None, "GET"),
    ("U2_uploadctx_oid", oid_act, None, None, "GET"),
    ("U3_uploadform_oid", oid_act_f, None, None, "GET"),
    ("U4_coursecx_oid", oid_ctx, None, None, "GET"),
    ("U5_crc_oid", oid_crc, None, None, "GET"),
    ("U6_referer_oid", oid_ref, None, None, "GET"),
    ("U7_crc_resid_size", oid_base, [("crc", crc), ("resid", str(up_base.get("resid") or "")), ("size", str(len(blob))), ("suffix", "jpg")], None, "GET"),
    ("U8_oid_is_resid", str(up_base.get("resid") or ""), None, None, "GET"),
    ("U9_crc_only", oid_base, [("crc", crc)], None, "GET"),
    ("U10_wholeresp", oid_base, None, json.dumps(up_base, ensure_ascii=False), "GET"),
    ("U11_base_POST", oid_base, None, None, "POST"),
]
hit = None
for tag, oid, extra, pr, meth in cases:
    body = submit(tag, oid, extra, pr, meth)
    record(tag, body)
    if body.strip().lower() in ("success", "success2"):
        hit = tag
        print("*** 命中：", tag)
        break
with open("out/photo_matrix16.json", "w", encoding="utf-8") as fp:
    json.dump({"aid": AID, "img": img, "crc": crc, "oids": {"base": oid_base, "act": oid_act, "ctx": oid_ctx,
               "crc": oid_crc, "ref": oid_ref}, "results": results, "hit": hit}, fp, ensure_ascii=False, indent=1)
print("[saved] out/photo_matrix16.json")
