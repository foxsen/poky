require conf/machine/include/qemu.inc
require conf/machine/include/loongarch/tune-loongarch64.inc

MACHINE_FEATURES = "screen keyboard ext2 ext3 serial"

KERNEL_IMAGETYPE = "vmlinux.efi"
KEEPUIMAGE = "no"

SERIAL_CONSOLES ?= "115200;ttyS0 115200;ttyS1"
SERIAL_CONSOLES_CHECK = "${SERIAL_CONSOLES}"

IMAGE_FSTYPES += "ext4 wic.qcow2"

WKS_FILE ?= "qemuloongarch64.wks"

MACHINE_EXTRA_RRECOMMENDS += " kernel-modules"

# qemuboot options
QB_SMP = "-smp 1"
QB_MACHINE = "-machine virt"
QB_DEFAULT_BIOS = "QEMU_EFI.fd"
QB_TAP_OPT = "-netdev tap,id=net0,ifname=@TAP@,script=no,downscript=no"
QB_NETWORK_DEVICE = "-device virtio-net-pci,netdev=net0,mac=@MAC@"
QB_ROOTFS_OPT = "-drive id=disk0,file=@ROOTFS@,if=none,format=raw -device virtio-blk-pci,drive=disk0"
QB_SERIAL_OPT = "-device virtio-serial-device -chardev null,id=virtcon -device virtconsole,chardev=virtcon"
QB_TCPSERIAL_OPT = " -device virtio-serial-device -chardev socket,id=virtcon,port=@PORT@,host=127.0.0.1 -device virtconsole,chardev=virtcon"
#QB_GRAPHICS = "-device bochs-display"
QB_GRAPHICS = "-device virtio-vga -device qemu-xhci -device usb-kbd -device usb-mouse"
#QB_OPT_APPEND = "-device virtio-tablet-pci -device virtio-keyboard-pci"
QB_OPT_APPEND = "-device virtio-keyboard-pci"
QB_MEM = "-m 4G"
