#!/usr/bin/env python3
"""Mine the readable string surface inside the sealed classes.dex; build the 学习通/签到 class + API map."""
import zipfile, re, collections, os

P = "samples/学习通.apk"
OUT = "chaoxing/out"
os.makedirs(OUT, exist_ok=True)
z = zipfile.ZipFile(P)

run = re.compile(rb"[\x20-\x7e]{5,400}")
desc = re.compile(rb"^L[A-Za-z0-9_$]+(?:/[A-Za-z0-9_$]+)+;?$")
sig = re.compile(rb"^\([A-Za-z0-9_$\[/;()]+\).+$")

total = 0
cx = collections.Counter()          # com/chaoxing descriptors
density = collections.Counter()     # offset bucket -> string bytes
apis = collections.Counter()
methods = collections.Counter()
fout = open(os.path.join(OUT, "classes_strings.txt"), "w")
dout = open(os.path.join(OUT, "cx_descriptors.txt"), "w")

with z.open("classes.dex") as f:
    off = 0
    while True:
        b = f.read(1 << 22)
        if not b: break
        for m in run.finditer(b):
            total += 1
            s = m.group()
            pos = off + m.start()
            density[pos // (1 << 20)] += len(s)
            fout.write(f"{pos}\t{s.decode('latin1')}\n")
            if desc.match(s):
                if s.startswith(b"Lcom/chaoxing") or s.startswith(b"Lcom/chaoxing/"):
                    cx[s.decode("latin1")] += 1
            low = s.lower()
            if b"/" in s and (b"ajax" in low or b"pptSign".lower() in low or s.startswith(b"/phone") or s.startswith(b"/apisign") or s.startswith(b"/mobilelearn") or s.startswith(b"/teacher") or s.startswith(b"/stu")):
                if b" " not in s and b"<" not in s and len(s) < 120:
                    apis[s.decode("latin1")] += 1
            if sig.match(s) and (b"Sign" in s or b"sign" in s):
                methods[s.decode("latin1")] += 1
        off += len(b)
fout.close()

for d in sorted(cx):
    dout.write(d + "\n")
dout.close()

print("=== total printable runs:", total)
print("=== read/write bytes per MB (whole-file density map, MB -> printable bytes)")
for k in sorted(density):
    if k % 8 == 0 or density[k] > 200000:
        print(f"   MB {k:>3} : {density[k]:>9}")
print("=== com/chaoxing descriptors:", len(cx))
namespaces = collections.Counter()
for d in cx:
    parts = d[1:].rstrip(";").split("/")
    namespaces["/".join(parts[:4])] += 1
for k, v in namespaces.most_common(30):
    print(f"   {v:>5}  {k}")
print("=== sign-module descriptors (full)")
signs = sorted(d for d in cx if re.search(r"/sign/|/sign$|/[Ss]ign[A-Z]|attendance|Attendance|/beacon/", d))
for d in signs:
    print("   ", d)
print("   count:", len(signs))
print("=== API-path-like strings:", len(apis))
with open(os.path.join(OUT, "api_paths.txt"), "w") as fh:
    for k, v in apis.most_common():
        fh.write(f"{v}\t{k}\n")
for k, v in apis.most_common(50):
    print(f"   {v:>4}  {k}")
print("=== sign-ish method signatures:", len(methods))
for k, v in methods.most_common(30):
    print(f"   {v:>4}  {k[:110]}")
