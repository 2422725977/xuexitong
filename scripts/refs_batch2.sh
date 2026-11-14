set -e
D=/opt/anaconda3/bin/droidasc
A=chaoxing/out/unpacked.apk
mkdir -p chaoxing/out/refs2
for s in "signType" "rcode=" "newsign" "gotasksign" "preSign" "signId" "loctype" "lat:" "sign/sign" "studentSign"; do
  f=$(echo "$s" | tr '/&?=: ' '______')
  timeout 600 $D findrefs $A string "$s" -o chaoxing/out/refs2/$f.txt >> chaoxing/out/refs2/log.txt 2>&1 || echo "FAIL $s" >> chaoxing/out/refs2/log.txt
  echo "=== $s $(wc -l < chaoxing/out/refs2/$f.txt 2>/dev/null)" >> chaoxing/out/refs2/log.txt
done
echo REFSDONE
