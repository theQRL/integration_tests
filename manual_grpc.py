import grpc
from qrl.core import config
from qrl.core.Wallet import Wallet, AddressBundle

from qrl_testing.tmp import qrl_pb2, qrl_pb2_grpc

channel = grpc.insecure_channel('172.19.0.2:9009')
stub = qrl_pb2_grpc.PublicAPIStub(channel)

response = stub.GetNodeState(qrl_pb2.GetNodeStateReq())
print("GetNodeState", response)

config.user.wallet_path = "volumes/testsintegration_node_1/wallet/"
w = Wallet()

import ipdb

ipdb.set_trace()

transferCoinsReq = qrl_pb2.TransferCoinsReq(
    address_from=w.address_bundle[0].address,
    address_to=b'Qe971057a52b08ffd549c6a0ed964c34256478ccc918bf14e383925a2ee95eab2781e87f8',
    amount=10,
    fee=10,
    xmss_pk=w.address_bundle[0].xmss.pk(),
    xmss_ots_index=w.address_bundle[0].xmss.get_index()
)
transferCoinsResp = stub.TransferCoins(transferCoinsReq)
print(transferCoinsResp)