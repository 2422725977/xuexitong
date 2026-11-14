import glob, os, struct, zlib, sys
snap=sys.argv[1] if len(sys.argv)>1 else "chaoxing/out/snap3"
PAT=[b"Lcom/", b"Lcom/chaoxing", b"studentSign", b"dex\n", b"/newsign", b"Lcom/secneo", b"Landroid/app/Activity;"]
print("%-10s %12s %9s %9s %8s %7s %7s %7s" % ("region","size","Lcom/","Lchaoxing","studentS","dexN","newsign","secneo"))
for fn in sorted(glob.glob(os.path.join(snap,"r_*.bin")), key=lambda p:int(''.join(c for c in os.path.basename(p) if c.isdigit()))):
    d=open(fn,"rb").read()
    c=[d.count(p) for p in PAT]
    if any(c):
        print("%-10s %12d %9d %9d %8d %7d %7d %7d" % (os.path.basename(fn), len(d), c[0], c[1], c[2], c[3], c[4], c[5]))
