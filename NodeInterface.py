import grpc

from qrl_testing.tmp import qrl_pb2, qrl_pb2_grpc

# This code depends on a modded qrl.core. Set PYTHONPATH.
from qrl.core.Transaction import Transaction
from qrl.core.Wallet import Wallet, AddressBundle

node1 = '172.19.0.5:9009'
node1_wallet_dir="tmp/qrlwallet1"
node2 = '127.0.0.2:9009'
node2_wallet_dir="tmp/qrlwallet2"

wallet1 = Wallet(wallet_path=node1_wallet_dir)
wallet2 = Wallet(wallet_path=node2_wallet_dir)

class NodeInterface:
    """
    Abstraction on top of gRPC so that CLI, tests that need to communicate 
    with a running node do not reimplement business logic on top of gRPC.
    """
    def __init__(self, ip, port=9009, debug=False):
       """
       server format: ip:addr
       """
       self.debug = debug
       self.channel = grpc.insecure_channel(":".join([ip, str(port)]))  # 127.0.0.1, 9009 -> "127.0.0.1:9009"
       self.stub = qrl_pb2_grpc.PublicAPIStub(self.channel)

    def send(self, from_addr:AddressBundle, to_addr:bytes, amount, fee):
        transferCoinsReq = qrl_pb2.TransferCoinsReq(
            address_from=from_addr.address,
            address_to=to_addr.address,
            amount=10,
            fee=1,
            xmss_pk=from_addr.xmss.pk(),
            xmss_ots_index=from_addr.xmss.get_index()
        )

        f = self.stub.TransferCoins.future(transferCoinsReq)
        transferCoinsResp = f.result(timeout=5)

        tx = Transaction.from_pbdata(transferCoinsResp.transaction_unsigned)
        tx.sign(wallet1.address_bundle[0].xmss)

        pushTransactionReq = qrl_pb2.PushTransactionReq(transaction_signed=tx.pbdata)
        f = self.stub.PushTransaction.future(pushTransactionReq, timeout=5)
        pushTransactionResp = f.result(timeout=5)

        if self.debug:
            print(transferCoinsReq)
            print(transferCoinsResp)
            print(pushTransactionResp)

        return pushTransactionResp.some_response

    def check_balance(self, address:bytes):
        getAddressStateReq = qrl_pb2.GetAddressStateReq(address=address)
        f = self.stub.GetAddressState.future(getAddressStateReq, timeout=5)
        getAddressStateResp = f.result(timeout=5)
        
        if self.debug:
            print(getAddressStateReq)
            print(getAddressStateResp)
        
        return getAddressStateResp.state.balance


node = NodeInterface('172.19.0.7', debug=True)
print("Wallet 1 balance is", node.check_balance(wallet1.address_bundle[0].address))
print("Wallet 2 balance is", node.check_balance(wallet2.address_bundle[0].address))
print("Sending 10 QRL from Wallet 1 to Wallet 2")
node.send(wallet1.address_bundle[0], wallet2.address_bundle[0], 10, 1)
print("Wallet 1 balance is", node.check_balance(wallet1.address_bundle[0].address))
print("Wallet 2 balance is", node.check_balance(wallet2.address_bundle[0].address))