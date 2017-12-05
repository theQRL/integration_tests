import grpc
from qrl_testing.NodeInterface import NodeInterface
from qrl_testing.tmp import qrl_pb2, qrl_pb2_grpc
from qrl.core import config
from qrl.core.Wallet import Wallet, AddressBundle


node = NodeInterface('172.19.0.2')
print("loading wallet 1")
config.user.wallet_path = "volumes/testsintegration_1/wallet"
w1 = Wallet()
print("wallet 1: generating new addr to send from")
w1.address_bundle.append(Wallet.get_new_address())

print("loading wallet 2")
config.user.wallet_path = "volumes/testsintegration_2/wallet"
w2 = Wallet()

response = node.send(from_addr=w1.address_bundle[1], to_addr=w2.address_bundle[0].address, amount=10, fee=1)
print(response)