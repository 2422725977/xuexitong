import frida, sys, time, json
ck=open("ck.txt").read().strip()
js=open("scripts/frida_app_probe.js").read().replace("__COOKIE__", json.dumps(ck))
dev=frida.get_usb_device()
try:
    pid=dev.spawn(["com.chaoxing.mobile"]); mode="spawn"
except Exception as e:
    print("spawn 失败:",e); sys.exit(1)
print("spawned pid",pid)
sess=dev.attach(pid); scr=sess.create_script(js)
scr.on("message", lambda m,d: print("[JS]",str(m.get("payload") if isinstance(m,dict) else m)[:300], flush=True))
scr.load(); dev.resume(pid)
time.sleep(30)
try: dev.kill(pid)
except Exception: pass
print("done")