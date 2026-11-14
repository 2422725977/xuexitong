#!/usr/bin/env python3
"""chaoxing apk recon: dex headers, entry census, packer markers."""
import zipfile, struct, hashlib, collections, sys, json

P = "samples/学习通.apk"
z = zipfile.ZipFile(P)
names = z.namelist()
print("entries:", len(names))

def dexhdr(dex):
    try:
        info = z.getinfo(dex)
    except KeyError:
        print("--- MISSING", dex); return None
    with z.open(dex) as f:
        b = f.read(4096)
    fields = dict(
        magic=b[:8],
        checksum=struct.unpack_from("<I", b, 8)[0],
        sig=b[12:32].hex(),
        file_size=struct.unpack_from("<I", b, 32)[0],
        header_size=struct.unpack_from("<I", b, 36)[0],
        endian=struct.unpack_from("<I", b, 40)[0],
        map_off=struct.unpack_from("<I", b, 52)[0],
        string_ids=struct.unpack_from("<I", b, 56)[0],
        type_ids=struct.unpack_from("<I", b, 64)[0],
        proto_ids=struct.unpack_from("<I", b, 72)[0],
        field_ids=struct.unpack_from("<I", b, 80)[0],
        method_ids=struct.unpack_from("<I", b, 88)[0],
        class_defs=struct.unpack_from("<I", b, 96)[0],
        data_size=struct.unpack_from("<I", b, 104)[0],
    )
    print("---", dex, "zip_stored_size=", info.file_size, "compress_type=", info.compress_type)
    for k, v in fields.items():
        print("   ", k, "=", v)
    return fields

for d in ["classes.dex", "assets/RiskStub.dex"]:
    dexhdr(d)

print("--- class-ish entry census (path based)")
c = collections.Counter(n.split("/")[0] for n in names)
print("  top:", c.most_common(12))

print("--- packer marker scan in lib/ + assets/")
import re
pat = re.compile(r"(jiagu|nagai|DexHelper|libdex|libexec|libshell|mobisec|tup\.so|secneo|bangcle|ijiami|RiskStub|libkwsc|libtoolchecker|libchaos|libnative-lib|libencrypt|libSecShell|libprotect)", re.I)
hits = sorted({n for n in names if pat.search(n)})
for h in hits[:40]:
    print("   ", h)

print("--- native-lib refs inside classes.dex (System.loadLibrary strings, name-probe)")
with z.open("classes.dex") as f:
    head = f.read(4 * 1024 * 1024)
print("   first4MB scan:", [s.decode() for s in re.findall(rb"[ -~]{6,40}\.so", head)][:20])

print("--- assets/meta-data manifest+rsa")
for n in names:
    if n.startswith("assets/meta-data/"):
        print("   ", n, z.getinfo(n).file_size)
