set -e
D=/opt/anaconda3/bin/droidasc
A=chaoxing/out/unpacked.apk
S=chaoxing/out/src
for t in "Lcom/chaoxing/mobile/sign/ui/SignInfoActivity\$d;" "Lcom/chaoxing/mobile/sign/ui/SignInfoActivity\$e;" "Lcom/chaoxing/mobile/s;" "Lcom/chaoxing/beacon/BluetoothSignEntity;" "Lcom/chaoxing/beacon/BluetoothScanner;"; do
  n=$(echo "$t" | sed 's/^L//; s/;$//' | tr '/$' '__')
  timeout 900 $D getclass $A "$t" -o "$S/$n.java" >> chaoxing/out/refs2/getclass.log 2>&1 || echo "FAIL $t" >> chaoxing/out/refs2/getclass.log
  echo "=== $n $(wc -l < "$S/$n.java" 2>/dev/null || echo 0)" >> chaoxing/out/refs2/getclass.log
done
echo GETCLASSDONE
