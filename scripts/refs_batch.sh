set -x
D=/opt/anaconda3/bin/droidasc
A=chaoxing/out/unpacked.apk
mkdir -p chaoxing/out/refs
for s in "usersign/addsign?" "newsign/studentSign" "sign/produceSignView" "activePrimaryId" "&loctype=" "ifTiJiao" "clientip" "&ctype=stusign"; do
  f=$(echo "$s" | tr '/&?=' '____')
  timeout 300 $D findrefs $A string "$s" -o chaoxing/out/refs/$f.txt >> chaoxing/out/refs/log.txt 2>&1
  echo "=== $s rc=$? lines=$(wc -l < chaoxing/out/refs/$f.txt 2>/dev/null)" >> chaoxing/out/refs/log.txt
done
echo ALLDONE
