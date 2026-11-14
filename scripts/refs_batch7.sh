set -e
D=/opt/anaconda3/bin/droidasc
A=chaoxing/out/unpacked.apk
mkdir -p chaoxing/out/refs7
timeout 600 $D findrefs $A type com.chaoxing.beacon -o chaoxing/out/refs7/beacon_refs.txt >> chaoxing/out/refs7/log.txt 2>&1 || true
echo B7DONE
