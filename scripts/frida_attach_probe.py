import frida, sys, time, json, subprocess
ADB="/opt/homebrew/share/android-commandlinetools/platform-tools/adb"
ck=open("ck.txt").read().strip()
js=open("scripts/frida_app_probe.js").read().replace("__COOKIE__", json.dumps(ck))
subprocess.run([ADB,"shell","am","force-stop","com.chaoxing.mobile"],capture_output=True)
subprocess.run([ADB,"shell","monkey","-p","com.chaoxing.mobile","-c","android.intent.category.LAUNCHER","1"],capture_output=True)
time.sleep(8)
p=subprocess.run([ADB,"shell","ps","-A"],capture_output=True,text=True).stdout
alive=[l for l in p.splitlines() if "chaoxing" in l]
print("进程:", alive[:2])
if not alive:
    print("App 未存活（可能被 anti-frida/加固杀掉）"); sys.exit(0)
dev=frida.get_usb_device()
try:
    sess=dev.attach("com.chaoxing.mobile"); print("attach OK")
except Exception as e:
    print("attach 失败:",e); sys.exit(1)
scr=sess.create_script(js)
def on_msg(m,d):
    try: print("[MSG]", json.dumps(m, ensure_ascii=False)[:300], flush=True)
    except Exception: print("[MSG]", str(m)[:300], flush=True)
scr.on("message", on_msg)
scr.load()
print("loaded, 观察 20s")
time.sleep(20)
p=subprocess.run([ADB,"shell","ps","-A"],capture_output=True,text=True).stdout
print("20s 后是否存活:", any("chaoxing" in l for l in p.splitlines()))
