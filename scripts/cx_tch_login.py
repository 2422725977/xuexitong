#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""学习通 Web 端「手机号 + 短信验证码」登录（教师账号用，桌面浏览器路径）。

契约来源（passport2-static.chaoxing.com/js/fanya/util.js 与 login.js 实测抓取）：
  ① 上限自检  POST {_CP_}/num/booleanCode?key=<phone>&type=1
     → 响应体 "alert" 表示「超出今日验证码发送上限」，其它值可继续。
  ② 发码      GET  {_CP_}/num/phonecode?phone=<phone>&code=&type=1&needcode=false
                   &countrycode=86&validate=&fid=-1
     → JSON {"result":true,...} / {"result":false,"msg":"..."}
  ③ 登录      POST {_CP_}/fanyaloginbycode
     data = fid, uname=<手机号明文>, verCode=encodeURIComponent(AES(验证码,transferKey)),
            refer=http%3A%2F%2Fi.chaoxing.com, doubleFactorLogin=0,
            independentNameId=0, countrycode=86
     → {"status":true,"url":"http%3A%2F%2Fi.chaoxing.com",...}
       status 为真后必须 unquote(url) 再跟随；
       containTwoFactorLogin 为真 → 双因子页（twoFactorLoginPCUrl）；
       type==1 → 该手机号未注册/需走注册流程。

AES 与密码登录同一个 transferKey（cx_login.TRANSFER_KEY），复用 cx_login.aes_b64。

用法：
  python3 scripts/cx_tch_login.py send  --phone 1xxxxxxxxxx
  python3 scripts/cx_tch_login.py login --phone 1xxxxxxxxxx --code 123456 --out ck_tch.txt
  python3 scripts/cx_tch_login.py auto  --phone 1xxxxxxxxxx          # send + 交互输入验证码
"""
import argparse, json, os, re, sys, time
from urllib.parse import unquote

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cx_login import TRANSFER_KEY, aes_b64, UA, KEY_COOKIES  # noqa: E402

CP = "https://passport2.chaoxing.com"
REFER_FIELD = "http%3A%2F%2Fi.chaoxing.com"
HOSTS = ["https://i.chaoxing.com", "https://mooc1.chaoxing.com",
         "https://mooc1-api.chaoxing.com", "https://mobilelearn.chaoxing.com"]


def mask(s, keep=4):
    s = str(s or "")
    return s[:keep] + "*" * max(0, len(s) - keep) if len(s) > keep else "***"


def make_session(cookie=None):
    import requests
    s = requests.Session()
    s.headers.update({
        "User-Agent": UA,
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Origin": CP,
        "Referer": CP + "/login?loginType=2&newversion=true&fid=-1&refer=" + REFER_FIELD,
        "X-Requested-With": "XMLHttpRequest",
    })
    if cookie:
        s.headers["Cookie"] = cookie
    return s


def check_limit(s, phone):
    """返回 True 表示还能发（未超限）。"""
    try:
        r = s.post(CP + "/num/booleanCode?key=%s&type=1" % phone, timeout=20)
        body = (r.text or "").strip()
        print("[limit] HTTP %s  %s" % (r.status_code, body[:80]))
        return body.lower() != "alert"
    except Exception as e:
        print("[limit] 检查失败（忽略）：%s" % e)
        return True


def send_code(s, phone, countrycode="86", fid="-1"):
    url = (CP + "/num/phonecode?phone=%s&code=&type=1&needcode=false"
                 "&countrycode=%s&validate=&fid=%s" % (phone, countrycode, fid))
    r = s.get(url, timeout=25)
    print("[send] HTTP %s  %s" % (r.status_code, (r.text or "")[:200]))
    try:
        j = r.json()
    except Exception:
        return False, (r.text or "")[:200]
    ok = bool(j.get("result"))
    return ok, (j.get("msg") or "")


def do_login(s, phone, code, countrycode="86", fid="-1", out="ck_tch.txt", jar_out="ck_tch.json"):
    vercode = aes_b64(code, TRANSFER_KEY)
    # login.js 里是 encodeURIComponent(AES(...))；requests 表单编码对 + / = 的结果一致
    data = {
        "fid": fid,
        "uname": phone,                 # 验证码登录用手机号明文（密码登录才 AES）
        "verCode": vercode,
        "refer": REFER_FIELD,
        "doubleFactorLogin": "0",
        "independentNameId": "0",
        "countrycode": countrycode,
    }
    r = s.post(CP + "/fanyaloginbycode", data=data, timeout=30)
    print("[login] HTTP %s" % r.status_code)
    try:
        j = r.json()
    except Exception:
        print("[login] 非 JSON 响应：%s" % (r.text or "")[:300])
        return False
    if not j.get("status"):
        print("[login] 失败：msg=%s  msg2=%s  type=%s" % (j.get("msg"), j.get("msg2"), j.get("type")))
        if j.get("type") == 1:
            print("[login] 该手机号未注册/需注册流程 quickUrl=%s url=%s" % (j.get("quickUrl"), j.get("url")))
        return False
    if j.get("containTwoFactorLogin"):
        print("[login] 需要双因子认证：%s" % j.get("twoFactorLoginPCUrl"))
        return False
    url = unquote(j.get("url") or "https://i.chaoxing.com")
    print("[login] 成功，跟随 → %s" % url)
    try:
        s.get(url, timeout=25, allow_redirects=True)
    except Exception as e:
        print("[login] 跟随跳转异常（忽略）：%s" % e)
    for h in HOSTS:                      # 逐个域抚摸一遍，拿到各自域票
        try:
            s.get(h + "/", timeout=20, allow_redirects=True)
        except Exception:
            pass
    jar = s.cookies.get_dict()
    got = [k for k in KEY_COOKIES if k in jar]
    print("[cookies] 共 %d 个，关键字段命中 %s" % (len(jar), ",".join(got) or "无"))
    if not any(k in jar for k in ("_uid", "UID")):
        print("[cookies] 未拿到身份 cookie，放弃写盘")
        return False
    ck = "; ".join("%s=%s" % (k, v) for k, v in jar.items())
    with open(out, "w") as f:
        f.write(ck)
    try:
        with open(jar_out, "w") as f:
            json.dump(jar, f, ensure_ascii=False, indent=1)
    except Exception:
        pass
    print("[cookies] 已写 %s（%d B）与 %s" % (out, len(ck), jar_out))
    print("[cookies] _uid=%s" % jar.get("_uid", jar.get("UID", "?")))
    return True


def main():
    ap = argparse.ArgumentParser(description="学习通手机号+短信验证码登录（Web 桌面路径）")
    ap.add_argument("mode", choices=["send", "login", "auto"])
    ap.add_argument("--phone", required=True)
    ap.add_argument("--code", default="")
    ap.add_argument("--countrycode", default="86")
    ap.add_argument("--fid", default="-1")
    ap.add_argument("--out", default="ck_tch.txt")
    ap.add_argument("--jar", default="ck_tch.json")
    ap.add_argument("--cookie", default=None, help="已有会话 cookie（可选）")
    ap.add_argument("--skip-limit-check", action="store_true")
    a = ap.parse_args()
    if not re.fullmatch(r"\d{11}", a.phone):
        print("手机号必须是 11 位数字")
        return 2
    s = make_session(a.cookie)

    if a.mode in ("send", "auto"):
        if not a.skip_limit_check and not check_limit(s, a.phone):
            print("[send] 已被今日发送上限拦住，未发码")
            return 3
        ok, msg = send_code(s, a.phone, a.countrycode, a.fid)
        print("[send] %s%s" % ("已发出" if ok else "发送失败", ("：" + msg) if msg else ""))
        if not ok:
            return 4
    if a.mode == "send":
        print("[下一步] 收到短信后运行：python3 scripts/cx_tch_login.py login --phone %s --code <验证码>" % a.phone)
        return 0

    code = a.code
    if not code:
        try:
            code = input("请输入收到的 6 位验证码：").strip()
        except EOFError:
            print("无输入")
            return 5
    if not re.fullmatch(r"\d{4,6}", code or ""):
        print("验证码格式异常")
        return 6
    ok = do_login(s, a.phone, code, a.countrycode, a.fid, a.out, a.jar)
    return 0 if ok else 7


if __name__ == "__main__":
    sys.exit(main())
