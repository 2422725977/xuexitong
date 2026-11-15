#!/usr/bin/env python3
"""Inspect the unsealed H5 schedule/attendance bundle inside assets."""
import zipfile, re
P = "samples/\u5b66\u4e60\u901a.apk"
z = zipfile.ZipFile(P)
names = [n for n in z.namelist() if n.startswith("assets/schedule")]
print("=== assets/schedule entries:", len(names))
for n in sorted(names):
    print(f"   {z.getinfo(n).file_size:9d}  {n}")
tgt = "assets/schedule/js/schedule.js"
d = z.read(tgt).decode("utf-8", "replace")
print()
print(f"=== {tgt}: {len(d)} chars")
for kw in ["attendance", "\u7b7e\u5230", "sign", "mobilelearn", "rcode", "activeId", "punch"]:
    idx = [m.start() for m in re.finditer(re.escape(kw), d, re.I)][:6]
    print(f"   {kw}: {len(re.findall(re.escape(kw), d, re.I))} hits, first offsets {idx}")
print()
print("=== urls inside schedule.js")
u = sorted(set(re.findall(r"https?://[A-Za-z0-9._~:/?#\[\]@!$&'()*+,;=%*\-]{6,200}", d)))
print("   distinct:", len(u))
for x in u[:60]:
    print("   ", x[:160])
print()
print("=== attendance context samples")
for m in list(re.finditer("attendance", d, re.I))[:12]:
    s = max(0, m.start() - 120); print("   ...", d[s:m.start() + 160].replace("\n", " ")[:290])
