#!/system/bin/sh
PKG=com.chaoxing.mobile
DELAY=${1:-2500}
OUT=${2:-/data/local/tmp/snap}
PAT=${3:-"libc_malloc|large object space|LinearAlloc|libDexHelper|dexjni|encrypt|dalvik-main space"}
am force-stop $PKG
sleep 1
rm -rf $OUT
mkdir -p $OUT
am start -n $PKG/.activity.SplashActivity >/dev/null 2>&1
pid=
i=0
while [ $i -lt 60 ]; do
  pid=$(pidof $PKG)
  [ -n "$pid" ] && break
  i=$((i+1))
  sleep 0.05
done
echo "pid=$pid"
t=$DELAY
while [ $t -gt 0 ]; do t=$((t-50)); sleep 0.05; done
kill -STOP $pid 2>/dev/null
n=0
tot=0
while read -r line; do
  set -- $line
  range=$1
  perms=$2
  path=$6
  case "$perms" in rw*) ;; *) continue ;; esac
  printf '%s' "$path" | grep -qE "$PAT" || continue
  start=${range%-*}
  end=${range#*-}
  s=$((0x$start))
  e=$((0x$end))
  len=$((e-s))
  [ $len -lt 4096 ] && continue
  n=$((n+1))
  tot=$((tot+len))
  dd if=/proc/$pid/mem of=$OUT/r_${n}.bin bs=4096 skip=$((s/4096)) count=$((len/4096)) 2>/dev/null
  echo "r_${n}.bin $start $len [$path]" >> $OUT/index.txt
done < /proc/$pid/maps
echo "regions=$n total_bytes=$tot"
kill -CONT $pid 2>/dev/null
ls -la $OUT | tail -8
du -sk $OUT
