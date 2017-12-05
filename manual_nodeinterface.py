import grpc
import time
from qrl_testing.NodeInterface import NodeInterface
from qrl.core import config
from qrl.core.Wallet import Wallet, AddressBundle


node = NodeInterface('172.19.0.5', 9009)
state = node.check_state()
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

state = node.check_state()
block_height_before_sending = state.block_height
while state.block_height < block_height_before_sending + 3:
    state = node.check_state()
    print("waiting for 3 blocks to go by", state.block_height)
    time.sleep(1)

node_2_balance = node.check_balance(w2.address_bundle[0].address)
print(node_2_balance)