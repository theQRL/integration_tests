# coding=utf-8
# Distributed under the MIT software license, see the accompanying
# file LICENSE or http://www.opensource.org/licenses/mit-license.php.
import os
import subprocess
from unittest import TestCase

from mocknet.MockNet import MockNet
from mocknet.NodeTracker import NodeLogTracker

from validators.StateValidator import StateValidator

TIMEOUT = 240
LAST_BLOCK_NUMBER = 201
LAST_BLOCK_HEADERHASH = '751cf57a7c022c3bb43a62d13047844a9f10c00a2717850ad9738cb15a463159'

ADDR_1 = '01060019f902ffbba4afd07fa2a75dacd9580d342a0e714610869b0b3d0b134abb56d16cc85924'
BALANCE_1 = 662285701845
TX_COUNT_1 = 102

ADDR_2 = '0106001a1bbb8e5df52a3befb27a3ed3caa253d2a712e02e8606cf202fd8b3971189dfc27893d3'
BALANCE_2 = 665618275821
TX_COUNT_2 = 100


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

    def _verify_address_state(self, address_state, balance, txn_count):
        if address_state.balance != balance:
            raise Exception('Expected Balance %s \n Found balance %s',
                            balance,
                            address_state.balance)

        if len(address_state.transaction_hashes) != txn_count:
            raise Exception('Expected Balance %s \n Found balance %s',
                            txn_count,
                            len(address_state.transaction_hashes))

    def test_fork_recovery(self):
        def func_monitor_log():
            node_tracker = NodeLogTracker(mocknet)
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
