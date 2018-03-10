PUBLIC_API_PORT = 9009
PASS_NUM = 100
import sys
sys.path.append('..')
import pytest
import docker
from random import choice
import grpc

from tests.helpers.module_conversion import modules_to_strategies
from qrl.generated import qrl_pb2
from qrl.generated import qrl_pb2_grpc

from collections import namedtuple
ReqAttrNames = namedtuple('ReqAttrNames', ['method', 'arg'])

@pytest.mark.grpchypothesis
def test_grpc_with_hypothesis():
    protobuf_strategies = modules_to_strategies(qrl_pb2)
    publicapi = qrl_pb2._PUBLICAPI
    if(not publicapi.methods):
        print("*******ASSERT: methods is empty ************")
        assert False
    req_attrs = []
    for m in publicapi.methods:       
        req_attrs.append(ReqAttrNames(m.name, m.input_type.name))
   
    def get_ip(container):
        return container.attrs['NetworkSettings']['Networks']['qrlnet_default']['IPAddress']
    stubs = []
    for container in docker.from_env().containers.list():
        channel = grpc.insecure_channel(get_ip(container) + ":" + str(PUBLIC_API_PORT))
        stubs.append(qrl_pb2_grpc.PublicAPIStub(channel))
    if not stubs:
        print("*******ASSERT: stubs is empty ************")
        assert False
    success = True
    for i in range(1, PASS_NUM):
        rand_stub = choice(stubs)
        rand_req = choice(req_attrs)
        req_strategy = protobuf_strategies[getattr(qrl_pb2, rand_req.arg)]
        req_arg = req_strategy.example()
        req_method = getattr(rand_stub, rand_req.method)
        try:      
            resp = req_method(req_arg)
        except grpc.RpcError as err:
            success = False        
            print("\n*******ERROR:***********\n", rand_req.method, "(\n")
            print(req_arg, ")\nraised error\n", err, "\n=======================\n")
    assert success
