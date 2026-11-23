#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""用「电脑浏览器」拿学习通的 mooc 域会话 —— 不碰手机、不碰钥匙串。

思路：起一个独立 Chrome 配置目录 + DevTools 协议（CDP）端口，你在那个窗口里正常登录
学习通；浏览器已经把 cookie 解密好了，CDP 的 Network.getAllCookies 直接给明文，
绕过「cookie 库是 v10 加密、钥匙串里没有 Safe Storage 密钥」这个死结。

顺带好处：这个配置目录是专用的（默认 ~/.cx_browser），不污染你平时的浏览器；
以后风控要复查、要手动看页面，复用同一份会话即可。

用法：
  python3 scripts/cdp_login_capture.py --launch-only      # 只开窗口（登录页）
  python3 scripts/cdp_login_capture.py --watch            # 轮询直到登录成功并落盘
  python3 scripts/cdp_login_capture.py --once             # 立刻导一次当前 cookie
  python3 scripts/cdp_login_capture.py --selftest
"""
import argparse, json, os, re, subprocess, sys, time, urllib.request

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
LOGIN_URL = "https://passport2.chaoxing.com/login?fid=&referer=https%3A%2F%2Fi.chaoxing.com"
THIRD = ("chaoxing.com", "cldisk.com", "chaoxing.cn")
KEYS = ["_uid", "UID", "vc3", "fid", "_d", "uf", "lv", "JSESSIONID"]
DEFAULT_PROFILE = os.path.expanduser("~/.cx_browser")


def jget(url, timeout=5):
    with urllib.request.urlopen(url, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8", "ignore"))


class CDP(object):
    def __init__(self, ws_url):
        import websocket
        self.ws = websocket.create_connection(ws_url, timeout=20)
        self.n = 0

    def call(self, method, params=None, timeout=20):
        self.n += 1
        mid = self.n
        self.ws.send(json.dumps({"id": mid, "method": method, "params": params or {}}))
        end = time.time() + timeout
        while time.time() < end:
            try:
                msg = json.loads(self.ws.recv())
            except Exception:
                break
            if msg.get("id") == mid:
                if "error" in msg:
                    raise RuntimeError(msg["error"])
                return msg.get("result", {})
        raise TimeoutError("%s 无响应" % method)

    def close(self):
        try:
            self.ws.close()
        except Exception:
            pass


def cdp_up(port):
    try:
        return jget("http://127.0.0.1:%d/json/version" % port)
    except Exception:
        return None


def launch(port, profile, url=LOGIN_URL, extra=()):
    os.makedirs(profile, exist_ok=True)
    cmd = [CHROME, "--remote-debugging-port=%d" % port, "--user-data-dir=" + profile,
           "--no-first-run", "--no-default-browser-check", "--restore-last-session=false",
           "--disable-features=Translate", url] + list(extra)
    p = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for _ in range(30):
        time.sleep(1)
        v = cdp_up(port)
        if v:
            return p, v
    return p, None


def _browse_ws(port):
    v = cdp_up(port)
    if not v:
        raise RuntimeError("CDP 没起来（端口 %d）" % port)
    return v["webSocketDebuggerUrl"]


def _page_ws(port):
    for t in jget("http://127.0.0.1:%d/json/list" % port):
        if t.get("type") == "page" and t.get("webSocketDebuggerUrl"):
            return t["webSocketDebuggerUrl"]
    return None


def all_cookies(port):
    """Chrome 较新版本里 Network.getAllCookies 只在页面会话可用；浏览器级用 Storage.getCookies。"""
    errs = []
    cands = [("Storage.getCookies", _browse_ws(port))]
    pw = _page_ws(port)
    if pw:
        cands.append(("Network.getAllCookies", pw))
    for meth, ws in cands:
        c = None
        try:
            c = CDP(ws)
            res = c.call(meth)
            if "cookies" in res:
                return res["cookies"]
            errs.append("%s: 无 cookies 字段" % meth)
        except Exception as e:
            errs.append("%s: %s" % (meth, e))
        finally:
            if c:
                c.close()
    raise RuntimeError("取 cookie 失败 —— " + " | ".join(errs))


def pick(cookies):
    return [c for c in cookies if any(t in c.get("domain", "") for t in THIRD)]


def brief(cookies):
    idx = {}
    for c in cookies:
        idx.setdefault(c["name"], c["value"])
    print("[=] chaoxing cookie %d 条" % len(cookies))
    for k in KEYS:
        v = idx.get(k)
        print("    %-11s %s" % (k, (v[:12] + "…") if v and len(v) > 12 else (v or "-")))
    return idx


def logged_in(idx):
    return bool(idx.get("_uid") or idx.get("UID")) and bool(idx.get("vc3"))


def to_netscape(cookies, path):
    lines = ["# Netscape HTTP Cookie File", "# cdp_login_capture.py"]
    for c in sorted(cookies, key=lambda x: (x["domain"], x["name"])):
        dom = c["domain"] or ""
        flag = "TRUE" if dom.startswith(".") else "FALSE"
        sec = "TRUE" if c.get("secure") else "FALSE"
        lines.append("\t".join([dom, flag, c.get("path") or "/", sec, "0",
                                c["name"], c["value"]]))
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    return len(cookies)


def save(cookies, out, json_out):
    n = to_netscape(cookies, out)
    with open(json_out, "w", encoding="utf-8") as f:
        json.dump(cookies, f, ensure_ascii=False, indent=1)
    return n


def selftest():
    cs = [
        {"domain": ".chaoxing.com", "name": "_uid", "value": "123", "path": "/", "secure": True},
        {"domain": ".chaoxing.com", "name": "vc3", "value": "abc", "path": "/", "secure": True},
        {"domain": "mooc1.chaoxing.com", "name": "JSESSIONID", "value": "XY", "path": "/", "secure": False},
        {"domain": ".example.com", "name": "nope", "value": "1", "path": "/", "secure": False},
    ]
    mine = pick(cs)
    assert len(mine) == 3, mine
    idx = brief(mine)
    assert logged_in(idx) is True
    assert brief(pick(cs[:1])) and logged_in(brief(pick(cs[:1]))) is False
    p = "/tmp/cdp_test_cookies.txt"
    assert save(mine, p, "/tmp/cdp_test_cookies.json") == 3
    body = open(p, encoding="utf-8").read()
    assert "\n.chaoxing.com\tTRUE\t/\tTRUE\t0\t_uid\t123" in body, body
    assert "\nmooc1.chaoxing.com\tFALSE\t/\tFALSE\t0\tJSESSIONID\tXY" in body, body
    print("[+] selftest PASS（过滤 / 登录判定 / Netscape 输出）")
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=9222)
    ap.add_argument("--profile", default=DEFAULT_PROFILE)
    ap.add_argument("--out", default="mooc.txt")
    ap.add_argument("--json-out", default="mooc_cookies.json")
    ap.add_argument("--launch-only", action="store_true")
    ap.add_argument("--watch", action="store_true")
    ap.add_argument("--once", action="store_true")
    ap.add_argument("--interval", type=int, default=5)
    ap.add_argument("--timeout", type=int, default=600)
    ap.add_argument("--visit-mooc", action="store_true", default=True,
                    help="登录后顺带访问 mooc1.chaoxing.com 让该域落 cookie")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()

    v = cdp_up(a.port)
    if v:
        print("[=] CDP 已在 %d：%s" % (a.port, v.get("Browser", "")[:60]))
        if a.once:
            cs = pick(all_cookies(a.port))
            idx = brief(cs)
            save(cs, a.out, a.json_out)
            print("[+] 写入 %s / %s" % (a.out, a.json_out))
            return 0 if logged_in(idx) else 5
    else:
        print("[=] 启动 Chrome（独立配置目录 %s，端口 %d）…" % (a.profile, a.port))
        p, v = launch(a.port, a.profile)
        if not v:
            print("[x] Chrome 没起来，检查是否已有同配置目录的实例在跑")
            return 2
        print("[+] Chrome OK：%s" % v.get("Browser", "")[:60])
        if a.launch_only:
            print("[=] 窗口里登录学习通（手机号/密码/扫码都行）。登录完回我一句，或让我 --watch。")
            return 0

    last = None
    t0 = time.time()
    print("[=] 开始轮询 cookie（每 %ds，最长 %ds）—— 请在窗口里完成登录…" % (a.interval, a.timeout))
    while time.time() - t0 < a.timeout:
        cs = pick(all_cookies(a.port))
        idx = {c["name"]: c["value"] for c in cs}
        sig = (idx.get("_uid"), idx.get("vc3"))
        if sig != last:
            print("[%s] cookie=%d _uid=%s vc3=%s fid=%s" %
                  (time.strftime("%H:%M:%S"), len(cs), (idx.get("_uid") or "-")[:8],
                   (idx.get("vc3") or "-")[:6] + ("…" if idx.get("vc3") else ""),
                   idx.get("fid") or "-"))
            last = sig
        if logged_in(idx):
            if a.visit_mooc:
                try:
                    tg = [x for x in jget("http://127.0.0.1:%d/json/list" % a.port)
                          if x.get("type") == "page"]
                    if tg:
                        c = CDP(tg[0]["webSocketDebuggerUrl"])
                        c.call("Page.navigate", {"url": "https://mooc1.chaoxing.com/"})
                        time.sleep(4)
                        c.close()
                        cs = pick(all_cookies(a.port))
                except Exception as e:
                    print("[!] 访问 mooc1 时出错（不影响导出）：%s" % e)
            idx = brief(cs)
            n = save(cs, a.out, a.json_out)
            print("[+] 登录成功，写入 %s（%d 条）、%s" % (a.out, n, a.json_out))
            if not idx.get("fid") or idx.get("fid") in ("0", ""):
                print("[!] fid 空/0 —— 这个账号没绑学校单位，mooc1 仍会 302；换学校账号登录。")
            else:
                print("[+] fid=%s → 下一步：python3 scripts/import_curl.py %s" % (idx["fid"], a.out))
            return 0
        time.sleep(a.interval)
    print("[x] 超时（%ds）还没登进去" % a.timeout)
    return 3


if __name__ == "__main__":
    sys.exit(main())
