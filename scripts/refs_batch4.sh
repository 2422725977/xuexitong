set -e
D=/opt/anaconda3/bin/droidasc
A=chaoxing/out/unpacked.apk
mkdir -p chaoxing/out/refs4
timeout 900 $D getclass $A 'Lcom/chaoxing/mobile/main/f;' -o chaoxing/out/src/com_chaoxing_mobile_main_f.java >> chaoxing/out/refs4/log.txt 2>&1 || true
for s in "&lat=" "&lon=" "&location=" "sign/produceSignView" ; do
  f=$(echo "$s" | tr '/&?=: ' '______')
  timeout 600 $D findrefs $A string "$s" -o chaoxing/out/refs4/$f.txt >> chaoxing/out/refs4/log.txt 2>&1 || true
done
echo B4DONE
