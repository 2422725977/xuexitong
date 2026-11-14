#!/bin/bash
# dump_and_mine.sh — 对 frida-dexdump 产物做批量分析（droidasc 链路）
# 用法: bash chaoxing/scripts/dump_and_mine.sh [dump_dir]
set -u
DUMP=chaoxing/out/dump
if [ -n "${1}" ]; then DUMP="${1}"; fi
DROIDASC=/opt/anaconda3/bin/droidasc
OUT=chaoxing/out

echo "== dump dir: $DUMP"
ls -la "$DUMP" 2>/dev/null | head -40
echo
echo "== merge class lists"
: > "$OUT/dumped_all_classes.txt"
for f in "$DUMP"/*.dex; do
  [ -e "$f" ] || continue
  echo "-- $f"
  "$DROIDASC" "$f" listclass >> "$OUT/dumped_all_classes.txt" 2>/dev/null
done
sort -u "$OUT/dumped_all_classes.txt" > "$OUT/dumped_all_classes.uniq.txt"
wc -l "$OUT/dumped_all_classes.uniq.txt"
echo
echo "== sign module hits"
grep -c 'com/chaoxing/mobile/sign' "$OUT/dumped_all_classes.uniq.txt" || true
grep -E 'chaoxing/(mobile/sign|beacon|mobile/office)' "$OUT/dumped_all_classes.uniq.txt" | sort -u | head -60
echo
echo "== decompile SignInfoActivity"
for f in "$DUMP"/*.dex; do
  [ -e "$f" ] || continue
  if "$DROIDASC" "$f" listclass 2>/dev/null | grep -q 'com/chaoxing/mobile/sign/ui/SignInfoActivity'; then
    echo ">> hit $f"
    "$DROIDASC" "$f" getclass 'Lcom/chaoxing/mobile/sign/ui/SignInfoActivity;' -o "$OUT/SignInfoActivity.java" && echo "wrote $OUT/SignInfoActivity.java"
    "$DROIDASC" "$f" findrefs string 'newsign/studentSign' -o "$OUT/refs_studentSign.txt" && echo "wrote $OUT/refs_studentSign.txt"
    break
  fi
done
echo DONE
