# coding=utf-8
# Distributed under the MIT software license, see the accompanying
# file LICENSE or http://www.opensource.org/licenses/mit-license.php.
import time
import os
import subprocess
from queue import Empty
from unittest import TestCase

from mocknet.mocknet import MockNet
from mocknet.NodeTracker import NodeLogTracker


class TestMocknetForkRecovery(TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.this_file = os.path.realpath(__file__)
        self.this_dir = os.path.dirname(self.this_file)
        self.script_dir = os.path.join(self.this_dir, 'scripts')
        self.execute_scripts("prepare_data.sh")

    def execute_scripts(self, script_file):
        cmd = "{0}/{1}".format(self.script_dir, script_file)
        p = subprocess.Popen(cmd, shell=True)
        p.wait()

    def test_launch_log_nodes(self):
        timeout = 1200

        def func_monitor_log():
            running_time = timeout
            start = time.time()
            node_tracker = NodeLogTracker()

            while time.time() - start < running_time:
                try:
                    msg = mocknet.log_queue.get(block=True, timeout=1)
                    print(msg, end='')
                    node_tracker.parse(msg)

                    if "Received Block #201 7132f0828a2689bff7c563b2ad941092525e48e6afb66bf62a4311d3e438495e" in msg:
                        return

                except Empty:
                    pass

        mocknet = MockNet(func_monitor_log,
                          timeout_secs=timeout,
                          node_count=2,
                          remove_data=False)

        mocknet.prepare_source()
        mocknet.run()
