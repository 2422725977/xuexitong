import glob, os, struct, zlib, sys
snap=sys.argv[1] if len(sys.argv)>1 else "chaoxing/out/snap3"
P=bytes.fromhex("7000000078563412")
hits=[]
for fn in sorted(glob.glob(os.path.join(snap,"r_*.bin"))):
    d=open(fn,"rb").read()
    pos=0
    while True:
        i=d.find(P,pos)
        if i<0: break
        pos=i+1
        s=i-0x24
        if s<0 or i+0x50>len(d): continue
        h=d[s:s+0x70]
        f=lambda o: struct.unpack_from("<I",h,o)[0]
        fsize=f(0x20); hsize=f(0x24); endian=f(0x28)
        rec=dict(region=os.path.basename(fn), off=s, magic=h[0:8].hex(),
                 fsize=fsize, hsize=hsize, endian=hex(endian), map_off=f(0x34),
                 str_sz=f(0x38), str_off=f(0x3C), typ_sz=f(0x40), proto_sz=f(0x48),
                 fld_sz=f(0x50), mth_sz=f(0x58), cls_sz=f(0x60), dsz=f(0x68), doff=f(0x6C),
                 fits=(s+fsize<=len(d) and fsize>0x100))
        hits.append((rec,fn,d,s))
print("candidate headers:", len(hits))
for rec,fn,d,s in hits[:40]:
    print("%-10s off=%-10d magic=%-18s fsize=%-10d hsize=%d endian=%s map=%-8d str=%-7d/%d typ=%-6d proto=%-6d fld=%-6d mth=%-6d cls=%-6d data=%-10d/%d fits=%s"
          % (rec["region"], rec["off"], rec["magic"], rec["fsize"], rec["hsize"], rec["endian"], rec["map_off"],
             rec["str_sz"], rec["str_off"], rec["typ_sz"], rec["proto_sz"], rec["fld_sz"], rec["mth_sz"], rec["cls_sz"], rec["dsz"], rec["doff"], rec["fits"]))
print("--- fits list ---")
for rec,fn,d,s in hits:
    if rec["fits"]:
        print(rec["region"], hex(rec["off"]), rec["fsize"], "cls", rec["cls_sz"], "str", rec["str_sz"], "magic", rec["magic"])
