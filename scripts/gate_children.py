import frida, sys, time, json, os, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
JS = open(os.path.join(HERE, 'probe_env2.js')).read()
PKG = 'com.chaoxing.mobile'
SESS = []

def show(msg, data):
    if msg.get('type') == 'send':
        p = msg.get('payload') or {}
        if isinstance(p, dict) and p.get('t') == 'hook':
            return
        print(json.dumps(p, ensure_ascii=False)[:400], flush=True)
    else:
        print('ERRMSG', str(msg)[:300], flush=True)

dev = frida.get_usb_device(timeout=15)
print('device', dev, flush=True)
dev.enable_spawn_gating()
print('spawn gating enabled', flush=True)

def load(sess, tag):
    try:
        s = sess.create_script(JS)
        s.on('message', show)
        s.load()
        SESS.append(s)
        print('[script loaded %s %s]' % (tag, sess), flush=True)
    except Exception as e:
        print('script err', tag, e, flush=True)

def on_child(child):
    print('[CHILD ADDED pid=%s]' % child.pid, flush=True)
    try:
        load(dev.attach(child.pid), 'child')
    except Exception as e:
        print('child attach err', e, flush=True)
    try:
        dev.resume(child.pid)
        print('[child %s resumed]' % child.pid, flush=True)
    except Exception as e:
        print('child resume err', e, flush=True)

def on_child_removed(child):
    print('[CHILD REMOVED pid=%s reason=%s]' % (child.pid, getattr(child, 'reason', '?')), flush=True)

dev.on('child-added', on_child)
try:
    dev.on('child-removed', on_child_removed)
except Exception as e:
    print('no child-removed signal', e, flush=True)

pid = dev.spawn([PKG])
print('spawned pid', pid, flush=True)
load(dev.attach(pid), 'main')
dev.resume(pid)
for i in range(12):
    time.sleep(1)
    r = subprocess.run(['adb','shell','pidof',PKG], capture_output=True, text=True)
    print('t+%d alive=%r' % (i+1, r.stdout.strip()), flush=True)
print('done', flush=True)
