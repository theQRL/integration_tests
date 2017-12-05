#!/usr/bin/env python
import os
import time

from concurrent.futures import ThreadPoolExecutor

from qrl_testing.IntegrationTest import IntegrationTest, TOTAL_NODES, LogEntry
from qrl_testing.NodeInterface import NodeInterface

from qrl.core.Transaction import Transaction
from qrl.core.Wallet import Wallet, AddressBundle
from qrl.core import config

pool = ThreadPoolExecutor(3)


class SendQRLToEachOther(IntegrationTest):

    def __init__(self):
        super().__init__(max_running_time_secs=600)
        self.test_running = False

    def send_qrl_test(self):
        IntegrationTest.writeout("Beginning Send QRL Integration Test")

        for s in self.node_states.values():
            s.find_ip_Qaddress_wallet()
        node_1 = self.node_states["node_1"]
        node_2 = self.node_states["node_2"]
        node = NodeInterface(node_1.ip, debug=True)

        # This is like saying Wallet(wallet_dir)
        config.user.wallet_path = node_1.wallet_dir
        node_1_wallet = Wallet()

        # Because all nodes stake in the integration test network, we can't send txns
        # from them. So we need to create a second AddressBundle to send money from.
        IntegrationTest.writeout("GENERATING SECOND ADDRESS TO SEND QRL FROM")
        node_1_wallet.address_bundle.append(Wallet.get_new_address())

        sending_address_new_balance = node.check_balance(address=sending_address)
        receiving_address_new_balance = node.check_balance(address=receiving_address)
        IntegrationTest.writeout(
            "Sending address now has: {}, Receiving address now has: {}".format(sending_address_new_balance,
                                                                                receiving_address_new_balance))
        if receiving_address_new_balance == (receiving_address_old_balance + 10):
            self.successful_test()
        else:
            self.fail_test()


    def custom_process_log_entry(self, log_entry: LogEntry):
        if log_entry.node_id is not None:
            self.update_node_state(log_entry.node_id, log_entry)

            if self.all_nodes_synced:
                print("All nodes in sync! Uptime: {} secs".format(self.running_time))
                if self.all_nodes_grpc_started and not self.test_running:
                    pool.submit(self.send_qrl_test)
                    self.test_running = True

if __name__ == '__main__':
    test = SendQRLToEachOther()
    test.start()
