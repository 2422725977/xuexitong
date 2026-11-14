import zipfile, glob, os
out="chaoxing/out/unpacked.apk"
dexes=sorted(glob.glob("chaoxing/out/dexes/*.dex"))
z=zipfile.ZipFile(out,"w",zipfile.ZIP_STORED)
for i,d in enumerate(dexes):
    name="classes.dex" if i==0 else "classes%d.dex"%(i+1)
    z.write(d,name)
    print(name, os.path.getsize(d))
z.close()
print("wrote",out,os.path.getsize(out))
