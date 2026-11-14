#!/usr/bin/env python3
"""Whole-APK endpoint census: chaoxing hosts and API paths in every readable entry."""
import zipfile, re, collections, os

P = "samples/学习通.apk"
z = zipfile.ZipFile(P)
OUT = "chaoxing/out"
os.makedirs(OUT, exist_ok=True)

host = re.compile(rb"https?://([A-Za-z0-9._-]*chaoxing[A-Za-z0-9._-]*)(?::[0-9]+)?(/[A-Za-z0-9_./?=&%+\-]*)")
api = re.compile(rb"/(?:pptSign|stuSignajax|apisign|sign/ajax|mobilel|teacher|student)[A-Za-z0-9_/.]{0,60}", re.I)

hosts = collections.Counter()
apis = collections.Counter()
where = collections.defaultdict(collections.Counter)

for info in z.infolist():
    if info.is_dir() or info.file_size == 0: continue
    if re.search(r"\.(so|png|jpg|jpeg|webp|ttf|otf|mp3|wav|ogg|bin|ocd2|prof|profm|map)$", info.filename, re.I): continue
    cap = min(info.file_size, 30 * 1024 * 1024)
    try:
        with z.open(info) as f:
            data = f.read(cap)
    except Exception:
        continue
    for m in host.finditer(data):
        h = m.group(1).decode("latin1") + m.group(2).decode("latin1")[:60]
        hosts[h] += 1
        where[h][info.filename] += 1
    for m in api.findall(data):
        apis[m.decode("latin1")] += 1

print("=== chaoxing hosts/paths (top 60)")
for k, v in hosts.most_common(60):
    print(f"   {v:>6}  {k}")
print("   distinct:", len(hosts))
print("=== sign-ish api path fragments (top 40)")
for k, v in apis.most_common(40):
    print(f"   {v:>6}  {k}")
print("=== files carrying sign-ish endpoints")
for h, c in sorted(where.items(), key=lambda kv: -sum(kv[1].values()))[:15]:
    print("  ", h[:70], "->", list(c)[:3])
