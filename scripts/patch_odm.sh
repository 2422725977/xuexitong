#!/system/bin/sh
f=/vendor/odm/etc/build.prop
echo "=== BEFORE ==="; cat $f
cp -f $f /data/local/tmp/bak_odm_build.prop
sed -i \
  -e 's#Android/sdk_phone64_arm64/emulator64_arm64:10/QSR1.211112.002/7910984:userdebug/test-keys#google/coral/coral:10/QQ3A.200805.001/6578210:user/release-keys#g' \
  -e 's#^ro\.odm\.build\.tags=test-keys#ro.odm.build.tags=release-keys#' \
  -e 's#^ro\.odm\.build\.id=.*#ro.odm.build.id=QQ3A.200805.001#' \
  -e 's#^ro\.odm\.build\.version\.incremental=.*#ro.odm.build.version.incremental=6578210#' \
  -e 's#^ro\.odm\.build\.type=.*#ro.odm.build.type=user#' \
  -e 's#^ro\.product\.odm\.brand=.*#ro.product.odm.brand=google#' \
  -e 's#^ro\.product\.odm\.device=.*#ro.product.odm.device=coral#' \
  -e 's#^ro\.product\.odm\.manufacturer=.*#ro.product.odm.manufacturer=Google#' \
  -e 's#^ro\.product\.odm\.model=.*#ro.product.odm.model=Pixel 4#' \
  -e 's#^ro\.product\.odm\.name=.*#ro.product.odm.name=coral#' \
  -e 's#^ro\.build\.product=.*#ro.build.product=coral#' \
  -e 's#^ro\.product\.brand=.*#ro.product.brand=google#' \
  -e 's#^ro\.product\.device=.*#ro.product.device=coral#' \
  -e 's#^ro\.product\.manufacturer=.*#ro.product.manufacturer=Google#' \
  -e 's#^ro\.product\.model=.*#ro.product.model=Pixel 4#' \
  -e 's#^ro\.product\.name=.*#ro.product.name=coral#' \
  -e 's#^ro\.product\.board=.*#ro.product.board=coral#' \
  -e 's#^ro\.serialno=.*#ro.serialno=0A1B2C3D4E5F#' \
  $f
echo "rc=$? patched odm"
echo "=== AFTER ==="; cat $f