set -e
D=/opt/anaconda3/bin/droidasc
A=chaoxing/out/unpacked.apk
mkdir -p chaoxing/out/refs5
timeout 600 $D findrefs $A method a --class com.chaoxing.mobile.sign.util.b -o chaoxing/out/refs5/utilb_a_callers.txt >> chaoxing/out/refs5/log.txt 2>&1 || true
timeout 600 $D findrefs $A type com.chaoxing.mobile.sign.util -o chaoxing/out/refs5/signutil_refs.txt >> chaoxing/out/refs5/log.txt 2>&1 || true
echo B5DONE
