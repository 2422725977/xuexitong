#!/usr/bin/env python3
"""Extract the readable class/string surface from the sealed classes.dex, focused on the sign module."""
import zipfile, re, collections, json, os

P = "samples/学习通.apk"
OUT = "chaoxing/out"
os.makedirs(OUT, exist_ok=True)
z = zipfile.ZipFile(P)

desc = re.compile(rb"L(?:com|cn|org)/[A-Za-z0-9_$]*(?:/[A-Za-z0-9_$]+)*;")
url = re.compile(rb"https?://[A-Za-z0-9._~:/?#\[\]@!$&'()*+,;=%-]{6,200}")
paths = re.compile(rb"/(?:apisign|pptSign|stuSignajax|sign|signin|attend|checkin|mobilelearn|phone)[A-Za-z0-9_/.?=&%-]{0,80}", re.I)

classes = collections.Counter()
urls = collections.Counter()
ppath = collections.Counter()
strs_sign = collections.Counter()

with z.open("classes.dex") as f:
    buf = b""
    while True:
        b = f.read(1 << 22)
        if not b: break
        win = buf[-256:] + b
        for m in desc.findall(win):
            classes[m.decode("latin1")] += 1
        for m in url.findall(win):
            try:
                urls[m.decode("utf-8")] += 1
            except Exception:
                pass
        for m in paths.findall(win):
            ppath[m.decode("latin1")] += 1
        for m in re.findall(rb"[\x20-\x7e]{5,120}", win):
            low = m.lower()
            if b"sign" in low or b"attend" in low or b"checkin" in low or b"qiandao" in low:
                strs_sign[m.decode("latin1")] += 1
        buf = b

def save(name, counter, minc=1):
    with open(os.path.join(OUT, name), "w") as fh:
        for k, v in counter.most_common():
            if v >= minc:
                fh.write(f"{v}\t{k}\n")
    print(f"   wrote {name}: {len(counter)} unique")

print("=== readable class descriptors:", len(classes))
save("classes_readable.txt", classes)
top = collections.Counter()
for d in classes:
    parts = d[1:].split("/")
    top["/".join(parts[:3])] += 1
print("   top namespaces:")
for k, v in top.most_common(25):
    print(f"     {v:>5}  {k}")

print("=== sign/attendance-related classes (full)")
sign_cls = sorted(d for d in classes if re.search(r"sign|attend|checkin|qiandao", d, re.I))
for d in sign_cls:
    print("   ", d)
print("   total:", len(sign_cls))

print("=== URLs:", len(urls))
save("urls_readable.txt", urls)
dom = collections.Counter()
for u in urls:
    m = re.match(r"https?://([^/]+)", u)
    if m: dom[m.group(1)] += 1
for k, v in dom.most_common(25):
    print(f"   {v:>5}  {k}")

print("=== sign-ish paths:", len(ppath))
save("paths_signish.txt", ppath)
for k, v in ppath.most_common(30):
    print(f"   {v:>5}  {k}")

print("=== printable strings containing sign/attend/checkin:", len(strs_sign))
save("strings_signish.txt", strs_sign)
for k, v in strs_sign.most_common(40):
    print(f"   {v:>4}  {k[:120]}")
