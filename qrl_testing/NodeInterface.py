import grpc

from qrl_testing.tmp import qrl_pb2, qrl_pb2_grpc

from qrl.core.Transaction import Transaction
from qrl.core.Wallet import Wallet, AddressBundle


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
            address_to=to_addr,
            amount=10,
            fee=1,
            xmss_pk=from_addr.xmss.pk(),
            xmss_ots_index=from_addr.xmss.get_index()
        )

        transferCoinsResp = self.stub.TransferCoins(transferCoinsReq)

        tx = Transaction.from_pbdata(transferCoinsResp.transaction_unsigned)
        tx.sign(from_addr.xmss)

        pushTransactionReq = qrl_pb2.PushTransactionReq(transaction_signed=tx.pbdata)
        pushTransactionResp = self.stub.PushTransaction(pushTransactionReq)

        if self.debug:
            print(transferCoinsReq)
            print(transferCoinsResp)
            print(pushTransactionResp)

        return pushTransactionResp.some_response

    def check_balance(self, address:bytes):
        getAddressStateReq = qrl_pb2.GetAddressStateReq(address=address)
        getAddressStateResp = self.stub.GetAddressState(getAddressStateReq)

        if self.debug:
            print(getAddressStateReq)
            print(getAddressStateResp)
        
        return getAddressStateResp.state.balance
