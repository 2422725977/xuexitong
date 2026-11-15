#!/usr/bin/env bash
# fsd.sh -- 低暴露地启停 frida-server
#   ./fsd.sh status | start [PORT] | stop
set -u
PORT="${2:-39042}"
BIN=/data/local/tmp/fsd
ADB="$(command -v adb || echo /opt/homebrew/share/android-commandlinetools/platform-tools/adb)"
case "${1:-status}" in
  status)
    echo "== 进程 =="; "$ADB" shell "ps -A 2>/dev/null | grep -iE 'frida|fsd' | head -5" || true
    echo "== 监听 =="; "$ADB" shell "netstat -ltn 2>/dev/null | grep -E '27042|39042' | head -6" || true
    echo "== 转发 =="; "$ADB" forward --list || true
    ;;
  start)
    "$ADB" root >/dev/null 2>&1 || true
    "$ADB" shell "killall fsd frida-server 2>/dev/null; sleep 0.3"
    "$ADB" shell "nohup $BIN -l 127.0.0.1:$PORT >/dev/null 2>&1 &"
    sleep 1
    "$ADB" forward "tcp:$PORT" "tcp:$PORT" >/dev/null
    echo "[fsd] started port $PORT (127.0.0.1 only)"
    ;;
  stop)
    "$ADB" shell "killall fsd frida-server 2>/dev/null" || true
    "$ADB" forward --remove-all >/dev/null 2>&1 || true
    echo "[fsd] stopped"
    ;;
  *) echo "usage: $0 {status|start [PORT]|stop}"; exit 1 ;;
esac
