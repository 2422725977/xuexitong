#!/usr/bin/env python3
"""Consolidated signin evidence: single-pass keyword census, payload chinese/identifier harvest, descriptor counts."""
import zipfile, re, collections

P = "samples/学习通.apk"
z = zipfile.ZipFile(P)
KW = ["\u7b7e\u5230", "rcode", "activeId", "signType", "ifTiJiao", "clientip", "latitude", "longitude", "beacon", "bluetooth", "checkin", "attendance"]
res = {k: [0, 0, []] for k in KW}
for info in z.infolist():
    if info.filename.endswith("/") or info.file_size > 6_000_000:
        continue
    try:
        d = z.read(info.filename)
    except Exception:
        continue
    for k in KW:
        c = d.count(k.encode("utf-8")) if not k.isascii() else d.count(k.encode())
        if c:
            res[k][0] += 1; res[k][1] += c
            if len(res[k][2]) < 4:
                res[k][2].append(info.filename)
print("=== keyword census (entries <6MB)")
for k, v in res.items():
    print(f"  {k:12s} files={v[0]:4d} hits={v[1]:6d}  {v[2]}")

data = z.read("classes.dex")
print()
print("=== Chinese strings containing signin keyword in readable payload")
pat = ("[^\x00-\x1f]{0,30}\u7b7e\u5230[^\x00-\x1f]{0,40}").encode("utf-8").decode("unicode_escape").encode("latin1")
seen = []
for m in re.finditer(pat, data):
    try:
        s = m.group().decode("utf-8")
    except Exception:
        continue
    if len(s) >= 4 and s not in seen:
        seen.append(s)
for s in seen[:60]:
    print("   ", s[:90])
print("   distinct:", len(seen))

print()
print("=== identifiers containing 'sign' in payload")
c = collections.Counter()
for m in re.finditer(rb"[A-Za-z_$][A-Za-z0-9_$]{2,30}", data):
    s = m.group().decode("latin1")
    if "sign" in s.lower():
        c[s] += 1
print("   distinct:", len(c))
for k, v in c.most_common(40):
    print(f"   x{v:4d}  {k}")

print()
print("=== descriptor counts")
t = open("chaoxing/out/classes_readable.txt", encoding="utf-8", errors="replace").read().split()
print("   total:", len(t))
for p in ["com/chaoxing/mobile/sign", "com/chaoxing/mobile/office", "com/chaoxing/beacon", "ttendance", "unch", "iFi", "luetooth"]:
    print(f"   {p:28s} {sum(1 for x in t if p in x)}")
