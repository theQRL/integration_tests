# coding=utf-8
# Distributed under the MIT software license, see the accompanying
# file LICENSE or http://www.opensource.org/licenses/mit-license.php.
import time
from unittest import TestCase

from mocknet.mocknet import MockNet


def func_blocks():
    time.sleep(100)


def func_raises_value_error():
    time.sleep(1)
    raise ValueError("test")


def func_no_issues():
    print("OK")


class TestMocknetHelpers(TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_timeout(self):
        mocknet = MockNet(func_blocks,
                          timeout_secs=2,
                          nodes=0)
        with self.assertRaises(TimeoutError):
            mocknet.run()

    def test_exception(self):
        mocknet = MockNet(func_raises_value_error,
                          timeout_secs=10,
                          nodes=0)

        with self.assertRaises(ValueError):
            mocknet.run()

    def test_works_ok(self):
        mocknet = MockNet(func_no_issues,
                          timeout_secs=10,
                          nodes=0)
        mocknet.run()

    def test_launch_1_node(self):
        mocknet = MockNet(func_no_issues,
                          timeout_secs=3,
                          nodes=1)
        mocknet.run()
