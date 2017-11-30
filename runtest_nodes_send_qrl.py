#!/usr/bin/env python
import os
import time

from concurrent.futures import ThreadPoolExecutor

from qrl_testing.IntegrationTest import IntegrationTest, TOTAL_NODES, LogEntry
from qrl_testing.NodeInterface import NodeInterface

# This code depends on a modded qrl.core. Set PYTHONPATH.
from qrl.core.Transaction import Transaction
from qrl.core.Wallet import Wallet, AddressBundle
from qrl.core import config

pool = ThreadPoolExecutor(3)


class SendQRLToEachOther(IntegrationTest):

    def __init__(self):
        super().__init__(max_running_time_secs=600)
        self.test_running = False

    @staticmethod
    def send_qrl_test(instance):
        """
        Why doesn't futures work with normal methods of a class?
        """
        IntegrationTest.writeout("GATHERING INFORMATION ABOUT NODES")
        for node_id in instance.node_state:
            volumes_dir = "volumes/testsintegration_{}".format(node_id)
            wallet_dir = os.path.join(volumes_dir, "wallet/")
            wallet_address_file = os.path.join(volumes_dir, "wallet_address")
            ip_file = os.path.join(volumes_dir, "node_ip")

            with open(wallet_address_file) as f:
                instance.node_state[node_id].Qaddress = f.readline().strip()
            with open(ip_file) as f:
                instance.node_state[node_id].ip = f.readline().strip()
            instance.node_state[node_id].wallet_dir = wallet_dir

        node_1 = instance.node_state["node_1"]
        node_2 = instance.node_state["node_2"]
        node = NodeInterface(node_1.ip, debug=True)

        IntegrationTest.writeout("YOU ARE ENTERING SEND_QRL_TEST")
        
        # This is like saying Wallet(wallet_dir)
        config.user.wallet_path = node_1.wallet_dir
        node_1_wallet = Wallet()

        response = node.send(from_addr=node_1_wallet.address_bundle[0], to_addr=node_2.Qaddress.encode(), amount=10, fee=1)
        time.sleep(5)
        node_2_balance = node.check_balance(address=node_2_wallet.addresses)
        IntegrationTest.writeout(node_2_balance)

        # return True

    def custom_process_log_entry(self, log_entry: LogEntry):
        if log_entry.node_id is not None:
            self.update_node_synced(log_entry.node_id, log_entry.synced)
            self.update_node_grpc_started(log_entry.node_id, log_entry.rest)

            if self.all_nodes_synced:
                    print("All nodes in sync! Uptime: {} secs".format(self.running_time))
                    # future = pool.submit(self.writeout, "WTF")
                    if self.all_nodes_grpc_started and not self.test_running:
                        print("GRPC READY ON ALL NODES, CONDUCTING TEST")
                        pool.submit(self.send_qrl_test, self)
                        self.test_running = True

if __name__ == '__main__':
    test = SendQRLToEachOther()
    test.start()
