#!/usr/bin/env python3
import argparse, hashlib, os, sys, time, frida
PKG = "com.chaoxing.mobile"
HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_OUT = os.path.normpath(os.path.join(HERE, "..", "out", "dump"))
JS_PATH = os.path.join(HERE, "masquerade.js")
SEEN, SAVED = set(), []
OUT = DEFAULT_OUT
T0 = time.time()
def on_message(msg, data):
    if msg.get("type") == "send":
        p = msg.get("payload") or {}
        t = p.get("type")
        if t == "hb":
            print("  [hb %.1fs]" % (time.time() - T0), flush=True)
        elif t == "log":
            print("[js %5.1fs]" % (time.time() - T0), p.get("msg"), flush=True)
        elif t == "dex" and data:
            d = bytes(data); h = hashlib.sha256(d).hexdigest()
            if h in SEEN:
                print("[=] dup", h[:16], flush=True); return
            SEEN.add(h)
            name = p.get("name") or "dex"
            path = os.path.join(OUT, name + "_" + h[:8] + ".dex")
            open(path, "wb").write(d)
            SAVED.append(path)
            print("[+] saved %s  %d bytes  sha256=%s" % (path, len(d), h), flush=True)
        else:
            print("[js-msg]", p, flush=True)
    else:
        print("[frida-msg]", msg, flush=True)
def main():
    global OUT
    ap = argparse.ArgumentParser()
    ap.add_argument("--wait", type=float, default=14.0)
    ap.add_argument("--out", default=DEFAULT_OUT)
    ap.add_argument("--scan", action="store_true")
    ap.add_argument("--max", type=int, default=0x60000000)
    ap.add_argument("--min", type=int, default=0x1000)
    ap.add_argument("--resume-only", action="store_true")
    ap.add_argument("--post-wait", type=float, default=20.0)
    args = ap.parse_args()
    OUT = args.out
    os.makedirs(OUT, exist_ok=True)
    dev = frida.get_usb_device(timeout=10)
    pid = dev.spawn([PKG])
    print("[*] spawned pid", pid, flush=True)
    session = dev.attach(pid)
    detached = {}
    session.on("detached", lambda reason, crash=None: detached.update({"reason": reason, "crash": crash}))
    script = session.create_script(open(JS_PATH).read())
    script.on("message", on_message)
    script.load()
    dev.resume(pid)
    print("[*] resumed, waiting %.1fs" % args.wait, flush=True)
    time.sleep(args.wait)
    alive = True
    try:
        print("[*] protector modules:", script.exports_sync.info(), flush=True)
    except Exception as e:
        alive = False
        print("[!] script dead:", type(e).__name__, e, flush=True)
    if alive:
        try:
            print("[*] ping:", script.exports_sync.ping(), flush=True)
        except Exception as e:
            alive = False
            print("[!] ping failed:", e, flush=True)
    if detached:
        print("[!] detached:", detached, flush=True)
    if not alive:
        print("[!] app dead", flush=True)
        return 2
    if args.resume_only:
        time.sleep(args.post_wait)
        try:
            print("[*] alive after extra wait:", script.exports_sync.ping(), flush=True)
            print("[*] modules:", script.exports_sync.info(), flush=True)
        except Exception as e:
            print("[!] died later:", e, flush=True)
            if detached: print("[!] detached:", detached, flush=True)
            return 3
        return 0
    if args.scan:
        res = script.exports_sync.scan(args.min, args.max)
        print("[*] scan:", res["ranges"], "ranges", res["bytes"], "bytes,", len(res["cands"]), "candidates", flush=True)
        for i, c in enumerate(res["cands"]):
            print("    cand", i, c["base"], hex(c["size"]), flush=True)
            try:
                script.exports_sync.grab(c["base"], c["size"], "dex_%02d" % i); time.sleep(0.5)
            except Exception as e:
                print("    grab failed:", e, flush=True)
    print("[*] saved:", len(SAVED), flush=True)
    for s in SAVED: print("   ", s, flush=True)
    return 0
if __name__ == "__main__":
    sys.exit(main())
