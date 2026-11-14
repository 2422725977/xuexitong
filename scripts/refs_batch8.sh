set -e
D=/opt/anaconda3/bin/droidasc
A=chaoxing/out/unpacked.apk
mkdir -p chaoxing/out/refs8
timeout 600 $D findrefs $A impl com.chaoxing.beacon.i -o chaoxing/out/refs8/beacon_i_impl.txt >> chaoxing/out/refs8/log.txt 2>&1 || true
timeout 600 $D findrefs $A type com.chaoxing.mobile.main.f -o chaoxing/out/refs8/mainf_refs.txt >> chaoxing/out/refs8/log.txt 2>&1 || true
echo B8DONE
