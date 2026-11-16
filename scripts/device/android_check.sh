#!/usr/bin/env bash
# 学习通真机环境自检：adb / 机型 / root / 包 / 代理现状
set -u
SER="${1:-}"
if [ -n "$SER" ]; then ADB="adb -s $SER"; else ADB="adb"; fi
echo '== devices =='; adb devices -l
echo; echo '== 机型与系统 =='
$ADB shell 'getprop ro.product.model; getprop ro.product.brand; getprop ro.product.device; getprop ro.build.version.release; getprop ro.build.version.sdk; getprop ro.build.type; getprop ro.debuggable; getprop ro.secure; getprop ro.product.cpu.abi; getprop ro.build.fingerprint' 2>&1
echo; echo '== root 判定（uid=0 才是 root）=='
$ADB shell 'id; (command -v su >/dev/null && su -c id) 2>/dev/null; (magisk -v 2>/dev/null) || echo no-magisk' 2>&1
echo; echo '== 学习通是否安装 =='
$ADB shell 'pm list packages -f | grep -i chaoxing' 2>&1
echo; echo '== 当前全局代理 =='
$ADB shell 'settings get global http_proxy' 2>&1
echo; echo '== WebView 版本（影响 chrome://inspect）=='
$ADB shell 'dumpsys webviewupdate | head -20' 2>&1
echo; echo '把上面整段回给我：机型 / 系统版本 / 是否 root / 学习通是否已装'