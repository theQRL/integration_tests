#!/usr/bin/env python
import traceback
import threading
from scripts.docker_helper import get_container_from_name
from time import sleep

from qrl_testing.IntegrationTest import IntegrationTest, LogEntry
from qrl_testing.helpers import wallet_gen, wallet_ls, tx_push


class TxDuplicates(IntegrationTest):

    def __init__(self, max_running_time_secs=None):
        super().__init__(max_running_time_secs=max_running_time_secs)
        self.test_thread = threading.Thread(target=self.the_test)
        self.test_successful = None

    def the_test(self):
        try:
            IntegrationTest.writeout("Beginning Test")
            node_1 = get_container_from_name('testsintegration_node_1')
            src_wallet_1 = wallet_ls(node_1, '/home/testuser/.qrl/wallet1')
            dst_wallet_1 = wallet_ls(node_1, '/home/testuser/.qrl/wallet2')

            IntegrationTest.writeout("tx_prepare an unsigned transaction")
            tx_blob = node_1.exec_run(
                ["qrl", "--wallet_dir", src_wallet_1.location, "tx_prepare", "--src", src_wallet_1.addresses[0].number,
                 "--dst",
                 dst_wallet_1.addresses[0].address,
                 "--amount", "10", "--fee", "3"]).decode().strip()

            IntegrationTest.writeout("tx_sign the transaction blob")
            tx_blob_signed = node_1.exec_run(
                ["qrl", "--wallet_dir", src_wallet_1.location, "tx_sign", "--src", src_wallet_1.addresses[0].number,
                 "--txblob", tx_blob]).decode().strip()

            tx_push(node_1, tx_blob_signed)
            tx_push(node_1, tx_blob_signed)
            tx_push(node_1, tx_blob_signed)

            IntegrationTest.writeout(
                "Wait a bit. If the tx is confirmed, the network shouldn't accept the tx_blob_signed again.")
            sleep(120)

            IntegrationTest.writeout("tx_push: the tx should be confirmed by now, so this time it should be rejected")
            tx_push(node_1, tx_blob_signed)

            src_wallet_2 = wallet_ls(node_1, '/home/testuser/.qrl/wallet1')
            dst_wallet_2 = wallet_ls(node_1, '/home/testuser/.qrl/wallet2')
            IntegrationTest.writeout("src_addr balance: {}".format(src_wallet_2.addresses[0].balance))
            IntegrationTest.writeout("dst_addr balance: {}".format(dst_wallet_2.addresses[0].balance))

            if (dst_wallet_2.addresses[0].balance == (dst_wallet_1.addresses[0].balance + 10)) and (
                    src_wallet_2.addresses[0].balance == (src_wallet_1.addresses[0].balance - 13)):
                self.test_successful = True
            else:
                self.test_successful = False
        except:
            IntegrationTest.writeout(traceback.format_exc())
            self.test_successful = False

    def custom_process_log_entry(self, log_entry: LogEntry):
        if log_entry.node_id is not None:
            self.update_node_state(log_entry.node_id, log_entry)

            if self.all_nodes_synced and self.all_nodes_grpc_started:
                if not self.test_thread.is_alive() and self.test_successful is None:
                    print("Uptime: {} secs, all nodes in sync and gRPC servers running! Starting test".format(
                        self.running_time))
                    self.test_thread.start()

            if self.test_successful is True:
                self.successful_test()
            elif self.test_successful is False:
                self.fail_test()


if __name__ == '__main__':
    test = TxDuplicates(max_running_time_secs=600)
    test.start()
