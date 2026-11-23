#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从本机 Chromium 系浏览器（Chrome / Edge / Brave）掏 chaoxing cookie → mooc.txt。

用途：刷网课需要 mooc 域会话；最省事的是「用户自己浏览器已经登录过 chaoxing」，
直接复用那份 cookie，不新增设备、不碰手机。

macOS 上 Chromium 的 cookie 值用 AES-128-CBC 加密，密钥存在钥匙串
（"<Browser> Safe Storage"），解密算法：
    key = PBKDF2-HMAC-SHA1(safestorage_pw, b"saltysalt", 1003, 16)
    明文 = AES-128-CBC(key, iv=b" "*16).decrypt(v10 密文去掉前 3 字节)
第一次读钥匙串 macOS 会弹一次授权框（只弹这一次）。

用法：
  python3 scripts/browser_cookie_lift.py --browser edge --out mooc.txt
  python3 scripts/browser_cookie_lift.py --list          # 只列有哪些库、各有多少 chaoxing cookie
  python3 scripts/browser_cookie_lift.py --selftest
"""
import argparse, glob, hashlib, os, shutil, sqlite3, subprocess, sys, tempfile

THIRD = ("chaoxing.com", "cldisk.com", "chaoxing.cn")
BROWSERS = {
    "chrome": ("Google/Chrome", "Chrome Safe Storage"),
    "edge": ("Microsoft Edge", "Microsoft Edge Safe Storage"),
    "brave": ("BraveSoftware/Brave-Browser", "Brave Safe Storage"),
}
KEYS = ["_uid", "UID", "vc3", "fid", "_d", "uf", "lv", "JSESSIONID"]


def db_paths(browser):
    base = os.path.expanduser(f"~/Library/Application Support/{BROWSERS[browser][0]}")
    return sorted(glob.glob(os.path.join(base, "*", "Cookies")))


def safe_storage_key(browser, timeout=25):
    """读钥匙串拿 Safe Storage 口令；拿不到就返回 None（可能被拒/不存在）。"""
    svc = BROWSERS[browser][1]
    try:
        p = subprocess.run(["security", "find-generic-password", "-wa", svc],
                           capture_output=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        print(f"[!] 读取钥匙串超时（{svc}）—— 可能有个授权弹窗在等你点「允许」。")
        return None
    if p.returncode != 0:
        print(f"[!] 钥匙串里没有 {svc}：{p.stderr.decode('utf-8','ignore').strip()[:120]}")
        return None
    return p.stdout.strip().decode("utf-8", "ignore").strip()


def decrypt_value(enc, pw):
    if not enc:
        return ""
    if enc[:3] not in (b"v10", b"v11"):
        return enc.decode("utf-8", "ignore")
    try:
        from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    except Exception as e:
        print(f"[!] 缺 cryptography，无法解密：{e}")
        return ""
    key = hashlib.pbkdf2_hmac("sha1", pw.encode(), b"saltysalt", 1003, 16)
    dec = Cipher(algorithms.AES(key), modes.CBC(b" " * 16)).decryptor()
    raw = dec.update(enc[3:]) + dec.finalize()
    # 去 PKCS7 填充
    if raw:
        n = raw[-1]
        if 1 <= n <= 16 and raw[-n:] == bytes([n]) * n:
            raw = raw[:-n]
    return raw.decode("utf-8", "ignore")


def read_db(path, pw):
    tmp = os.path.join(tempfile.mkdtemp(prefix="bclift_"), "c.db")
    shutil.copy2(path, tmp)
    con = sqlite3.connect(tmp)
    con.row_factory = sqlite3.Row
    rows = con.execute("SELECT host_key,name,value,encrypted_value,path,is_secure,is_httponly "
                       "FROM cookies WHERE host_key LIKE '%chaoxing%'").fetchall()
    out, enc_cnt = [], 0
    for r in rows:
        v = r["value"] if "value" in r.keys() else ""
        if not v:
            ev = bytes(r["encrypted_value"] or b"")
            if ev:
                enc_cnt += 1
                v = decrypt_value(ev, pw) if pw else ""
        if not v:
            continue
        out.append({"host": r["host_key"], "name": r["name"], "value": v,
                    "path": r["path"] or "/", "secure": bool(r["is_secure"]),
                    "httponly": bool(r["is_httponly"])})
    con.close()
    return out, enc_cnt


def to_netscape(cookies, path):
    lines = ["# Netscape HTTP Cookie File", "# browser_cookie_lift.py"]
    for c in sorted(cookies, key=lambda x: (x["host"], x["name"])):
        dom = c["host"] if c["host"].startswith(".") else c["host"]
        flag = "TRUE" if dom.startswith(".") else "FALSE"
        lines.append("\t".join([dom, flag, c["path"], "TRUE" if c["secure"] else "FALSE",
                                 "0", c["name"], c["value"]]))
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    return len(cookies)


def brief(cookies):
    idx = {}
    for c in cookies:
        idx.setdefault(c["name"], c["value"])
    print(f"[=] chaoxing cookie {len(cookies)} 条")
    for k in KEYS:
        v = idx.get(k)
        if v:
            print(f"    {k:<11} {v if len(v) <= 16 else v[:10] + '…'}")
    return idx


def selftest():
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    pw = "dummy-pw"
    key = hashlib.pbkdf2_hmac("sha1", pw.encode(), b"saltysalt", 1003, 16)
    msg = b"verysecret-value" + bytes([16]) * 16  # 内容正好 16 字节 → 整块填充
    enc = Cipher(algorithms.AES(key), modes.CBC(b" " * 16)).encryptor()
    ct = b"v10" + enc.update(msg) + enc.finalize()
    got = decrypt_value(ct, pw)
    assert got == "verysecret-value", repr(got)
    tmp = tempfile.mkdtemp()
    db = os.path.join(tmp, "c.db")
    con = sqlite3.connect(db)
    con.execute("CREATE TABLE cookies (host_key TEXT,name TEXT,value TEXT,encrypted_value BLOB,"
                "path TEXT,is_secure INT,is_httponly INT)")
    con.execute("INSERT INTO cookies VALUES (?,?,?,?,?,?,?)",
                (".chaoxing.com", "_uid", "9999", b"", "/", 1, 1))
    con.execute("INSERT INTO cookies VALUES (?,?,?,?,?,?,?)",
                (".chaoxing.com", "vc3", "", ct, "/", 1, 1))
    con.execute("INSERT INTO cookies VALUES (?,?,?,?,?,?,?)",
                (".baidu.com", "x", "y", b"", "/", 0, 0))
    con.commit(); con.close()
    cs, e = read_db(db, pw)
    assert len(cs) == 2 and e == 1, (cs, e)
    ns = os.path.join(tmp, "n.txt")
    assert to_netscape(cs, ns) == 2
    body = open(ns, encoding="utf-8").read()
    assert "_uid\t9999" in body and "vc3\tverysecret-value" in body, body
    print("[+] selftest PASS（keychain 解密 / 过滤 / Netscape 输出）")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--browser", choices=list(BROWSERS), default="edge")
    ap.add_argument("--out", default="mooc.txt")
    ap.add_argument("--header", default="mooc.txt.hdr")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if a.list:
        for b in BROWSERS:
            for p in db_paths(b):
                try:
                    con = sqlite3.connect("file:" + p + "?mode=ro", uri=True)
                    n = con.execute("SELECT count(*) FROM cookies").fetchone()[0]
                    c = con.execute("SELECT count(*) FROM cookies WHERE host_key LIKE '%chaoxing%'").fetchone()[0]
                    print(f"{b:<7} {p}  总 {n} / chaoxing {c}")
                except Exception as e:
                    print(f"{b:<7} {p}  打不开：{e}")
        return 0
    paths = db_paths(a.browser)
    if not paths:
        print(f"[x] 没找到 {a.browser} 的 cookie 库")
        return 2
    pw = safe_storage_key(a.browser)
    best, bp = [], None
    for p in paths:
        try:
            cs, e = read_db(p, pw)
        except Exception as ex:
            print(f"[!] {p} 读取失败：{ex}")
            continue
        print(f"[=] {p}: chaoxing {len(cs)} 条（加密 {e}）")
        if len(cs) > len(best):
            best, bp = cs, p
    if not best:
        print("[x] 没有可用的 chaoxing cookie —— 请先在这个浏览器里登录 chaoxing.com 再跑本脚本。")
        return 3
    idx = brief(best)
    n = to_netscape(best, a.out)
    with open(a.header, "w", encoding="utf-8") as f:
        f.write("; ".join(f"{k}={v}" for k, v in idx.items()))
    print(f"[+] 写入 {a.out}（{n} 条，来自 {bp}）")
    if not idx.get("fid"):
        print("[!] 没有 fid —— 登录可能没成功（匿名访问也会留下 JSESSIONID）。")
    else:
        print(f"[+] fid={idx['fid']} → python3 scripts/import_curl.py {a.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
