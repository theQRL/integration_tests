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
        timeout = 120

        def func_monitor_log():
            running_time = timeout
            start = time.time()
            node_tracker = NodeLogTracker()

            while time.time() - start < running_time:
                try:
                    msg = mocknet.log_queue.get(block=True, timeout=1)
                    node_tracker.parse(msg)
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
                                raise

                except Empty:
                    pass

        protobuf_strategies = modules_to_strategies(qrl_pb2)
        publicapi = qrl_pb2._PUBLICAPI

        self.assertTrue(publicapi.methods, "methods is empty")
        req_attrs = []
        for m in publicapi.methods:
            req_attrs.append(ReqAttrNames(m.name, m.input_type.name))

        stubs = [
            qrl_pb2_grpc.PublicAPIStub(grpc.insecure_channel("127.0.0.1:" + str(PUBLIC_API_PORT)))
        ]

        # Launch mocknet
        mocknet = MockNet(func_monitor_log,
                          timeout_secs=timeout,
                          node_count=2)

        mocknet.prepare_source()
        mocknet.run()

# PASS_NUM = 100
# import sys
# sys.path.append('..')
# import pytest
# import docker
# from random import choice
# import grpc
#
#
# from collections import namedtuple
# ReqAttrNames = namedtuple('ReqAttrNames', ['method', 'arg'])
#
# @pytest.mark.grpchypothesis
# def test_grpc_with_hypothesis():
#     protobuf_strategies = modules_to_strategies(qrl_pb2)
#     publicapi = qrl_pb2._PUBLICAPI
#     if(not publicapi.methods):
#         print("*******ASSERT: methods is empty ************")
#         assert False
#     req_attrs = []
#     for m in publicapi.methods:
#         req_attrs.append(ReqAttrNames(m.name, m.input_type.name))
#
#     def get_ip(container):
#         return container.attrs['NetworkSettings']['Networks']['qrlnet_default']['IPAddress']
#     stubs = []
#     for container in docker.from_env().containers.list():
#         channel = grpc.insecure_channel(get_ip(container) + ":" + str(PUBLIC_API_PORT))
#         stubs.append(qrl_pb2_grpc.PublicAPIStub(channel))
#     if not stubs:
#         print("*******ASSERT: stubs is empty ************")
#         assert False
#     success = True
#     for i in range(1, PASS_NUM):
#         rand_stub = choice(stubs)
#         rand_req = choice(req_attrs)
#         req_strategy = protobuf_strategies[getattr(qrl_pb2, rand_req.arg)]
#         req_arg = req_strategy.example()
#         req_method = getattr(rand_stub, rand_req.method)
#         try:
#             resp = req_method(req_arg)
#         except grpc.RpcError as err:
#             success = False
#             print("\n*******ERROR:***********\n", rand_req.method, "(\n")
#             print(req_arg, ")\nraised error\n", err, "\n=======================\n")
#     assert success
