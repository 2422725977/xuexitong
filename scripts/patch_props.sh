#!/system/bin/sh
FP_OLD=Android/sdk_phone64_arm64/emulator64_arm64:10/QSR1.211112.002/7910984:userdebug/test-keys
FP_NEW=google/coral/coral:10/QQ3A.200805.001/6578210:user/release-keys
for f in /system/build.prop /vendor/build.prop /system/product/build.prop /system/odm/build.prop; do
  [ -f "$f" ] || continue
  case "$f" in /vendor/*) b=/data/local/tmp/vendor_build.prop.bak;; /system/product/*) b=/data/local/tmp/product_build.prop.bak;; /system/odm/*) b=/data/local/tmp/odm_build.prop.bak;; *) b=/data/local/tmp/system_build.prop.bak;; esac
  [ -f "$b" ] || cp -f "$f" "$b"
  sed -i -e "s#$FP_OLD#$FP_NEW#g" \
    -e "s#^ro.build.characteristics=.*#ro.build.characteristics=nosdcard#" \
    -e "s#^ro.build.tags=test-keys#ro.build.tags=release-keys#" \
    -e "s#^ro.system.build.tags=test-keys#ro.system.build.tags=release-keys#" \
    -e "s#^ro.vendor.build.tags=test-keys#ro.vendor.build.tags=release-keys#" \
    -e "s#^ro.build.type=userdebug#ro.build.type=user#" \
    -e "s#^ro.vendor.build.type=userdebug#ro.vendor.build.type=user#" \
    -e "s#^ro.product.brand=Android#ro.product.brand=google#" \
    -e "s#^ro.product.system.brand=Android#ro.product.system.brand=google#" \
    -e "s#^ro.product.vendor.brand=Android#ro.product.vendor.brand=google#" \
    -e "s#^ro.product.manufacturer=unknown#ro.product.manufacturer=Google#" \
    -e "s#^ro.product.system.manufacturer=unknown#ro.product.system.manufacturer=Google#" \
    -e "s#^ro.product.vendor.manufacturer=unknown#ro.product.vendor.manufacturer=Google#" \
    -e "s#^ro.product.model=Android SDK built for arm64#ro.product.model=Pixel 4#" \
    -e "s#^ro.product.system.model=Android SDK built for arm64#ro.product.system.model=Pixel 4#" \
    -e "s#^ro.product.vendor.model=Android SDK built for arm64#ro.product.vendor.model=Pixel 4#" \
    -e "s#^ro.product.device=emulator64_arm64#ro.product.device=coral#" \
    -e "s#^ro.product.system.device=emulator64_arm64#ro.product.system.device=coral#" \
    -e "s#^ro.product.vendor.device=emulator64_arm64#ro.product.vendor.device=coral#" \
    -e "s#^ro.product.name=sdk_phone64_arm64#ro.product.name=coral#" \
    -e "s#^ro.product.system.name=sdk_phone64_arm64#ro.product.system.name=coral#" \
    -e "s#^ro.product.vendor.name=sdk_phone64_arm64#ro.product.vendor.name=coral#" \
    -e "s#^ro.product.board=goldfish_arm64#ro.product.board=coral#" \
    -e "s#^ro.board.platform=$#ro.board.platform=msmnile#" \
    -e "s#^ro.kernel.qemu=1#ro.kernel.qemu=0#" \
    -e "s#^ro.serialno=.*#ro.serialno=0A1B2C3D4E5F#" \
    -e "s#^ro.boot.serialno=.*#ro.boot.serialno=0A1B2C3D4E5F#" \
    -e "s#^ro.build.flavor=sdk_phone64_arm64-userdebug#ro.build.flavor=coral-user#" \
    -e "s#^ro.build.id=QSR1.211112.002#ro.build.id=QQ3A.200805.001#" \
    -e "s#^ro.build.vendor.id=QSR1.211112.002#ro.build.vendor.id=QQ3A.200805.001#" \
    -e "s#^ro.vendor.build.id=QSR1.211112.002#ro.vendor.build.id=QQ3A.200805.001#" \
    -e "s#^ro.build.description=.*#ro.build.description=coral-user 10 QQ3A.200805.001 6578210 release-keys#" \
    -e "s#^ro.build.version.incremental=7910984#ro.build.version.incremental=6578210#" \
    -e "s#^ro.vendor.build.version.incremental=7910984#ro.vendor.build.version.incremental=6578210#" \
    "$f"
  echo "patched $f"
done
echo "--- characteristics location ---"
grep -rn "characteristics" /system/build.prop /vendor/build.prop 2>/dev/null
echo "--- verify ---"
grep -nE "fingerprint|characteristics|build.tags|build.type|product.(brand|model|device|name|board)|serialno|board.platform|kernel.qemu|build.flavor|build.id|version.incremental" /system/build.prop /vendor/build.prop | grep -vE "^#|version.preview|security_patch"