# LOONGARCH Architecture definition

DEFAULTTUNE ?= "loongarch64"

TUNE_ARCH = "${TUNE_ARCH:tune-${DEFAULTTUNE}}"
TUNE_PKGARCH = "${TUNE_PKGARCH:tune-${DEFAULTTUNE}}"
