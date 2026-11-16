#!/usr/bin/env python3
"""run_frida.py —— 经 adb forward 连模拟器上的 frida-server，spawn 目标 App，注入一或多个脚本。"""
import argparse, os, subprocess, sys, time
import frida

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--serial", default="emulator-5554")
    ap.add_argument("--app", default="com.chaoxing.mobile")
    ap.add_argument("--script", required=True, action="append", dest="scripts")
    ap.add_argument("--seconds", type=float, default=40.0)
    ap.add_argument("--port", type=int, default=27042)
    a = ap.parse_args()
    subprocess.run(["adb", "-s", a.serial, "forward", "tcp:%d" % a.port, "tcp:27042"], check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    dev = frida.get_device_manager().add_remote_device("127.0.0.1:%d" % a.port)
    pid = dev.spawn([a.app])
    print("[+] spawned pid=%d" % pid, flush=True)
    session = dev.attach(pid)
    def on_msg(m, data):
        if m.get("type") == "send":
            print("[send] " + str(m.get("payload"))[:6000], flush=True)
        elif m.get("type") == "log":
            print("[log] " + str(m.get("payload"))[:800], flush=True)
        elif m.get("type") == "error":
            print("[!] " + str(m.get("description"))[:1000], flush=True)
    scripts = []
    for p in a.scripts:
        try:
            s = session.create_script(open(p, encoding="utf-8").read())
            s.on("message", on_msg)
            s.load()
            scripts.append((p, s))
            print("[+] loaded " + os.path.basename(p), flush=True)
        except Exception as e:
            print("[!] load fail %s: %s" % (p, e), flush=True)
    print("[+] resume", flush=True)
    dev.resume(pid)
    t0 = time.time(); alive = 0.0
    while time.time() - t0 < a.seconds:
        time.sleep(0.3)
        try:
            ps = {p.pid: p.name for p in dev.enumerate_processes()}
        except Exception:
            continue
        if pid in ps:
            alive = time.time() - t0
        elif alive and (time.time() - t0 - alive) > 4:
            break
    print("[=] 存活 %.1fs" % alive, flush=True)
    for p, s in scripts:
        try: s.unload()
        except Exception: pass
    try: session.detach()
    except Exception: pass

if __name__ == "__main__":
    main()
