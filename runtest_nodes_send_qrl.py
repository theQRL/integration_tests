#!/usr/bin/env python
import traceback
import threading
from time import sleep

from scripts.docker_helper import get_container_from_name
from qrl_testing.helpers import wallet_gen, wallet_ls
from qrl_testing.IntegrationTest import IntegrationTest, LogEntry


class SendQRLToEachOther(IntegrationTest):

    def __init__(self, max_running_time_secs=None):
        super().__init__(max_running_time_secs=max_running_time_secs)
        self.test_thread = threading.Thread(target=self.send_qrl_test)
        self.test_successful = None

    def send_qrl_test(self):
        IntegrationTest.writeout("Beginning Send QRL Integration Test")
        try:
            node_1 = get_container_from_name('testsintegration_node_1')
            src_wallet_1 = wallet_ls(node_1, '/home/testuser/.qrl/wallet1')
            dst_wallet_1 = wallet_ls(node_1, '/home/testuser/.qrl/wallet2')

            amount = 50
            fee = 13
            IntegrationTest.writeout("qrl tx_transfer {},{}".format(amount, fee))

            output = node_1.exec_run(
                ["qrl", "--wallet_dir", src_wallet_1.location, "-r", "tx_transfer", "--src",
                 src_wallet_1.addresses[0].number, "--dst", dst_wallet_1.addresses[0].address,
                 "--amount", str(amount), "--fee", str(fee)]).decode().strip()

            if 'True' not in output:
                IntegrationTest.writeout("qrl tx_transfer error: {}".format(output))
                self.test_successful = False

            IntegrationTest.writeout("TX sent. Waiting a bit...")
            sleep(120)

            src_wallet_2 = wallet_ls(node_1, '/home/testuser/.qrl/wallet1')
            dst_wallet_2 = wallet_ls(node_1, '/home/testuser/.qrl/wallet2')
            IntegrationTest.writeout(
                "src balance {}->{}".format(src_wallet_1.addresses[0].balance, src_wallet_2.addresses[0].balance))
            IntegrationTest.writeout(
                "dst balance {}->{}".format(dst_wallet_1.addresses[0].balance, dst_wallet_2.addresses[0].balance))

            src_balance_correct = src_wallet_2.addresses[0].balance == (src_wallet_1.addresses[0].balance - (amount + fee))
            dst_balance_correct = dst_wallet_2.addresses[0].balance == (dst_wallet_1.addresses[0].balance + amount)
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
    test = SendQRLToEachOther(max_running_time_secs=600)
    test.start()
