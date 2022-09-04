# SPDX-License-Identifier: MIT
import os
import subprocess
from oeqa.core.decorator import OETestTag
from oeqa.core.case import OEPTestResultTestCase
from oeqa.selftest.case import OESelftestTestCase
from oeqa.utils.commands import runCmd, bitbake, get_bb_var, get_bb_vars, runqemu, Command
from oeqa.utils.sshcontrol import SSHControl

# Total time taken for testing is of about 2hr 20min, with PARALLEL_MAKE set to 40 number of jobs.
class RustSelfTestBase(OESelftestTestCase, OEPTestResultTestCase):

	def run_check_emulated(self, *args, **kwargs):
		# build remote-test-server before image build
		recipe = "rust"
		bitbake("{} -c test_compile".format(recipe))
		builddir = get_bb_var("RUSTSRC", "rust")
		# build core-image-minimal with required packages
		default_installed_packages = ["libgcc", "libstdc++", "libatomic", "libgomp"]
		features = []
		features.append('IMAGE_FEATURES += "ssh-server-openssh"')
		features.append('CORE_IMAGE_EXTRA_INSTALL += "{0}"'.format(" ".join(default_installed_packages)))
		self.write_config("\n".join(features))
		bitbake("core-image-minimal")
		# wrap the execution with a qemu instance.
                # Tests are run with 512 tasks in parallel to execute all tests very quickly
		with runqemu("core-image-minimal", runqemuparams = "nographic", qemuparams = "-m 512") as qemu:
			# Copy remote-test-server to image through scp
			ssh = SSHControl(ip=qemu.ip, logfile=qemu.sshlog, user="root")
			ssh.copy_to(builddir + "/" + "build/x86_64-unknown-linux-gnu/stage1-tools-bin/remote-test-server","~/")
			# Execute remote-test-server on image through background ssh
			command = '~/remote-test-server -v remote'
			sshrun=subprocess.Popen(("ssh", '-o',  'UserKnownHostsFile=/dev/null', '-o',  'StrictHostKeyChecking=no', '-f', "root@%s" % qemu.ip, command),
                                shell=False,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
			# Get the values of variables.
			tcpath = get_bb_var("TARGET_SYS", "rust")
			targetsys = get_bb_var("RUST_TARGET_SYS", "rust")
			rustlibpath = get_bb_var("WORKDIR", "rust")
			tmpdir = get_bb_var("TMPDIR", "rust")

			# Exclude the test folders that error out while building
                        # TODO: Fix the errors and include them for testing
                        # no-fail-fast: Run all tests regardless of failure.
                        # bless: First runs rustfmt to format the codebase,
                        # then runs tidy checks.
			testargs = "--exclude src/test/rustdoc --exclude src/test/rustdoc-json  --exclude src/test/run-make-fulldeps --exclude src/tools/tidy --exclude src/tools/rustdoc-themes --exclude src/rustdoc-json-types --exclude src/librustdoc --exclude src/doc/unstable-book --exclude src/doc/rustdoc --exclude src/doc/rustc --exclude compiler/rustc --exclude library/panic_abort --exclude library/panic_unwind --exclude src/test/rustdoc --no-doc --no-fail-fast --bless"

			# Set path for target-poky-linux-gcc, RUST_TARGET_PATH and hosttools.
			cmd = " export PATH=%s/recipe-sysroot-native/usr/bin:$PATH;" % rustlibpath
			cmd = cmd + " export TARGET_VENDOR=\"-poky\";"
			cmd = cmd + " export PATH=%s/recipe-sysroot-native/usr/bin/%s:%s/hosttools:$PATH;" % (rustlibpath, tcpath, tmpdir)
			cmd = cmd + " export RUST_TARGET_PATH=%s/rust-targets;" % rustlibpath
			# Trigger testing.
			cmd = cmd + " export TEST_DEVICE_ADDR=\"%s:12345\";" % qemu.ip
			cmd = cmd + " cd %s;  python3 src/bootstrap/bootstrap.py test %s --target %s ;" % (builddir, testargs, targetsys)
			result = runCmd(cmd)

@OETestTag("toolchain-system")
class RustSelfTestSystemEmulated(RustSelfTestBase):
	def test_rust(self):
		self.run_check_emulated("rust")
