set -e
D=/opt/anaconda3/bin/droidasc
A=chaoxing/out/unpacked.apk
mkdir -p chaoxing/out/src2
timeout 900 $D getclass $A 'Lcom/chaoxing/mobile/webapp/jsprotocal/common/j0;' -o chaoxing/out/src2/j0.java >> chaoxing/out/refs8/gc2.log 2>&1 || true
timeout 900 $D getclass $A 'Lcom/chaoxing/mobile/webapp/jsprotocal/common/j0\$a;' -o chaoxing/out/src2/j0_a.java >> chaoxing/out/refs8/gc2.log 2>&1 || true
timeout 600 $D findrefs $A string bluetooth -o chaoxing/out/refs8/bluetooth_str.txt >> chaoxing/out/refs8/gc2.log 2>&1 || true
echo GC2DONE
