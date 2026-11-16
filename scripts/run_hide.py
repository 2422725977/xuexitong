#!/usr/bin/env python3
"""run_hide.py — 用 frida spawn 学习通并注入 hide_env.js，观测能否越过启动自毁。
用法: python3 run_hide.py [--app com.chaoxing.mobile] [--script scripts/hide_env.js] [--seconds 30]
"""
import argparse, sys, time, os
import frida

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--app", default="com.chaoxing.mobile")
    ap.add_argument("--script", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "hide_env.js"))
    ap.add_argument("--seconds", type=float, default=30.0)
    ap.add_argument("--log", action="store_true")
    a = ap.parse_args()

    dev = frida.get_usb_device(timeout=10)
    pid = dev.spawn([a.app])
    print(f"[+] spawned pid={pid}", flush=True)
    session = dev.attach(pid)
    src = open(a.script, encoding="utf-8").read()
    if a.log:
        src = src.replace("log:false", "log:true")
    script = session.create_script(src)
    counts = {}
    def on_msg(msg, data):
        if msg.get("type") == "log":
            line = msg["payload"]
            key = line.split(" ")[0]
            counts[key] = counts.get(key, 0) + 1
            if counts[key] <= 40 or "hide" in key or "SANITIZE" in line:
                print("   ", line, flush=True)
        elif msg.get("type") == "error":
            print("[!]", msg.get("description"), flush=True)
    script.on("message", on_msg)
    script.load()
    print("[+] script loaded, resuming", flush=True)
    dev.resume(pid)
    t0 = time.time()
    alive_max = 0.0
    while time.time() - t0 < a.seconds:
        time.sleep(0.3)
        try:
            ps = {p.pid: p.name for p in dev.enumerate_processes()}
        except Exception:
            continue
        if pid in ps:
            alive_max = time.time() - t0
        elif alive_max and (time.time() - t0 - alive_max) > 3:
            break
    if alive_max > 0:
        print(f"[=] 进程存活 {alive_max:.1f}s（>3s 说明过了启动自毁）", flush=True)
    else:
        print("[=] 进程从未存活", flush=True)
    print("[=] 统计:", dict(sorted(counts.items(), key=lambda kv: -kv[1])[:12]), flush=True)
    try:
        session.detach()
    except Exception:
        pass

if __name__ == "__main__":
    main()
