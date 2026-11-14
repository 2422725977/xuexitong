#!/usr/bin/env python3
"""Dump the mobilelearn API template table + hunt the student sign-in submit endpoint."""
import zipfile, re, collections, os

P = "samples/学习通.apk"
OUT = "chaoxing/out"
z = zipfile.ZipFile(P)

host = re.compile(rb"[a-z0-9.]*chaoxing\.com/[A-Za-z0-9_/]{2,70}")
kw = re.compile(rb"(stuSignajax|activeId|clientip|ifTiJiao|signCode|getSign|signEnc|generalSign|faceSign|qrSign|signType|attendenc|signInType|pptSign/[A-Za-z0-9_]+)")
tmpl = re.compile(rb"/(?:pptSign|ppt|pptAnswer|pptTestPaper|pptTest|pptPingFen|phone|apisign)[A-Za-z0-9_/]*(?:\?[A-Za-z0-9_%=&+.,*$-]*)?")
zh = re.compile("手势".encode("utf-8"))

hosts = collections.Counter()
kws = collections.Counter()
tmpls = collections.Counter()
sign_ctx = []

with z.open("classes.dex") as f:
    while True:
        b = f.read(1 << 22)
        if not b: break
        for m in host.finditer(b):
            hosts[m.group().decode("latin1")] += 1
        for m in tmpl.finditer(b):
            t = m.group().decode("latin1")
            tmpls[t] += 1
            if len(sign_ctx) < 24 and ("pptSign" in t or "sign" in t.lower()):
                a = max(0, m.start() - 700); c = min(len(b), m.end() + 700)
                sign_ctx.append(b[a:c].decode("utf-8", "replace"))
        for m in kw.finditer(b):
            kws[m.group().decode("latin1")] += 1

print("=== chaoxing host/path table (mobilelearn first)", len(hosts))
with open(os.path.join(OUT, "chaoxing_hostpaths.txt"), "w") as fh:
    for k, v in hosts.most_common():
        fh.write(f"{v}\t{k}\n")
for k, v in hosts.most_common():
    if "mobilelearn" in k:
        print(f"   x{v}  {k}")

print("=== sign keyword census")
for k, v in kws.most_common(30):
    print(f"   x{v}  {k}")

print("=== android-level templates (pptSign family)")
for k, v in tmpls.most_common(60):
    print(f"   x{v}  {k}")

print("=== 手势 present:", len(zh.findall(b"")))

print("=== raw context around sign templates")
seen = set()
for c in sign_ctx[:6]:
    key = c[:60]
    if key in seen: continue
    seen.add(key)
    print("----------------------------------------")
    print(re.sub(r"[^\x20-\x7e\u4e00-\u9fff]", ".", c)[:1500])