#!/usr/bin/env python
import traceback
import threading
from scripts.docker_helper import get_container_from_name

from time import sleep
from qrl_testing.helpers import wallet_gen, wallet_ls, tx_push
from qrl_testing.IntegrationTest import IntegrationTest, LogEntry


class TxOtsDuplicates(IntegrationTest):
    def __init__(self, max_running_time_secs=None):
        super().__init__(max_running_time_secs=max_running_time_secs)
        self.test_thread = threading.Thread(target=self.the_test)
        self.test_successful = None

    def the_test(self):
        try:
            IntegrationTest.writeout("Beginning Test")
            node_1 = get_container_from_name('node_1')
            src_wallet_1 = wallet_ls(node_1, '/home/testuser/.qrl/wallet1')
            dst_wallet_1 = wallet_ls(node_1, '/home/testuser/.qrl/wallet2')

            IntegrationTest.writeout("tx_prepare an unsigned transaction")
            tx_blob_1 = node_1.exec_run(
                ["qrl", "--wallet_dir", src_wallet_1.location, "tx_prepare", "--src", src_wallet_1.addresses[0].number,
                 "--dst",
                 dst_wallet_1.addresses[0].address,
                 "--amount", "10", "--fee", "3"]).decode().strip()

            IntegrationTest.writeout("tx_sign the transaction blob")
            tx_blob_1_signed = node_1.exec_run(
                ["qrl", "--wallet_dir", src_wallet_1.location, "tx_sign", "--src", src_wallet_1.addresses[0].number,
                 "--txblob", tx_blob_1]).decode().strip()

            tx_push(node_1, tx_blob_1_signed)
            tx_push(node_1, tx_blob_1_signed)
            tx_push(node_1, tx_blob_1_signed)

            IntegrationTest.writeout("tx_prepare yet another unsigned transaction")
            tx_blob_2 = node_1.exec_run(
                ["qrl", "--wallet_dir", src_wallet_1.location, "tx_prepare", "--src", src_wallet_1.addresses[0].number,
                 "--dst",
                 dst_wallet_1.addresses[0].address,
                 "--amount", "35", "--fee", "3"]).decode().strip()

            IntegrationTest.writeout("tx_sign the new transaction blob")
            tx_blob_2_signed = node_1.exec_run(
                ["qrl", "--wallet_dir", src_wallet_1.location, "tx_sign", "--src", src_wallet_1.addresses[0].number,
                 "--txblob", tx_blob_2]).decode().strip()

            tx_push(node_1, tx_blob_2_signed)
            tx_push(node_1, tx_blob_2_signed)
            tx_push(node_1, tx_blob_2_signed)

            IntegrationTest("Waiting a bit for the 2 txs to confirm")
            sleep(120)

            src_wallet_2 = wallet_ls(node_1, '/home/testuser/.qrl/wallet1')
            dst_wallet_2 = wallet_ls(node_1, '/home/testuser/.qrl/wallet2')
            IntegrationTest.writeout("src_addr balance: {}".format(src_wallet_2.addresses[0].balance))
            IntegrationTest.writeout("dst_addr balance: {}".format(dst_wallet_2.addresses[0].balance))

            src_balance_correct = src_wallet_2.addresses[0].balance == (src_wallet_1.addresses[0].balance - 51)
            dst_balance_correct = dst_wallet_2.addresses[0].balance == (dst_wallet_1.addresses[0].balance + 45)

            if src_balance_correct and dst_balance_correct:
                self.test_successful = True
            else:
                self.test_successful = False
        except:
            IntegrationTest.writeout(traceback.format_exc())
            self.test_successful = False

    def custom_process_log_entry(self, log_entry: LogEntry):
        if log_entry.node_id is not None:
            self.update_node_state(log_entry.node_id, log_entry)

            if self.all_nodes_grpc_started:
                if not self.test_thread.is_alive() and self.test_successful is None:
                    print("Uptime: {} secs, gRPC servers running!".format(self.running_time))
                    self.test_thread.start()

            if self.test_successful is True:
                self.successful_test()
            elif self.test_successful is False:
                self.fail_test()


if __name__ == '__main__':
    test = TxOtsDuplicates(max_running_time_secs=600)
    test.start()
