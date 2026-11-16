#!/bin/bash
# cx29/cx3x 模拟器"去模拟器化"脚本（学习通 6.7.8 启动自毁对抗）
# 用法: emu_sanitize.sh [serial] [--skip-reboot] [--mounts-only]
set -u
SDK=${SDK:-/opt/homebrew/share/android-commandlinetools}
export PATH=$SDK/platform-tools:$PATH
SER="emulator-5554"; MODE=full
for a in "$@"; do case "$a" in --skip-reboot) MODE=no_reboot;; --mounts-only) MODE=mounts;; *) SER="$a";; esac; done
D="-s $SER"
HERE=$(cd "$(dirname "$0")" && pwd)/emulator

apply_mounts() {
  adb $D push $HERE/proc_version /data/local/tmp/proc_version >/dev/null 2>&1
  adb $D push $HERE/proc_cpuinfo /data/local/tmp/proc_cpuinfo >/dev/null 2>&1
  adb $D shell "chmod 644 /data/local/tmp/proc_version /data/local/tmp/proc_cpuinfo
setenforce 0 2>/dev/null
chcon u:object_r:proc_version:s0 /data/local/tmp/proc_version 2>/dev/null
chcon u:object_r:proc_cpuinfo:s0 /data/local/tmp/proc_cpuinfo 2>/dev/null
setenforce 1 2>/dev/null
mount -o bind /data/local/tmp/proc_version /proc/version 2>/dev/null
mount -o bind /data/local/tmp/proc_cpuinfo /proc/cpuinfo 2>/dev/null
echo '--- /proc/version ->'; head -1 /proc/version
echo '--- cpuinfo Hardware ->'; grep -i hardware /proc/cpuinfo"
}

if [ "$MODE" = "mounts" ]; then apply_mounts; exit 0; fi

adb $D root >/dev/null 2>&1; sleep 2
adb $D remount 2>&1 | grep -iE "succeed|fail" || true

echo '=== 1) build.prop 去模拟器化'
adb $D shell "cp -n /system/build.prop /data/local/tmp/system_build.prop.orig 2>/dev/null; cp -n /vendor/build.prop /data/local/tmp/vendor_build.prop.orig 2>/dev/null; true"
adb $D push $HERE/system_build.prop /system/build.prop >/dev/null
adb $D push $HERE/vendor_build.prop /vendor/build.prop >/dev/null
adb $D shell "chown root:root /system/build.prop /vendor/build.prop; chmod 600 /system/build.prop /vendor/build.prop; setenforce 0 2>/dev/null; chcon u:object_r:system_file:s0 /system/build.prop; chcon u:object_r:vendor_file:s0 /vendor/build.prop; restorecon /system/build.prop /vendor/build.prop 2>/dev/null; setenforce 1 2>/dev/null; echo prop-ok"

echo '=== 2) 藏 su 二进制'
adb $D shell "mv /system/xbin/su /system/xbin/su.orig 2>/dev/null; /system/xbin/ls /system/xbin/ 2>/dev/null | grep -i '^su' || echo no-su-visible"

if [ "$MODE" = "no_reboot" ]; then echo '=== 跳过重启'; exit 0; fi
echo '=== 3) 重启 guest（保持 emulator 进程，overlay 不丢）'
adb $D reboot
sleep 20
adb -s $SER wait-for-device
for i in $(seq 1 30); do b=$(adb $D shell getprop sys.boot_completed 2>/dev/null | tr -d '\r'); [ "$b" = "1" ] && { echo "guest 重启完成 ($((i*8))s)"; break; }; sleep 8; done
echo '=== 4) 校验伪装结果'
adb $D shell "getprop ro.product.model; getprop ro.product.manufacturer; getprop ro.product.brand; getprop ro.product.device; getprop ro.build.type; getprop ro.build.tags; getprop ro.build.fingerprint; getprop ro.boot.hardware; getprop ro.hardware; getprop ro.kernel.qemu; getprop ro.serialno; getprop ro.bootloader" | tr -d '\r'
apply_mounts
