#!/system/bin/sh
PKG=com.chaoxing.mobile
ACT=$PKG/.activity.SplashActivity
am force-stop $PKG
sleep 1
logcat -c
am start -n $ACT >/dev/null 2>&1
n=0
while [ $n -lt 300 ]; do
  n=$((n+1))
  set -- $(ps -A -o PID,PPID,NAME 2>/dev/null | grep "$PKG" | awk '{print $1}')
  if [ $# -gt 1 ]; then
    main=$1
    for p in $@; do
      if [ "$p" != "$main" ]; then
        echo "kill child $p (main=$main) at n=$n"
        kill -9 $p 2>/dev/null
      fi
    done
  fi
  if [ $# -eq 0 ] && [ $n -gt 20 ]; then
    echo "no proc at n=$n"
    break
  fi
  sleep 0.1
done
echo "--- pids now: $(ps -A -o PID,PPID,NAME | grep $PKG | tr '\n' '|')"
echo "--- pidof: $(pidof $PKG)"
