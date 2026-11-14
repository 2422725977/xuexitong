#!/usr/bin/env python3
"""Hunt the 签到/attendance surface across every readable entry of the APK."""
import zipfile, re, collections, sys

P = "samples/学习通.apk"
z = zipfile.ZipFile(P)

KW = {
 "zh_signin": re.compile("签到".encode("utf-8")),
 "zh_qr": re.compile("二维码".encode("utf-8")),
 "zh_gesture": re.compile("手势".encode("utf-8")),
 "zh_loc": re.compile("位置签到".encode("utf-8")),
 "qiandao": re.compile(rb"qiandao", re.I),
 "signin": re.compile(rb"sign[_]?in", re.I),
 "checkin": re.compile(rb"check[_]?in", re.I),
 "attendance": re.compile(rb"attendance", re.I),
 "signact": re.compile(rb"signactiv|signActivity|attendActivity|signinactivity", re.I),
}

hits = collections.defaultdict(lambda: collections.Counter())
samples = collections.defaultdict(list)
files = collections.defaultdict(set)

for info in z.infolist():
    if info.is_dir() or info.file_size == 0:
        continue
    name = info.filename
    if info.file_size > 30 * 1024 * 1024:
        cap = 30 * 1024 * 1024
    else:
        cap = info.file_size
    try:
        with z.open(info) as f:
            data = f.read(cap)
    except Exception:
        continue
    for k, rx in KW.items():
        n = len(rx.findall(data))
        if n:
            hits[k][name] += n
            files[k].add(name)
            if len(samples[k]) < 6:
                m = rx.search(data)
                a = max(0, m.start() - 40); b = min(len(data), m.end() + 60)
                try:
                    snip = data[a:b].decode("utf-8", "replace")
                except Exception:
                    snip = repr(data[a:b])
                samples[k].append((name, snip.replace("\n", " ")[:140]))

print("=== keyword -> files")
for k in KW:
    print(f"  {k:<12} files={len(files[k]):<6} totalHits={sum(hits[k].values())}")
print()
for k in KW:
    if not files[k]:
        continue
    print(f"=== {k} top files")
    for name, n in hits[k].most_common(12):
        print(f"   {n:>7}  {name}")
    print(f"--- {k} samples")
    for name, s in samples[k]:
        print(f"   [{name}] {s}")
    print()

print("=== classes.dex: readable class descriptors matching sign/attend/checkin")
rxdesc = re.compile(rb"L(?:com|org|cn)[A-Za-z0-9_/]*(?:[Ss]ign|[Aa]ttend|[Cc]heck[Ii]n|[Cc]heckin|Qiandao|qiandao)[A-Za-z0-9_/]*;")
with z.open("classes.dex") as f:
    seen = collections.Counter()
    buf = b""
    while True:
        b = f.read(1 << 22)
        if not b: break
        buf = buf[-64:] + b
        for m in rxdesc.findall(buf):
            seen[m.decode("latin1")] += 1
for d, c in seen.most_common(40):
    print(f"   x{c:<5} {d}")
print("   distinct:", len(seen))