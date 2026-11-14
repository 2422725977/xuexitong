#!/usr/bin/env bash
# fsd.sh —— 低暴露地启停 frida-server（学习通风控眼里 frida 是显性特征：能不用就不用，用就短命）
#
#   ./fsd.sh status          看当前有没有在跑、监听哪个端口
#   ./fsd.sh start [PORT]    默认 39042（避开 27042 这个 frida 默认端口指纹），只监听 127.0.0.1
#   ./fsd.sh stop            杀掉进程 + 撤掉 adb forward + 删掉落盘的抓取文件
#
# 用非默认端口后，frida 要显式连端口：
#   frida -H 127.0.0.1:39042 -f com.chaoxing.mobile -l scripts/masquerade.js -l scripts/frida_video_hook.js --no-pause
set -u
PORT="${2:-39042}"
BIN=/data/local/tmp/fsd
ADB="$(command -v adb || echo /opt/homebrew/share/android-commandlinetools/platform-tools/adb)"

case "${1:-status}" in
  status)
    echo "== 进程 =="
    "$ADB" shell "ps -A 2>/dev/null | grep -iE 'frida|fsd' | head -5" || true
    echo "== 监听 =="
    "$ADB" shell "netstat -ltn 2>/dev/null | grep -E '27042|39042' | head -6" || true
    echo "== 端口转发 =="
    "$ADB" forward --list || true
    echo "== 落盘产物 =="
    "$ADB" shell "ls -l /data/local/tmp/cx_*.jsonl 2>/dev/null" || true
    ;;
  start)
    "$ADB" root >/dev/null 2>&1 || true
    "$ADB" shell "killall fsd frida-server 2>/dev/null; sleep 0.3"
    "$ADB" shell "nohup $BIN -l 127.0.0.1:$PORT >/dev/null 2>&1 &"
    sleep 1
    "$ADB" forward "tcp:$PORT" "tcp:$PORT" >/dev/null
    echo "[fsd] 已启动，端口 $PORT（仅 127.0.0.1）"
    echo "[fsd] 接法: frida -H 127.0.0.1:$PORT -f com.chaoxing.mobile -l scripts/masquerade.js -l scripts/frida_video_hook.js --no-pause"
    echo "[fsd] 抓完立刻 ./fsd.sh stop —— 别让它常驻"
    ;;
  stop)
    "$ADB" shell "killall fsd frida-server 2>/dev/null" || true
    "$ADB" forward --remove "tcp:$PORT" >/dev/null 2>&1 || true
    "$ADB" forward --remove-all >/dev/null 2>&1 || true
    "$ADB" shell "rm -f /data/local/tmp/cx_video_cap.jsonl /data/local/tmp/cx_cap.jsonl" || true
    echo "[fsd] 已停 + 转发已撤 + 抓取文件已删"
    ;;
  *)
    echo "用法: $0 {status|start [PORT]|stop}"; exit 1 ;;
esac
