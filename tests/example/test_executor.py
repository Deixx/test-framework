#
# Copyright(c) 2019 Intel Corporation
# SPDX-License-Identifier: BSD-3-Clause-Clear
#

import pytest

from utils.size import Size, Unit


def test_executor(get_dut, get_executor):
    executor = get_executor
    print(get_dut['ip'])
    assert executor is not None
    executor.execute('echo test > /dev/ttyS0')


@pytest.mark.parametrize('get_dut', [[
    "get-dut-with-disk-type-of-size", {
        "disk_type": "nand", "size": int(Size(100, Unit.GibiByte))}]], indirect=True)
def test_parametrized_auto_executor(get_dut, get_executor):
    executor = get_executor
    print(get_dut['ip'])
    executor.execute('echo test > /dev/ttyS0')
