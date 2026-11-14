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
cp /proc/$pid/maps /data/local/tmp/maps.txt
echo "maps_lines=$(wc -l < /data/local/tmp/maps.txt)"
echo "stopped_at_delay=$DELAY alive=$(pidof $PKG)"
kill -CONT $pid 2>/dev/null
