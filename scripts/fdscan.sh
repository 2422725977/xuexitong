#!/system/bin/sh
PKG=com.chaoxing.mobile
DELAY=${1:-2500}
am force-stop $PKG
sleep 1
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
echo "=== fd list ==="
ls -l /proc/$pid/fd 2>/dev/null
echo "=== fd sizes (non-socket) ==="
for f in /proc/$pid/fd/*; do
  tgt=$(readlink $f)
  case "$tgt" in socket*|pipe*|anon_inode*|/dev/*) continue ;; esac
  sz=$(wc -c < $f 2>/dev/null)
  echo "$f -> $tgt size=$sz"
done
echo "=== maps: memfd/deleted ==="
grep -E "memfd|deleted" /proc/$pid/maps | head -20
kill -CONT $pid 2>/dev/null
