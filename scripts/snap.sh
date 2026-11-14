#!/system/bin/sh
# usage: snap.sh <delay_ms> <mode: dry|dump> <outdir>
PKG=com.chaoxing.mobile
DELAY=${1:-2500}
MODE=${2:-dry}
OUT=${3:-/data/local/tmp/snap}
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
echo "pid=$pid waited_iters=$i"
[ -z "$pid" ] && exit 1
t=$DELAY
while [ $t -gt 0 ]; do t=$((t-50)); sleep 0.05; done
alive=$(pidof $PKG)
echo "alive_before_stop=$alive"
kill -STOP $pid 2>/dev/null
echo "stopped=$pid"
nreg=0
total=0
while read -r line; do
  set -- $line
  range=$1
  perms=$2
  path=$6
  case "$perms" in rw*) ;; *) continue ;; esac
  start=${range%-*}
  end=${range#*-}
  s=$((0x$start))
  e=$((0x$end))
  len=$((e-s))
  if [ $len -lt 65536 ]; then continue; fi
  nreg=$((nreg+1))
  total=$((total+len))
  if [ "$MODE" = "dump" ]; then
    dd if=/proc/$pid/mem of=$OUT/r_${nreg}_${start}_${len}.bin bs=4096 skip=$((s/4096)) count=$((len/4096)) 2>/dev/null
  fi
done < /proc/$pid/maps
echo "rw_regions_ge64k=$nreg total_bytes=$total"
if [ "$MODE" = "dump" ]; then
  echo "dumped_files=$(ls $OUT | wc -l)"
  du -sk $OUT
fi
kill -CONT $pid 2>/dev/null
echo "continued"
sleep 1
echo "pid_after=$(pidof $PKG)"
