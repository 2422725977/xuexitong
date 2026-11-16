#!/usr/bin/env bash
# USB 抓包：adb reverse + 设备全局代理 -> 本机 mitmproxy
# 用法: bash mitm_capture.sh start | stop
set -u
CMD="${1:-start}"
PORT="${PORT:-8080}"
HERE="$(cd "$(dirname "$0")/../.." && pwd)"
OUT="$HERE/out/mitm"
case "$CMD" in
  start)
    mkdir -p "$OUT"
    adb reverse tcp:$PORT tcp:$PORT
    adb shell settings put global http_proxy 127.0.0.1:$PORT
    echo '[+] 设备代理 -> 127.0.0.1:'$PORT'（走 USB adb reverse，不用改 WiFi）'
    echo '[+] 证书：装上 mitmproxy-ca-cert.cer；Android 7+ 的 App 不信任用户 CA，原生请求会 TLS 失败（要 root 装系统证书）'
    echo '[+] 抓包文件: '$OUT'/chx.flow   （Ctrl-C 结束）'
    exec mitmproxy --listen-port $PORT --save-stream-file "$OUT/chx.flow"
    ;;
  stop)
    adb shell settings put global http_proxy :0
    adb reverse --remove tcp:$PORT 2>/dev/null || true
    echo '[+] 已恢复（http_proxy=:0，reverse 已移除）'
    ;;
  *) echo "用法: bash mitm_capture.sh start|stop"; exit 1;;
esac