#!/usr/bin/env python3
"""Window dump around the sign-in endpoints: recover nearby string-pool constants."""
import zipfile, re, sys

P = "samples/学习通.apk"
z = zipfile.ZipFile(P)
MARKERS = [b"newsign/studentSign", b"sign/produceSignView", b"pptSign/gotasksign", b"widget/sign/api/findPuidsByActiveId", b"getSign"]
run = re.compile(rb"[\x20-\x7e]{4,200}")

data = b""
with z.open("classes.dex") as f:
    data = f.read()

print("file bytes:", len(data))
for mk in MARKERS:
    pos = data.find(mk)
    print("=" * 70)
    print("MARKER", mk.decode(), "at", pos)
    if pos < 0:
        continue
    a = max(0, pos - 2500); b = min(len(data), pos + 1200)
    win = data[a:b]
    seen = set()
    for m in run.finditer(win):
        s = m.group().decode("latin1")
        if s in seen: continue
        seen.add(s)
        if len(s) < 5: continue
        print(f"   [{a + m.start():>10}] {s[:190]}")
