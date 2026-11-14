set -e
D=/opt/anaconda3/bin/droidasc
A=chaoxing/out/unpacked.apk
mkdir -p chaoxing/out/refs3
timeout 600 $D findrefs $A method I7 --class com.chaoxing.mobile.s -o chaoxing/out/refs3/I7_callers.txt >> chaoxing/out/refs3/log.txt 2>&1 || true
timeout 600 $D findrefs $A method G6 --class com.chaoxing.mobile.s -o chaoxing/out/refs3/G6_callers.txt >> chaoxing/out/refs3/log.txt 2>&1 || true
echo CALLERSDONE
