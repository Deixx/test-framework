#
# Copyright(c) 2019 Intel Corporation
# SPDX-License-Identifier: BSD-3-Clause-Clear
#

import json
import logging
import socket

import pytest
import requests

import config.configuration as c
from connection.dummy_executor import DummyExecutor
from connection.local_executor import LocalExecutor
from connection.ssh_executor import SshExecutor


def pytest_addoption(parser):
    """
        Allows to pass CLI options for test execution
        --executor accepts { dummy | local | auto | <IP address> }, i.e. --executor=127.0.0.1
    """
    parser.addoption('--executor', action='store', default='dummy')


@pytest.fixture
def get_executor(request, get_dut):
    """
        Returns proper executor depending on CLI options and test restrictions
    """
    target = request.config.getoption('executor')
    if target == 'dummy':
        return DummyExecutor()
    elif target == 'local':
        return LocalExecutor()
    elif target == 'auto':
        ip = get_dut['ip']
        return SshExecutor(ip, c.user, c.password)  # Add credentials in config/configuration.py file
    else:
        try:
            socket.inet_aton(target)
            return SshExecutor(target, c.user, c.password)  # Add credentials in config/configuration.py file
        except socket.error:
            raise ValueError('Wrong --executor provided')


@pytest.fixture
def get_dut(request):
    """
        Dummy method mocking logic for superbburner DUT auto-selection
    """
    if hasattr(request, 'param'):
        for i in request.param:
            print(i)
        return sb_request(request.param[0], request.param[1])
    print('\nNo test restrictions set')
    # TODO return first available DUT or DUT with minimal configuration (like smallest disks, etc)
    return {'ip': c.dummy_ip}


LOGGER = logging.getLogger(__name__)


def sb_request(endpoint, body):
    data = json.dumps(body)
    session = requests.Session()
    session.trust_env = False
    r = session.post(c.API_ADDR + endpoint, data=data, headers={'content-type': 'application/json'})
    return r.json()


@pytest.fixture
def duts_with_disks_count():
    def get_duts(count, disk_type):
        return sb_request("get-dut-with-disks-count", {"count": count, "disk_type": str(disk_type)})

    return get_duts


@pytest.fixture
def duts_with_total_minimum_size():
    def get_duts(size):
        return sb_request("get-dut-with-total-minimum-size", {"size": size})

    return get_duts


@pytest.fixture
def duts_with_disk_type_total_min_size():
    def get_duts(disk_type, size):
        return sb_request("get-dut-with-disk-type-total-min-size", {"disk_type": disk_type, "size": size})

    return get_duts


@pytest.fixture
def duts_with_disk_type_of_size():
    def get_duts(disk_type, size):
        return sb_request("get-dut-with-disk-type-of-size", {"disk_type": disk_type, "size": size})

    return get_duts
