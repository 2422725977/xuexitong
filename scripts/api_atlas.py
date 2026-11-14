#!/usr/bin/env python3
"""API atlas of the core segment + sign-related identifier harvest + manifest neighbours."""
import zipfile, re, collections, os

P = "samples/学习通.apk"
OUT = "chaoxing/out"
z = zipfile.ZipFile(P)
data = z.read("classes.dex")

print("=== core segment (35.5M-37.5M) URL atlas")
seg = data[35_500_000:37_500_000]
urls = collections.Counter()
for m in re.finditer(rb"https?://[A-Za-z0-9._~:/?#\[\]@!$&'()*+,;=%*\-]{6,220}", seg):
    urls[m.group().decode("latin1")] += 1
print("   distinct urls:", len(urls))
with open(os.path.join(OUT, "api_atlas_core.txt"), "w") as fh:
    for k, v in sorted(urls.items()):
        fh.write(k + "\n")
for k in sorted(urls):
    print("   ", k[:150])

print("=== sign-ish identifiers in the readable payload")
ident = re.compile(rb"(?:[gs]et)?[A-Za-z_]{0,14}[Ss]ign[A-Za-z_]{0,14}")
c = collections.Counter()
for m in ident.finditer(data):
    s = m.group().decode("latin1")
    if 5 <= len(s) <= 32:
        c[s] += 1
for k, v in c.most_common(60):
    print(f"   x{v}  {k}")
print("   total distinct:", len(c))

print("=== sign-related literal strings (Chinese) in payload")
for m in re.finditer("签到[^\\x00]{0,40}".encode(), data):
    try:
        s = m.group().decode("utf-8")
    except Exception:
        continue
    if len(s) > 3:
        print("   ", s[:70])
