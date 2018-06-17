# coding=utf-8
# Distributed under the MIT software license, see the accompanying
# file LICENSE or http://www.opensource.org/licenses/mit-license.php.
from unittest import TestCase

from mocknet.MockNet import MockNet
from mocknet.NodeTracker import NodeLogTracker


class TestMocknet10Min(TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_launch_log_nodes(self):
        def func_monitor_log():
            node_logtracker = NodeLogTracker(mocknet)

            while mocknet.uptime < 120:
                node_logtracker.track()

        mocknet = MockNet(func_monitor_log,
                          timeout_secs=150,
                          node_count=5,
                          node_args="--mocknet")

        mocknet.prepare_source()
        mocknet.run()
