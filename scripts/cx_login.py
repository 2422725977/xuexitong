#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""学习通 Web 端登录（桌面浏览器路径）→ 导出 cookie 供只读抓取使用。

为什么走这条路：服务端看到的是「用户在自己电脑浏览器上登录学习通」——
没有 App UA、没有模拟器、没有 root、没有注入框架，账号设备列表不会新增一台机器。
（App / 模拟器登录才会把设备写进账号，并撞上梆梆 everisk 的模拟器检测。）

契约来源：passport2-static.chaoxing.com/js/fanya/login.js 的 loginByPhoneAndPwdSubmit()
  POST https://passport2.chaoxing.com/fanyalogin
  fid=-1  refer=http%3A%2F%2Fi.chaoxing.com  t=true  forbidotherlogin=0
  doubleFactorLogin=0  independentId=0  independentNameId=0  validate=
  uname   = base64(AES-CBC-PKCS7(手机号, key, iv=key))
  password= base64(AES-CBC-PKCS7(密码,   key, iv=key))
  key = 页面里的 transferKey（10 字符，直接取自 login.js）

用法（密码走环境变量，不进 argv / 不进 shell history）：
  CX_PHONE=1xxxxxxxxxx CX_PASS='***' python3 scripts/cx_login.py --out ck.txt
"""
import argparse, base64, json, os, re, sys
from urllib.parse import unquote

LOGIN_PAGE = "https://passport2.chaoxing.com/login?fid=&refer=http%3A%2F%2Fi.chaoxing.com"
SUBMIT_URL = "https://passport2.chaoxing.com/fanyalogin"
REFER_FIELD = "http%3A%2F%2Fi.chaoxing.com"      # 与页面 hidden input 同值（jQuery 会再编码 %）
TRANSFER_KEY = "u2oh6Vu^HWe4_AES"             # login.js 里的 transferKey
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")
KEY_COOKIES = ["_uid", "_d", "vc3", "uf", "fid", "lv", "UID", "JSESSIONID"]


def aes_b64(msg: str, key: str) -> str:
    from cryptography.hazmat.primitives import padding as sympad
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    k = key.encode()
    pad = sympad.PKCS7(128).padder()
    data = pad.update(msg.encode()) + pad.finalize()
    enc = Cipher(algorithms.AES(k), modes.CBC(k)).encryptor()
    return base64.b64encode(enc.update(data) + enc.finalize()).decode()


def mask(s: str, keep: int = 0) -> str:
    if s is None:
        return "(none)"
    s = str(s)
    if len(s) <= keep:
        return "*" * len(s)
    return "*" * (len(s) - keep) + s[-keep:] if keep else "*" * 8 + f"({len(s)}B)"


def redact_jwt(obj):
    if not isinstance(obj, dict):
        return obj
    out = {}
    for k, v in obj.items():
        if k.lower() in ("pwd", "password", "uname", "name", "phone", "mobile", "email", "token"):
            out[k] = mask(v, 0) if k.lower() not in ("token",) else "<redacted>"
        elif k.lower() == "url" and isinstance(v, str):
            out[k] = re.sub(r"([?&](?:token|pwd|uid|_uid)=)[^&]*", r"\1<redacted>", v)
        else:
            out[k] = v
    return out


def cookie_header(jar) -> str:
    pairs, seen = [], set()
    for c in jar:
        if "chaoxing" in (c.domain or "") and c.name not in seen:
            seen.add(c.name)
            pairs.append(f"{c.name}={c.value}")
    return "; ".join(pairs)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--phone", default=os.environ.get("CX_PHONE", ""))
    ap.add_argument("--password", default=os.environ.get("CX_PASS", ""))
    ap.add_argument("--out", default="ck.txt", help="cookie 单行文本输出路径")
    ap.add_argument("--jar", default="ck.json", help="原始 cookie jar 输出路径（含过期信息）")
    a = ap.parse_args()
    if not a.phone or not a.password:
        print("[x] 需要 CX_PHONE / CX_PASS（或 --phone/--password）")
        return 2

    import requests
    s = requests.Session()
    s.headers.update({
        "User-Agent": UA,
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "X-Requested-With": "XMLHttpRequest",
        "Origin": "https://passport2.chaoxing.com",
        "Referer": LOGIN_PAGE,
    })
    # 1) 先落地 cookie（JSESSIONID/route），保持与浏览器一致的顺序
    r0 = s.get(LOGIN_PAGE, timeout=25)
    print(f"[1] 登录页 HTTP {r0.status_code}  cookies={[c.name for c in s.cookies]}")

    # 2) 提交（手机号与密码都用 AES-CBC 加密）
    data = {
        "fid": "-1",
        "uname": aes_b64(a.phone, TRANSFER_KEY),
        "password": aes_b64(a.password, TRANSFER_KEY),
        "refer": REFER_FIELD,
        "t": "true",
        "forbidotherlogin": "0",
        "validate": "",
        "doubleFactorLogin": "0",
        "independentId": "0",
        "independentNameId": "0",
    }
    r1 = s.post(SUBMIT_URL, data=data, timeout=30)
    print(f"[2] POST /fanyalogin HTTP {r1.status_code}")
    try:
        j = r1.json()
    except Exception:
        print("[!] 非 JSON 响应，前 300 字符：", r1.text[:300])
        return 3
    print("    响应字段：", json.dumps(redact_jwt(j), ensure_ascii=False)[:600])
    if not j.get("status"):
        msg = str(j.get("msg", ""))
        print(f"[x] 登录未成功：{msg}")
        if any(k in msg for k in ("验证码", "校验", "vcode", "次数")):
            print("    → 这是风控要求的人机校验；先别重试，把这条消息给我，我换路线（或你手动在浏览器过验证码后把 cookie 给我）。")
        return 4

    # 3) 跟着跳转把 .chaoxing.com 的会话 cookie 收全（任一步失败都不影响后续导出）
    target = unquote(str(j.get("url") or "https://i.chaoxing.com"))
    for u in (target, "https://i.chaoxing.com", "https://mooc1.chaoxing.com/",
              "https://mooc1-1.chaoxing.com/"):
        try:
            rr = s.get(u, timeout=30, allow_redirects=True)
            print(f"[3] GET {u[:48]} → HTTP {rr.status_code}")
        except Exception as e:
            print(f"    (忽略) {u[:48]} → {type(e).__name__}")

    hdr = cookie_header(s.cookies)
    names = sorted({c.name for c in s.cookies if "chaoxing" in (c.domain or "")})
    print(f"[4] 拿到 cookie {len(names)} 个：{names}")
    missing = [k for k in KEY_COOKIES if k not in names]
    print(f"    关键字段缺失：{missing if missing else '无'}")

    open(a.out, "w").write(hdr + "\n")
    try:
        open(a.jar, "w").write(json.dumps(
            [{"name": c.name, "value": c.value, "domain": c.domain, "path": c.path,
              "expires": c.expires} for c in s.cookies], ensure_ascii=False, indent=1))
    except Exception:
        pass
    print(f"[5] 已写入 {a.out}（{len(hdr)} B）与 {a.jar}")

    # 4) 立刻只读校验一次：未登录会 302 到 passport
    try:
        v = s.get("https://mooc1.chaoxing.com/visit/interaction", timeout=25, allow_redirects=False)
        tag = "已登录" if v.status_code == 200 else f"HTTP {v.status_code}（可能未登录）"
        print(f"[6] 只读校验 GET /visit/interaction → {tag}")
    except Exception as e:
        print("[6] 校验异常", type(e).__name__)
    return 0


if __name__ == "__main__":
    sys.exit(main())
