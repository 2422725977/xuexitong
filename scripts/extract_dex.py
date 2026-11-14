#!/usr/bin/env python3
# Extract every DEX found in the memory dump, verify checksum+signature.
import glob, os, struct, zlib, hashlib, sys
snap = sys.argv[1] if len(sys.argv)>1 else "chaoxing/out/snap3"
outd = sys.argv[2] if len(sys.argv)>2 else "chaoxing/out/dexes"
os.makedirs(outd, exist_ok=True)
P = bytes.fromhex("6465780a30333500")   # dex\n035\0
n_ok = 0; n_ck = 0
for fn in sorted(glob.glob(os.path.join(snap, "r_*.bin"))):
    d = open(fn, "rb").read()
    pos = 0
    while True:
        i = d.find(P, pos)
        if i < 0: break
        pos = i + 1
        if i + 0x70 > len(d): continue
        g = lambda o: struct.unpack_from("<I", d, i+o)[0]
        fsize, hsize, endian, moff = g(0x20), g(0x24), g(0x28), g(0x34)
        if hsize != 0x70 or endian != 0x12345678: continue
        if fsize <= 0x100 or i + fsize > len(d): continue
        if not (0x70 < moff < fsize) or g(0x3c) != 0x70: continue
        blob = d[i:i+fsize]
        ck = zlib.adler32(blob[12:]) & 0xffffffff
        sha = hashlib.sha1(blob[32:]).hexdigest()
        stored_ck = struct.unpack_from("<I", blob, 8)[0]
        stored_sig = blob[12:32].hex()
        n_ok += 1
        ck_ok = (ck == stored_ck)
        if ck_ok: n_ck += 1
        name = "classes_%02d_%08x.dex" % (n_ok, i)
        open(os.path.join(outd, name), "wb").write(blob)
        print("%-26s off=%-10d size=%-9d ck_ok=%-5s sig_ok=%-5s cls=%-6d str=%-6d mth=%-6d fld=%-6d typ=%-6d pro=%-6d"
              % (name, i, fsize, str(ck_ok), str(sha == stored_sig),
                 g(0x60), g(0x38), g(0x58), g(0x50), g(0x40), g(0x48)))
print("extracted:", n_ok, "checksum-valid:", n_ck, "->", outd)
