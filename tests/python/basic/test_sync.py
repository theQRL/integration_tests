# coding=utf-8
# Distributed under the MIT software license, see the accompanying
# file LICENSE or http://www.opensource.org/licenses/mit-license.php.
import time
from queue import Empty
from unittest import TestCase

from mocknet.mocknet import MockNet
from mocknet.NodeTracker import NodeLogTracker


class TestMocknetSync(TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_launch_log_nodes(self):
        timeout = 120

        def func_monitor_log():
            running_time = timeout
            start = time.time()
            node_tracker = NodeLogTracker()

            while time.time() - start < running_time:
                try:
                    msg = mocknet.log_queue.get(block=True, timeout=1)
                    print(msg, end='')
                    node_tracker.parse(msg)

                    if node_tracker.get_status('Node 0') == 'synced' and \
                       node_tracker.get_status('Node 1') == 'synced' and \
                       node_tracker.get_status('Node 2') == 'synced':
                        return
                except Empty:
                    pass

        mocknet = MockNet(func_monitor_log,
                          timeout_secs=timeout,
                          node_count=3)

        mocknet.prepare_source()
        mocknet.run()
