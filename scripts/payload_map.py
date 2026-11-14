#!/usr/bin/env python3
"""Fine-grained map of the sealed payload inside classes.dex + zlib/ELF magic census."""
import zipfile, struct, math, collections, re

P = "samples/学习通.apk"
z = zipfile.ZipFile(P)
CH = 65536

def ent(b):
    c = collections.Counter(b); n = len(b)
    return -sum((v/n) * math.log2(v/n) for v in c.values())

segs = []
with z.open("classes.dex") as f:
    off = 0
    while True:
        b = f.read(CH)
        if not b: break
        e = ent(b)
        kind = "zero/pad" if e < 2.0 else ("compressed" if e < 6.8 else "cipher")
        segs.append((off, kind, e))
        off += len(b)

# collapse runs
runs = []
for o, k, e in segs:
    if runs and runs[-1][0] == k:
        runs[-1][1] = o + CH; runs[-1][2] += 1
    else:
        runs.append([k, o, 1, e])
print("=== payload runs (>64KB)")
for k, start, cnt, e in runs:
    end = start + cnt * CH
    if cnt * CH >= 65536:
        print(f"   {k:<11} {start:>10} .. {end:>10}  ({cnt*CH/1048576:.1f} MB) ent~{e:.2f}")

print("=== magic census across classes.dex")
pats = {
    "zlib 789c": b"\x78\x9c", "zlib 7801": b"\x78\x01", "zlib 78da": b"\x78\xda",
    "dex magic": b"dex\n035", "ELF": b"\x7fELF", "PK zip": b"PK\x03\x04",
    "PK apk v2": b"APK Sig Block 42",
}
counts = collections.Counter()
offsets = collections.defaultdict(list)
with z.open("classes.dex") as f:
    pos = 0
    prev = b""
    while True:
        b = f.read(1 << 22)
        if not b: break
        buf = prev + b
        for name, pat in pats.items():
            i = buf.find(pat)
            while i >= 0:
                counts[name] += 1
                if len(offsets[name]) < 6: offsets[name].append(pos - len(prev) + i)
                i = buf.find(pat, i + 1)
        prev = buf[-8:]
        pos += len(b)
for k, v in counts.most_common():
    print(f"   {k:<12} x{v:<8} first@{offsets[k][:4]}")

print("=== vendor strings in payload (first 200 hits, deduped)")
pat = re.compile(rb"(secneo|bangcle|DexHelper|nagain|ijiami|apkprotect|jiagu|com\.chaoxing|classes\.dex|CACHE|decrypt|VMP|vmprotect|licen|soinfo)", re.I)
hits = collections.Counter()
with z.open("classes.dex") as f:
    f.seek(24528)
    while True:
        b = f.read(1 << 22)
        if not b: break
        for m in pat.findall(b):
            hits[m.decode('latin1').lower()] += 1
        tags = 0
for k, v in hits.most_common(20):
    print(f"   {k:<16} x{v}")
