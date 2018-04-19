# coding=utf-8
# Distributed under the MIT software license, see the accompanying
# file LICENSE or http://www.opensource.org/licenses/mit-license.php.
import time
import os
import subprocess
import grpc
from queue import Empty
from unittest import TestCase

from mocknet.mocknet import MockNet
from mocknet.NodeTracker import NodeLogTracker

from pyqrllib.pyqrllib import hstr2bin, bin2hstr

from qrl.generated import qrl_pb2_grpc, qrl_pb2


LAST_BLOCK_NUMBER = 201
LAST_BLOCK_HEADERHASH = '7132f0828a2689bff7c563b2ad941092525e48e6afb66bf62a4311d3e438495e'


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
        timeout = 120

        def state_check():
            public_api_addresses = mocknet.public_addresses
            for public_api_address in public_api_addresses:
                channel_public = grpc.insecure_channel(public_api_address)
                stub = qrl_pb2_grpc.PublicAPIStub(channel_public)

                # TODO: Check coins emitted, coins total supply, epoch, block_last_reward
                # response = stub.GetStats(request=qrl_pb2.GetStatsReq())

                response = stub.GetNodeState(request=qrl_pb2.GetNodeStateReq())
                if response.info.block_height != LAST_BLOCK_NUMBER:
                    raise Exception('Expected Blockheight %s \n Found blockheight %s',
                                    LAST_BLOCK_NUMBER,
                                    response.info.block_height)

                if response.info.block_last_hash != bytes(hstr2bin(LAST_BLOCK_HEADERHASH)):
                    raise Exception('Last Block Headerhash mismatch\n'
                                    'Expected : %s\n', bin2hstr(response.info.block_last_hash),
                                    'Found : %s ', LAST_BLOCK_HEADERHASH)

                return True

        def func_monitor_log():
            node_tracker = NodeLogTracker(mocknet)
            while mocknet.running:
                msg = node_tracker.track()
                if "Added Block #{0} {1}".format(LAST_BLOCK_NUMBER, LAST_BLOCK_HEADERHASH) in msg:
                    state_check()
                    return

        mocknet = MockNet(func_monitor_log,
                          timeout_secs=timeout,
                          node_count=2,
                          node_args="--mockGetMeasurement 1000000000",
                          remove_data=False)

        mocknet.prepare_source()
        mocknet.run()
