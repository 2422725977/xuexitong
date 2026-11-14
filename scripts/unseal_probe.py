#!/usr/bin/env python3
"""Attempt static recovery inside the sealed payload: embedded zips, zlib/deflate streams, single-byte-xor dex."""
import zipfile, zlib, re, struct, collections

P = "samples/学习通.apk"
z = zipfile.ZipFile(P)
data = z.read("classes.dex")
print("payload bytes:", len(data))

print("=== embedded PK local headers")
for p in [14871863, 18191542, 29333864]:
    try:
        sig, ver, flags, method, mtime, mdate, crc, csize, usize, nlen, elen = struct.unpack_from("<IHHHHHIIIHH", data, p)
        name = data[p + 30:p + 30 + nlen]
        print(f"  @{p} sig={sig:08x} method={method} csize={csize} usize={usize} name={name[:24]!r}")
    except Exception as e:
        print(f"  @{p} parse error {e}")

print("=== zlib/deflate recovery attempts (sampled)")
hits = []
for m in re.finditer(rb"\x78[\x01\x9c\xda]", data):
    hits.append(m.start())
print("  zlib-header candidates:", len(hits))
ok = 0; tried = 0
for off in hits[:4000]:
    tried += 1
    for wbits in (15, -15):
        try:
            d = zlib.decompressobj(wbits)
            out = d.decompress(data[off:off + 262144], 262144)
            if len(out) >= 64:
                ok += 1
                if ok <= 12:
                    print(f"   @{off} wbits={wbits} inflated={len(out)} head={out[:16].hex()} ascii={out[:24]!r}")
                break
        except Exception:
            continue
print(f"  tried={tried} successful={ok}")

print("=== single-byte XOR / dex magic probe on region heads")
for off in [65536, 4718592, 12189696, 21233664, 33619968, 45744128, 57802752, 69664768, 81788928, 92274688]:
    win = data[off:off + 8]
    best = None
    for k in range(256):
        x = bytes(b ^ k for b in win)
        if x.startswith(b"dex\n035"):
            best = k
    print(f"   @{off} head={win.hex()} xor-dex-key={best}")

print("=== tail structure (last 8MB): repeated 16-byte block check")
tail = data[-8 << 20:]
blocks = collections.Counter(tail[i:i + 16] for i in range(0, len(tail) - 16, 16))
print("   unique 16B blocks:", len(blocks), "most common:", blocks.most_common(2)[0][1])
print("   first 64B:", tail[:64].hex())
print("=== is the tail an APK/zip/dex under simple transforms?")
for k in (0x00, 0xff):
    blk = bytes(b ^ k for b in tail[:8])
    print(f"   xor{k:02x} head:", blk)
print("   PK search in tail:", tail.find(b"PK\x03\x04"), " dex search:", tail.find(b"dex\n035"))