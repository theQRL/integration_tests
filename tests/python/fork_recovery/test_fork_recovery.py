# coding=utf-8
# Distributed under the MIT software license, see the accompanying
# file LICENSE or http://www.opensource.org/licenses/mit-license.php.
import os
import subprocess
from unittest import TestCase

from mocknet.MockNet import MockNet
from mocknet.NodeTracker import NodeLogTracker

from validators.StateValidator import StateValidator

TIMEOUT = 600  # Increased to 10 minutes for CI stability
LAST_BLOCK_NUMBER = 201
LAST_BLOCK_HEADERHASH = '751cf57a7c022c3bb43a62d13047844a9f10c00a2717850ad9738cb15a463159'


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

    def test_fork_recovery(self):
        def func_monitor_log():
            # Use longer timeout for block addition in fork recovery test
            node_tracker = NodeLogTracker(mocknet, max_no_addition_time=600)
            while mocknet.running:
                msg = node_tracker.track()
                if "Added Block #{0} {1}".format(LAST_BLOCK_NUMBER, LAST_BLOCK_HEADERHASH) in msg:
                    StateValidator(mocknet.debug_addresses).validate_state()
                    return

        mocknet = MockNet(func_monitor_log,
                          timeout_secs=TIMEOUT,
                          node_count=2,
                          node_args="--mockGetMeasurement 10000000000",
                          remove_data=False)

        mocknet.prepare_source()
        mocknet.run()
