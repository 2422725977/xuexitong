#!/usr/bin/env python3
"""Layout + entropy map of classes.dex (stub vs payload) and asset blob census."""
import zipfile, struct, math, collections, re

P = "samples/学习通.apk"
z = zipfile.ZipFile(P)

def ent(b):
    if not b: return 0.0
    c = collections.Counter(b); n = len(b)
    return -sum((v/n) * math.log2(v/n) for v in c.values())

print("=== classes.dex layout (streamed)")
info = z.getinfo("classes.dex")
CH = 1 << 20
with z.open("classes.dex") as f:
    off = 0; rows = []
    while True:
        b = f.read(CH)
        if not b: break
        zeros = b.count(0)
        rows.append((off, len(b), ent(b), zeros / len(b)))
        off += len(b)
print("   chunks:", len(rows), "total:", off)
for i, (o, n, e, zr) in enumerate(rows):
    if i % 8 == 0 or i == len(rows) - 1:
        print(f"   off={o:>10} len={n:>8} ent={e:.3f} zero={zr:.3f}")

print("=== where does real content end? (header data_size=19372, data_off)")
with z.open("classes.dex") as f:
    head = f.read(112)
data_off = struct.unpack_from("<I", head, 108)[0]
print("   data_off:", data_off, "-> real content ends near", data_off + 19372)

print("=== distinct-byte sample in tail")
with z.open("classes.dex") as f:
    f.seek(off - 65536)
    tail = f.read(65536)
print("   tail[0:32] hex:", tail[:32].hex())
print("   tail printable runs:", [s.decode('latin1') for s in re.findall(rb"[ -~]{8,60}", tail)][:10])

print("=== second dex magic anywhere?")
found = []
with z.open("classes.dex") as f:
    pos = 0
    while True:
        b = f.read(1 << 22)
        if not b: break
        i = b.find(b"dex\n035")
        while i >= 0:
            found.append(pos + i); i = b.find(b"dex\n035", i + 1)
        pos += len(b)
print("   occurrences:", found[:10])

print("=== assets/ blobs worth a look (>100KB, not image/font)")
rows = []
for n in z.namelist():
    if not n.startswith("assets/"): continue
    if n.endswith((".png",".jpg",".jpeg",".webp",".gif",".ttf",".otf",".mp3",".wav",".ogg",".svg",".dex",".html",".js",".json",".txt",".md",".xml",".prof",".profm")): continue
    s = z.getinfo(n).file_size
    if s > 100_000: rows.append((s, n))
rows.sort(reverse=True)
for s, n in rows[:25]:
    print(f"   {s:>12}  {n}")

print("=== lib/ dirs present")
libdirs = sorted({n.split('/')[1] for n in z.namelist() if n.startswith("lib/")})
print("  ", libdirs)
print("=== interesting libs")
for n in sorted(z.namelist()):
    if n.startswith("lib/") and re.search(r"(DexHelper|dexjni|encrypt|SecShell|SecNeo|secneo|RiskStub|jiagu|shell|protect|vmp|chaos|stub)", n, re.I):
        print("   ", n, z.getinfo(n).file_size)
