set -e
D=/opt/anaconda3/bin/droidasc
A=chaoxing/out/unpacked.apk
mkdir -p chaoxing/out/refs6
timeout 600 $D findrefs $A type com.chaoxing.mobile.sign.ui -o chaoxing/out/refs6/signui_refs.txt >> chaoxing/out/refs6/log.txt 2>&1 || true
timeout 600 $D findrefs $A type com.chaoxing.mobile.sign.LocationPoi -o chaoxing/out/refs6/poi_refs.txt >> chaoxing/out/refs6/log.txt 2>&1 || true
timeout 600 $D findrefs $A method q --class com.chaoxing.mobile.s -o /dev/null >> chaoxing/out/refs6/log.txt 2>&1 || true
echo B6DONE
