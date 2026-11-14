#!/usr/bin/env python3
# Dump the string pool of every extracted dex (now plaintext).
import glob, struct, os, sys, re
out = sys.argv[1] if len(sys.argv) > 1 else "chaoxing/out/dumped_strings.txt"
seen = set(); total = 0
with open(out, "w", errors="replace") as w:
    for fn in sorted(glob.glob("chaoxing/out/dexes/*.dex")):
        d = open(fn, "rb").read()
        g = lambda o: struct.unpack_from("<I", d, o)[0]
        sz, off = g(0x38), g(0x3c)
        for i in range(sz):
            try:
                so = struct.unpack_from("<I", d, off + 4*i)[0]
                n = 0; p = so
                # uleb128 string length
                while True:
                    b = d[p]; n |= (b & 0x7f) << (7*0)
                    p += 1
                    if not (b & 0x80): break
                # correct uleb128 decode
                p = so; n = 0; shift = 0
                while True:
                    b = d[p]; n |= (b & 0x7f) << shift; shift += 7; p += 1
                    if not (b & 0x80): break
                s = d[p:p+n].decode("utf-8", errors="replace")
            except Exception:
                continue
            total += 1
            if s and s not in seen:
                seen.add(s); w.write(s + "\n")
print("strings scanned:", total, "unique:", len(seen), "->", out)
