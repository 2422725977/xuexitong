#!/usr/bin/env python3
"""Recover sign-request parameter constants near the sign code region."""
import zipfile, re, collections

P = "samples/学习通.apk"
z = zipfile.ZipFile(P)
data = z.read("classes.dex")
TOKENS = [b"rcode", b"ifTiJiao", b"clientip", b"latitude", b"longitude", b"address", b"appType=15", b"signType", b"getSign", b"signGps", b"enc=", b"activeId", b"generalSign", b"qrSign", b"faceSign", b"signCode"]
run = re.compile(rb"[\x20-\x7e]{4,200}")

for t in TOKENS:
    pos = [m.start() for m in re.finditer(re.escape(t), data)]
    print(f"--- {t.decode():<12} occurrences={len(pos)} first={pos[:5]}")
    for p in pos[:2]:
        a = max(0, p - 400); b = min(len(data), p + 400)
        win = data[a:b]
        strs = [m.group().decode("latin1") for m in run.finditer(win)]
        strs = [s for s in strs if len(s) >= 5][:14]
        print("     ctx:", " | ".join(strs))
