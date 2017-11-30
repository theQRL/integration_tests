#!/usr/bin/env python
import os

from concurrent.futures import ThreadPoolExecutor

from qrl_testing.IntegrationTest import IntegrationTest, TOTAL_NODES, LogEntry
from qrl_testing.NodeInterface import NodeInterface

# This code depends on a modded qrl.core. Set PYTHONPATH.
from qrl.core.Transaction import Transaction
from qrl.core.Wallet import Wallet, AddressBundle

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

        IntegrationTest.writeout(instance.node_state)

        node_1 = instance.node_state["node_1"]
        node = NodeInterface(node_1.ip, debug=True)
        node_1_wallet = Wallet(wallet_path="/home/shinichi/qrlwallet")
        IntegrationTest.writeout(node_1_wallet)
        node_2_wallet = Wallet(wallet_path=node_2.wallet_dir)
        # return True

    def custom_process_log_entry(self, log_entry: LogEntry):
        if log_entry.node_id is not None:
            self.update_node_synced(log_entry.node_id, log_entry.synced)

            if self.all_nodes_synced:
                    print("All nodes in sync! Uptime: {} secs".format(self.running_time))
                    # future = pool.submit(self.writeout, "WTF")
                    if not self.test_running:
                        pool.submit(self.send_qrl_test, self)
                        self.test_running = True

if __name__ == '__main__':
    test = SendQRLToEachOther()
    test.start()
