#!/system/bin/sh
PKG=com.chaoxing.mobile
am force-stop $PKG
sleep 1
am start -n $PKG/.activity.SplashActivity >/dev/null 2>&1
pid=
i=0
while [ $i -lt 60 ]; do pid=$(pidof $PKG); [ -n "$pid" ] && break; i=$((i+1)); sleep 0.05; done
echo "pid=$pid"
t=20
while [ $t -gt 0 ]; do t=$((t-1)); sleep 0.1; done
kill -STOP $pid
grep "libc_malloc" /proc/$pid/maps | head -6
echo "=== test 1: dd bs=4096 skip offset ==="
line=$(grep "libc_malloc" /proc/$pid/maps | head -1)
set -- $line
range=$1
s=$((0x${range%-*}))
e=$((0x${range#*-}))
echo "range=$range start=$s len=$((e-s))"
dd if=/proc/$pid/mem of=/data/local/tmp/t1.bin bs=4096 skip=$((s/4096)) count=4 2>&1 | tail -3
ls -la /data/local/tmp/t1.bin
echo "=== test 2: dd bs=1M skip_bytes ==="
dd if=/proc/$pid/mem of=/data/local/tmp/t2.bin bs=1048576 iflag=skip_bytes,count_bytes skip=$s count=4194304 2>&1 | tail -3
ls -la /data/local/tmp/t2.bin
echo "=== test 3: dd bs=1 count=64 ==="
dd if=/proc/$pid/mem of=/data/local/tmp/t3.bin bs=4096 skip=$((s/4096)) count=1 2>&1 | tail -2
ls -la /data/local/tmp/t3.bin
echo "=== test 4: read via /proc/pid/mem direct (cat) ==="
dd if=/proc/$pid/mem bs=65536 skip=$((s/65536)) count=2 2>/dev/null | wc -c
kill -CONT $pid 2>/dev/null
