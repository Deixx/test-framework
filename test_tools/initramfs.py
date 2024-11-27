#
# Copyright(c) 2024 Huawei Technologies Co., Ltd.
# SPDX-License-Identifier: BSD-3-Clause
#

from core.test_run import TestRun
from test_utils.os_utils import get_distro, Distro


def update():
    distro = get_distro()
    TestRun.LOGGER.info("Updating initramfs")
    match distro:
        case Distro.DEBIAN | Distro.UBUNTU:
            TestRun.executor.run_expect_success("update-initramfs -u")
        case Distro.OPENEULER | Distro.CENTOS | Distro.REDHAT:
            TestRun.executor.run_expect_success(
                "dracut -f /boot/initramfs-$(uname -r).img $(uname -r)"
            )
