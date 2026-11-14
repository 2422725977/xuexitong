import glob, collections, os, re, struct
snap="chaoxing/out/snap3"
pref=collections.Counter()
hits=[]
tot=0
for fn in sorted(glob.glob(os.path.join(snap,"r_*.bin"))):
    d=open(fn,"rb").read(); tot+=len(d)
    pos=0
    while True:
        i=d.find(b"035\x00",pos)
        if i<0: break
        pos=i+1
        if i>=4 and i+0x24+8<len(d):
            p=d[i-4:i+4]
            pref[p]+=1
            if i+0x40<len(d):
                hdr=d[i-4:i+0x40]
                et=struct.unpack_from("<I",hdr,0x28-4 if False else 0)[0]
                if len(hits)<8: hits.append((fn.split("/")[-1],hex(i),p.hex()))
print("total bytes scanned", tot)
print("top prefixes preceding '035\\x00':")
for p,c in pref.most_common(12): print("  ",p.hex(),p,c)
print("samples", hits[:8])
