#!/usr/bin/env python3
import zipfile, re, struct, collections
P = "samples/学习通.apk"
z = zipfile.ZipFile(P)
VMP = ["en_fun", "en_fun_num", "g_func_map", "g_addr", "dexflag", "multidex_entry", "g_sdkVer_forhook", "libc_ptrace", "file_queue", "resItems", "resCount", "baseinfo", "javaVM", "JNI_OnLoad"]
for lib in ["libDexHelper.so", "libdexjni.so", "libencrypt.so", "libDexHelper-x86.so"]:
    for cand in ["lib/arm64-v8a/" + lib, "lib/x86/" + lib]:
        try:
            d = z.read(cand)
        except KeyError:
            continue
        machine = struct.unpack_from("<H", d, 18)[0] if d[:4] == b"\x7fELF" else None
        names = re.findall(rb"[A-Za-z_][A-Za-z0-9_]{3,40}", d)
        s = set(n.decode() for n in names)
        hit = [k for k in VMP if k in s]
        vmpblob = len(re.findall(rb"p[0-9A-Za-z_$]{20,}", d))
        print(f"{cand:44s} size={len(d):9d} machine={machine} vmp_markers={hit} vmp_nametables={vmpblob}")
        print("    >", cand)
print()
print("=== section names in libDexHelper.so")
d = z.read("lib/arm64-v8a/libDexHelper.so")
shoff = struct.unpack_from("<Q", d, 40)[0]; shnum = struct.unpack_from("<H", d, 60)[0]; shstr = struct.unpack_from("<H", d, 62)[0]
sh = [struct.unpack_from("<IIQQQQIIQQ", d, shoff + i * 64) for i in range(shnum)]
st = d[sh[shstr][4]:sh[shstr][4] + sh[shstr][5]]
def nm(x): return st[x:st.index(b"\x00", x)].decode()
print("   ", ", ".join(f"{nm(s[0])}({s[5]})" for s in sh if s[5]))
print()
print("=== dynamic exports of interest")
for s in sh:
    if s[1] == 11:
        sym = d[s[4]:s[4] + s[5]]; strs = d[sh[s[6]][4]:sh[s[6]][4] + sh[s[6]][5]]
        ex = []
        for j in range(0, len(sym), s[9] or 24):
            st_name, info = struct.unpack_from("<I", sym, j)[0], sym[j + 4]
            if st_name and (info >> 4) in (1, 2):
                e = strs.index(b"\x00", st_name); ex.append(strs[st_name:e].decode())
        print("   exported:", ", ".join(ex[:40]), " count:", len(ex))
