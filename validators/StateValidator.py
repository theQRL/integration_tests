# coding=utf-8
# Distributed under the MIT software license, see the accompanying
# file LICENSE or http://www.opensource.org/licenses/mit-license.php.
import grpc
from qrl.generated import qrldebug_pb2_grpc, qrldebug_pb2


class StateValidator:
    def __init__(self, debug_addresses):
        self.debug_addresses = debug_addresses

    def get_full_state(self):
        debug_api_addresses = self.debug_addresses
        full_state_responses = []
        for debug_api_address in debug_api_addresses:
            channel_public = grpc.insecure_channel(debug_api_address)
            stub = qrldebug_pb2_grpc.DebugAPIStub(channel_public)

            full_state_responses.append(stub.GetFullState(request=qrldebug_pb2.GetFullStateReq()))

        return full_state_responses

    @staticmethod
    def check_address_state(state1, state2):
        if state1.address != state2.address:
            raise Exception('Address mismatch %s %s', state1.address, state2.address)

        if state1.balance != state2.balance:
            raise Exception('Balance mismatch %s %s', state1.balance, state2.balance)

        if state1.nonce != state2.nonce:
            raise Exception('Nonce mismatch %s %s', state1.nonce, state2.nonce)

        if state1.ots_bitfield != state2.ots_bitfield:
            raise Exception('OTS Bitfield mismatch %s %s', state1.ots_bitfield, state2.ots_bitfield)

        if state1.transaction_hashes != state2.transaction_hashes:
            raise Exception('Transaction hashes mismatch %s %s',
                            state1.transaction_hashes,
                            state2.transaction_hashes)

        if state1.tokens != state2.tokens:
            raise Exception('Tokens mismatch %s %s', state1.tokens, state2.tokens)

        if state1.latticePK_list != state2.latticePK_list:
            raise Exception('LatticePK mismatch %s %s', state1.latticePK_list, state2.latticePK_list)

        if state1.slave_pks_access_type != state2.slave_pks_access_type:
            raise Exception('Slave PKS mismatch %s %s', state1.slave_pks_access_type, state2.slave_pks_access_type)

        if state1.ots_counter != state2.ots_counter:
            raise Exception('Slave PKS mismatch %s %s', state1.ots_counter, state2.ots_counter)

    def validate_addresses_state(self, state1, state2):
        try:
            self.check_address_state(state1, state2)
        except Exception as e:
            raise Exception('Exception for state check between addresses %s %s\nError:\n',
                            state1.address,
                            state2.address,
                            e)

    def validate_state(self) -> bool:
        full_state_responses = self.get_full_state()
        state_response1 = full_state_responses[0]
        for state_response in full_state_responses[1:]:
            self.validate_addresses_state(state_response1.coinbase_state, state_response.coinbase_state)
            if len(state_response1.addresses_state) != len(state_response.addresses_state):
                raise Exception('Number of Addresses State mismatch')
            for address_state in state_response1.addresses_state:
                self.validate_addresses_state(address_state, address_state)

        return True
