#!/system/bin/sh
for f in /system/build.prop /vendor/build.prop /system/product/build.prop; do
  [ -f "$f" ] || continue
  case "$f" in */vendor/*) b=/data/local/tmp/bak_vendor_build.prop;; */product/*) b=/data/local/tmp/bak_product_build.prop;; *) b=/data/local/tmp/bak_system_build.prop;; esac
  [ -f "$b" ] || cp -f "$f" "$b"
  sed -i \
    -e 's#Android/sdk_phone64_arm64/emulator64_arm64:10/QSR1.211112.002/7910984:userdebug/test-keys#google/coral/coral:10/QQ3A.200805.001/6578210:user/release-keys#g' \
    -e 's#^ro\.build\.characteristics=.*#ro.build.characteristics=nosdcard#' \
    -e 's#^ro\.build\.tags=test-keys#ro.build.tags=release-keys#' \
    -e 's#^ro\.system\.build\.tags=test-keys#ro.system.build.tags=release-keys#' \
    -e 's#^ro\.vendor\.build\.tags=test-keys#ro.vendor.build.tags=release-keys#' \
    -e 's#^ro\.product\.system\.brand=Android#ro.product.system.brand=google#' \
    -e 's#^ro\.product\.vendor\.brand=Android#ro.product.vendor.brand=google#' \
    -e 's#^ro\.product\.system\.manufacturer=unknown#ro.product.system.manufacturer=Google#' \
    -e 's#^ro\.product\.vendor\.manufacturer=unknown#ro.product.vendor.manufacturer=Google#' \
    -e 's#^ro\.product\.system\.model=.*#ro.product.system.model=Pixel 4#' \
    -e 's#^ro\.product\.vendor\.model=.*#ro.product.vendor.model=Pixel 4#' \
    -e 's#^ro\.product\.system\.device=.*#ro.product.system.device=coral#' \
    -e 's#^ro\.product\.vendor\.device=.*#ro.product.vendor.device=coral#' \
    -e 's#^ro\.product\.system\.name=.*#ro.product.system.name=coral#' \
    -e 's#^ro\.product\.vendor\.name=.*#ro.product.vendor.name=coral#' \
    -e 's#^ro\.product\.board=.*#ro.product.board=coral#' \
    -e 's#^ro\.board\.platform=.*#ro.board.platform=msmnile#' \
    -e 's#^ro\.build\.product=.*#ro.build.product=coral#' \
    -e 's#^ro\.build\.flavor=.*#ro.build.flavor=coral-user#' \
    -e 's#^ro\.build\.id=.*#ro.build.id=QQ3A.200805.001#' \
    -e 's#^ro\.system\.build\.id=.*#ro.system.build.id=QQ3A.200805.001#' \
    -e 's#^ro\.vendor\.build\.id=.*#ro.vendor.build.id=QQ3A.200805.001#' \
    -e 's#^ro\.build\.version\.incremental=.*#ro.build.version.incremental=6578210#' \
    -e 's#^ro\.system\.build\.version\.incremental=.*#ro.system.build.version.incremental=6578210#' \
    -e 's#^ro\.vendor\.build\.version\.incremental=.*#ro.vendor.build.version.incremental=6578210#' \
    -e 's#^ro\.build\.description=.*#ro.build.description=coral-user 10 QQ3A.200805.001 6578210 release-keys#' \
    -e 's#^ro\.build\.display\.id=.*#ro.build.display.id=QQ3A.200805.001#' \
    -e 's#^ro\.build\.host=.*#ro.build.host=abfarm730#' \
    -e 's#^ro\.hardware\.power=ranchu#ro.hardware.power=qcom#' \
    -e 's#^ro\.hwui\.use_vulkan=.*#ro.hwui.use_vulkan=0#' \
    -e 's#^ro\.kernel\.qemu=.*#ro.kernel.qemu=0#' \
    -e 's#^ro\.serialno=.*#ro.serialno=0A1B2C3D4E5F#' \
    "$f"
  echo "rc=$? $f"
done
grep -q "^service.adb.root" /system/build.prop || echo "service.adb.root=1" >> /system/build.prop
echo "=== after ==="
grep -nE "fingerprint|characteristics|tags|product\.(system|vendor)\.(brand|model|device|name|manufacturer)|product\.board|board\.platform|build\.(id|type|flavor|product|description)|kernel\.qemu|hardware\.power|adb\.root" /system/build.prop /vendor/build.prop /system/product/build.prop