#!/usr/bin/env python3
# Carve DEX files out of the memory dump regions.
import os, sys, zlib, struct, hashlib, re, json, glob

SNAPDIR = sys.argv[1] if len(sys.argv) > 1 else "chaoxing/out/snap3"
OUTDIR  = sys.argv[2] if len(sys.argv) > 2 else "chaoxing/out/dexes"
os.makedirs(OUTDIR, exist_ok=True)

# region index: filename -> (base_addr, size, pathname)
idx = {}
idxp = os.path.join(SNAPDIR, "index.txt")
if os.path.exists(idxp):
    for line in open(idxp, errors="replace"):
        m = re.match(r"(\S+\.bin) start=([0-9a-f]+) want=(\d+) got=(\d+)\s*\[(.*)", line.strip())
        if m:
            idx[m.group(1)] = (int(m.group(2), 16), int(m.group(4)), m.group(5))

MAGICS = [b"dex\n035\x00", b"dex\n036\x00", b"dex\n037\x00", b"dex\n038\x00", b"dex\n039\x00"]
found = []
for fn in sorted(glob.glob(os.path.join(SNAPDIR, "r_*.bin"))):
    base = fn.split("/")[-1]
    data = open(fn, "rb").read()
    n = len(data)
    for mg in MAGICS:
        pos = 0
        while True:
            i = data.find(mg, pos)
            if i < 0:
                break
            pos = i + 1
            if i + 0x70 > n:
                continue
            hdr = data[i:i+0x70]
            (checksum, sig, fsize, hsize, endian, link_sz, link_off, map_off,
             str_sz, str_off, typ_sz, typ_off, proto_sz, proto_off,
             fld_sz, fld_off, mth_sz, mth_off, cls_sz, cls_off,
             dsize, doff) = struct.unpack_from("<IIIIIIIIIIIIIIIIIIIIII", hdr, 8)
            ok = {}
            ok["endian"] = (endian == 0x12345678)
            ok["hsize"] = (hsize == 0x70)
            ok["size_in_map"] = (i + fsize <= n)
            ck = None
            if ok["size_in_map"] and fsize > 32:
                ck = zlib.adler32(data[i+12:i+fsize]) & 0xffffffff
                ok["checksum"] = (ck == checksum)
            else:
                ok["checksum"] = False
            sha = hashlib.sha1(data[i+32:i+fsize]).hexdigest() if ok["size_in_map"] else None
            ok["sig"] = (sha == "%08x%s" % (0, "") ) if False else None
            if sha is not None:
                try:
                    ok["sig_ok"] = (bytes.fromhex(sha) == sig)
                except Exception:
                    ok["sig_ok"] = False
            rec = dict(region=base, off=i, addr=(idx.get(base, (0,))[0] + i),
                       fsize=fsize, strings=str_sz, classes=cls_sz, methods=mth_sz,
                       types=typ_sz, ok=ok, pathname=idx.get(base, (0, 0, "?"))[2])
            found.append(rec)
            print(json.dumps(rec))
            if ok.get("checksum"):
                out = os.path.join(OUTDIR, "dex_%s_%x.dex" % (base.replace(".bin",""), i))
                open(out, "wb").write(data[i:i+fsize])
                print("SAVED", out, fsize, "classes=%d strings=%d methods=%d" % (cls_sz, str_sz, mth_sz))

print("---- total magic hits:", len(found))
good = [r for r in found if r["ok"].get("checksum")]
print("---- checksum-valid dex:", len(good))
for r in good:
    print("  ", r["region"], hex(r["off"]), "addr", hex(r["addr"]), "size", r["fsize"],
          "classes", r["classes"], "strings", r["strings"], "path", r["pathname"])
