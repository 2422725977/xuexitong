#!/system/bin/sh
PKG=com.chaoxing.mobile
DELAY=${1:-2500}
OUT=${2:-/data/local/tmp/snap3}
MINSZ=${3:-1048576}
# 64-bit-safe page number for a 64-bit hex address (toybox sh arithmetic is 32-bit)
pg() {
  a=$1
  hi=${a%????????}
  lo=${a#${hi}}
  lo=${lo%???}
  if [ -z "$hi" ]; then echo $((0x$lo)); else echo $((0x$hi*1048576+0x$lo)); fi
}
am force-stop $PKG
sleep 1
rm -rf $OUT
mkdir -p $OUT
am start -n $PKG/.activity.SplashActivity >/dev/null 2>&1
pid=
i=0
while [ $i -lt 60 ]; do pid=$(pidof $PKG); [ -n "$pid" ] && break; i=$((i+1)); sleep 0.05; done
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
  start=${range%-*}
  end=${range#*-}
  sp=$(pg $start)
  ep=$(pg $end)
  pages=$((ep-sp))
  [ $pages -lt 256 ] && continue
  n=$((n+1))
  dd if=/proc/$pid/mem of=$OUT/r_$n.bin bs=4096 skip=$sp count=$pages 2>$OUT/err_$n.txt
  sz=$(stat -c %s $OUT/r_$n.bin 2>/dev/null)
  tot=$((tot+sz))
  echo "r_$n.bin start=$start want=$((pages*4096)) got=$sz [$path]" >> $OUT/index.txt
done < /proc/$pid/maps
echo "regions=$n dumped_bytes=$tot"
kill -CONT $pid 2>/dev/null
cat $OUT/index.txt
