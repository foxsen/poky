require conf/machine/include/loongarch/arch-loongarch64.inc

TUNEVALID[loongarch64] = "Enable 64-bit LOONGARCH optimizations"

AVAILTUNES += "loongarch64"

# Default
TUNE_FEATURES:tune-loongarch64 = "loongarch64"
TUNE_ARCH:tune-loongarch64 = "loongarch64"
TUNE_PKGARCH:tune-loongarch64 = "loongarch64"
PACKAGE_EXTRA_ARCHS:tune-loongarch64 = "loongarch64"
