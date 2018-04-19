# coding=utf-8
# Distributed under the MIT software license, see the accompanying
# file LICENSE or http://www.opensource.org/licenses/mit-license.php.
from unittest import TestCase

from mocknet.mocknet import MockNet
from mocknet.NodeTracker import NodeLogTracker


class TestMocknetSync(TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_launch_log_nodes(self):
        def func_monitor_log():
            node_logtracker = NodeLogTracker(mocknet)

            while mocknet.running:
                node_logtracker.track()
                if node_logtracker.synced_count() == mocknet.node_count:
                    return

        mocknet = MockNet(func_monitor_log,
                          timeout_secs=60,
                          node_count=3)

        mocknet.prepare_source()
        mocknet.run()
