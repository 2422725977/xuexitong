#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""stuonly_sign.py — 只有学生 cookie（无教师端）时的全类型签到。
用法示例：
  python3 scripts/stuonly_sign.py --active-id 4000180998060 --auto
  python3 scripts/stuonly_sign.py --active-id 4000180998624 --auto --sign-code 147258
  python3 scripts/stuonly_sign.py --active-id 4000180998628 --auto --lat 30.71142 --lon 103.86839 --address "四川农业大学(成都校区)"
  python3 scripts/stuonly_sign.py --active-id 4000180998089 --auto --qr-image shot.png
  python3 scripts/stuonly_sign.py --list            # 列出当前可签的活动（courseactivelist）
"""
import argparse, hashlib, json, os, re, sys, time
import requests

BASE = "https://mobilelearn.chaoxing.com"
DEFAULT_UA = ("Mozilla/5.0 (Linux; Android 11; MI 9 Build/RKQ1.200826.002; wv) "
              "AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/90.0.4430.210 Mobile Safari/537.36")

TYPE_NAME = {0: "普通", 2: "二维码", 3: "手势", 4: "位置", 5: "签到码"}
OK = ("success", "success2")


def load_cookie(path="ck.txt"):
    if path and os.path.exists(path):
        return open(path, encoding="utf-8").read().strip()
    return ""


class Stu:
    def __init__(self, cookie=None, uid=None, course_id=None, class_id=None,
                 proxy=None, timeout=25):
        self.s = requests.Session()
        self.s.headers.update({"User-Agent": DEFAULT_UA, "X-Requested-With": "com.chaoxing.mobile"})
        self.cookie = (cookie or load_cookie()).replace("\n", "").strip()
        # 直接整串塞进 Cookie 头（与 App 一致；解析成 cookiejar 易丢 uid/_uid）
        self.s.headers["Cookie"] = self.cookie
        self.uid = uid or "[学生PUID]"
        self.course_id = course_id or "269282723"
        self.class_id = class_id or "159926750"
        self.timeout = timeout
        if proxy:
            self.s.proxies = {"http": proxy, "https": proxy}

    # ---------- 只读 ----------
    def detail(self, aid):
        r = self.s.get(f"{BASE}/newsign/signDetail", params={"activePrimaryId": aid, "type": "1"},
                       timeout=self.timeout)
        try:
            return r.json()
        except Exception:
            return {}

    def sign_type(self, aid):
        """由 signDetail 判定签到类型 -> (type_key, label)"""
        d = self.detail(aid)
        if not d:
            return None, "未知(signDetail 拉取失败)"
        o = str(d.get("otherId", "0"))
        if o == "4" or str(d.get("ifopenAddress", "0")) == "1":
            return 4, TYPE_NAME[4]
        if str(d.get("ifPhoto", "0")) == "1":
            return 1, "拍照"
        m = {"2": 2, "3": 3, "5": 5, "0": 0, "1": 1}
        k = m.get(o, 0)
        return k, ("拍照" if k == 1 else TYPE_NAME.get(k, f"未知({o})"))

    def pre_sign(self, aid):
        """拉学生签到页，返回页面源码（含隐藏 signCode 等）"""
        url = (f"{BASE}/newsign/preSign?courseId={self.course_id}&classId={self.class_id}"
               f"&activePrimaryId={aid}&uid={self.uid}&role=1&appType=15&isTeacherViewOpen=0")
        r = self.s.get(url, timeout=self.timeout)
        return r.text

    def page_sign_code(self, aid):
        html = self.pre_sign(aid)
        m = re.search(r'id="signCode"[^>]*value="([^"]*)"', html)
        return (m.group(1) if m else ""), html

    def list_active(self):
        r = self.s.get(f"{BASE}/ppt/activeAPI/courseactivelist",
                       params={"puid": self.uid, "status": "1", "page": "1", "pageSize": "50"},
                       timeout=self.timeout)
        try:
            return r.json().get("data") or []
        except Exception:
            return []

    # ---------- 写操作 ----------
    def check_sign_code(self, aid, code):
        """手势/签到码预校验；必须 GET（POST 会 500）"""
        r = self.s.get(f"{BASE}/widget/sign/pcStuSignController/checkSignCode",
                       params={"activeId": aid, "signCode": code}, timeout=self.timeout)
        try:
            return r.json()
        except Exception:
            return {"raw": r.text[:200], "status": r.status_code}

    def submit(self, aid, sign_code="", enc="", location="", location_result="",
               object_id="", photo_result="", extra=None, method="get"):
        p = {"activeId": aid, "courseId": self.course_id, "uid": self.uid, "clientip": "",
             "useragent": DEFAULT_UA if method == "get" else "", "latitude": "-1", "longitude": "-1",
             "appType": "15", "fid": "0", "name": ""}
        if sign_code:
            p["signCode"] = sign_code
        if enc:
            p["enc"] = enc
        if location:
            p["location"] = location
        if location_result:
            p["locationResult"] = location_result
        if object_id:
            p["objectId"] = object_id
        if photo_result:
            p["photoResult"] = photo_result
        if extra:
            p.update(extra)
        url = f"{BASE}/pptSign/stuSignajax"
        if method == "post":
            r = self.s.post(url, data=p, timeout=self.timeout)
        else:
            r = self.s.get(url, params=p, timeout=self.timeout)
        body = (r.text or "").strip()
        return r.status_code, body

    # ---------- 类型战术 ----------
    def do_normal(self, aid):
        return self.submit(aid)

    def do_code(self, aid, code):
        return self.submit(aid, sign_code=code)

    def do_location(self, aid, lat, lon, address="", only_location=False):
        loc = json.dumps({"result": 1, "address": address, "longitude": float(lon),
                          "latitude": float(lat)}, ensure_ascii=False)
        return self.submit(aid, location=loc, location_result="" if only_location else loc)

    def do_qr(self, aid, enc):
        return self.submit(aid, enc=enc)

    def decode_qr_file(self, path):
        try:
            import cv2
        except Exception as e:
            raise SystemExit("需要 opencv-python：%s" % e)
        img = cv2.imread(path)
        data, _, _ = cv2.QRCodeDetector().detectAndDecode(img)
        return self.enc_from_qr_text(data)

    def enc_from_qr_text(self, text):
        m = re.search(r"[?&]enc=([0-9A-Fa-f]+)", text or "")
        if m:
            return m.group(1)
        m = re.search(r"\benc=([0-9A-Fa-f]{8,64})", text or "")
        return m.group(1) if m else ""

    def do_photo(self, aid, object_id, name="photo.jpg", photo_result=None):
        if photo_result is None:
            photo_result = json.dumps({"files": [{"name": name, "objectid": object_id, "type": "jpg"}]})
        return self.submit(aid, object_id=object_id, photo_result=photo_result, method="post",
                           extra={"name": name})


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cookie", default="ck.txt")
    ap.add_argument("--uid", default="[学生PUID]")
    ap.add_argument("--course-id", default="269282723")
    ap.add_argument("--class-id", default="159926750")
    ap.add_argument("--active-id")
    ap.add_argument("--auto", action="store_true", help="自动判定类型并提交")
    ap.add_argument("--type", choices=["0", "1", "2", "3", "4", "5"])
    ap.add_argument("--sign-code", default="")
    ap.add_argument("--enc", default="")
    ap.add_argument("--qr-image", default="")
    ap.add_argument("--lat", default="")
    ap.add_argument("--lon", default="")
    ap.add_argument("--address", default="")
    ap.add_argument("--object-id", default="")
    ap.add_argument("--only-location", action="store_true", help="只带 location 不带 locationResult")
    ap.add_argument("--list", action="store_true")
    a = ap.parse_args()

    _ck = load_cookie(a.cookie) or a.cookie   # --cookie 可传文件路径或整串
    st = Stu(_ck, a.uid, a.course_id, a.class_id)
    if a.list:
        for it in st.list_active():
            print(json.dumps(it, ensure_ascii=False)[:300])
        return
    if not a.active_id:
        raise SystemExit("需要 --active-id 或 --list")
    aid = a.active_id
    key, label = st.sign_type(aid)
    print(f"[*] activeId={aid} 类型={label}(key={key})")
    code = a.sign_code
    if not code:
        code, _html = st.page_sign_code(aid)
        if code:
            print(f"[*] 页面隐藏 signCode={code}")

    if a.enc:
        enc = a.enc
    elif a.qr_image:
        enc = st.decode_qr_file(a.qr_image)
        print(f"[*] 二维码解出 enc={enc}")
    else:
        enc = ""

    if a.type:
        t = int(a.type)
    elif a.auto:
        t = key if key is not None else 0
    else:
        t = None
    if t is None:
        raise SystemExit("需要 --auto 或 --type")

    if t in (3, 5):
        print("[*] 预校验:", json.dumps(st.check_sign_code(aid, code), ensure_ascii=False)[:160])
        sc, body = st.do_code(aid, code)
    elif t == 4:
        sc, body = st.do_location(aid, a.lat or 30.71142640936642, a.lon or 103.868397592583,
                                  a.address, a.only_location)
    elif t == 2:
        sc, body = st.do_qr(aid, enc)
    elif t == 1:
        sc, body = st.do_photo(aid, a.object_id)
    else:
        sc, body = st.do_normal(aid)
    print(f"[=] HTTP {sc} -> {body[:200]}")
    if body in OK:
        print("[=] 签到成功" + ("（迟到/已过截止）" if body == "success2" else ""))
    elif "已签到过" in body:
        print("[=] 之前已签到")


if __name__ == "__main__":
    main()
