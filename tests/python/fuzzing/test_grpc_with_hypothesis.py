# coding=utf-8
# Distributed under the MIT software license, see the accompanying
# file LICENSE or http://www.opensource.org/licenses/mit-license.php.
import time
from queue import Empty
from random import choice
from unittest import TestCase

import grpc
from qrl.generated import qrl_pb2, qrl_pb2_grpc

from mocknet.mocknet import MockNet
from mocknet.NodeTracker import NodeLogTracker

from hypothesis_protobuf.module_conversion import modules_to_strategies

from collections import namedtuple

ReqAttrNames = namedtuple('ReqAttrNames', ['method', 'arg'])

PUBLIC_API_PORT = 9009
PASS_NUM = 100


class TestFuzzingAPI(TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_grpc_fuzzing(self):
        timeout = 60*15

        def func_monitor_log():
            node_tracker = NodeLogTracker(mocknet)

            while mocknet.uptime < 30:
                node_tracker.track()
                time.sleep(0.01)

            if node_tracker.synced_count() < mocknet.node_count:
                raise Exception("Nodes did not sync")

            protobuf_strategies = modules_to_strategies(qrl_pb2)
            publicapi = qrl_pb2._PUBLICAPI

            self.assertTrue(publicapi.methods, "methods is empty")
            req_attrs = []
            for m in publicapi.methods:
                req_attrs.append(ReqAttrNames(m.name, m.input_type.name))

            stubs = [
                qrl_pb2_grpc.PublicAPIStub(grpc.insecure_channel("127.0.0.1:10002"))
            ]

            while mocknet.uptime < 180:
                try:
                    node_tracker.track()
                    if node_tracker.synced_count() == mocknet.node_count:
                        for i in range(1, PASS_NUM):
                            rand_stub = choice(stubs)
                            rand_req = choice(req_attrs)
                            req_strategy = protobuf_strategies[getattr(qrl_pb2, rand_req.arg)]
                            req_arg = req_strategy.example()
                            req_method = getattr(rand_stub, rand_req.method)

                            try:
                                resp = req_method(req_arg)
                            except grpc.RpcError as err:
                                print('*******************************')
                                print("\nERROR: %s \n" % rand_req.method)
                                print(req_arg)
                                print('*******************************')
                                print(err)
#                                raise
                            except Exception as e:
                                pass
                            time.sleep(1)

                except Empty:
                    pass

        # Launch mocknet
        mocknet = MockNet(func_monitor_log,
                          timeout_secs=timeout,
                          node_count=2)

        mocknet.prepare_source()
        mocknet.run()
