#!/usr/bin/env python3
import zipfile, re
P = "samples/学习通.apk"
z = zipfile.ZipFile(P)
d = z.read("assets/schedule/js/schedule.js").decode("utf-8", "replace")
print("=== region 72500-79500")
print(d[72500:79500])
print()
print("=== path-like templates in schedule.js")
pats = sorted(set(re.findall(r"['\"](/(?:ppt|phone|sign|newsign|widget|pptSign|active|task|mobile)[A-Za-z0-9_/?=&%\-.]{0,120})['\"]", d)))
for p in pats:
    print("   ", p)
print("   total path templates:", len(pats))
print()
print("=== hosts referenced")
for h in sorted(set(re.findall(r"https?://([A-Za-z0-9.\-]+)", d))):
    print("   ", h)
print()
print("=== md5.txt head")
print(z.read("assets/schedule/md5.txt").decode("utf-8", "replace")[:400])
