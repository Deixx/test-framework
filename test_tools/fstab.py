#
# Copyright(c) 2019-2021 Intel Corporation
# Copyright(c) 2024 Huawei Technologies Co., Ltd.
# SPDX-License-Identifier: BSD-3-Clause
#

from test_tools import fs_tools, systemctl


def add_mountpoint(device, mount_point, fs_type, mount_now=True):
    fs_tools.append_line("/etc/fstab",
                         f"{device.path} {mount_point} {fs_type.name} defaults 0 0")
    systemctl.reload_daemon()
    if mount_now:
        systemctl.restart_service("local-fs.target")


def remove_mountpoint(device):
    fs_tools.remove_lines("/etc/fstab", device.path)
    systemctl.reload_daemon()
