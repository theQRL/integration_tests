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
            # Use longer timeout for block addition in 10-minute test (3 minutes)
            node_logtracker = NodeLogTracker(mocknet, max_no_addition_time=180)

            while mocknet.uptime < 600:
                node_logtracker.track()
                node_logtracker.check_idle_nodes()
                node_logtracker.check_last_addition()

        mocknet = MockNet(func_monitor_log,
                          timeout_secs=630,
                          node_count=10,
                          node_args="--mocknet")

        mocknet.prepare_source()
        mocknet.run()
