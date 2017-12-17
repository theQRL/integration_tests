#!/usr/bin/env python
import json
import traceback
import os
import subprocess
import threading
from time import sleep

from qrl_testing.IntegrationTest import IntegrationTest, LogEntry


class SendQRLToEachOther(IntegrationTest):

    def __init__(self, max_running_time_secs=None):
        super().__init__(max_running_time_secs=max_running_time_secs)
        self.test_thread = threading.Thread(target=self.send_qrl_test)
        self.test_successful = None

    def send_qrl_test(self):
        def read_machine_decodable_output(o: str):
            output = json.loads(o)
            location = output["location"]
            addr = output["addresses"][0]["address"]
            bal = output["addresses"][0]["balance"]
            return (location, addr, bal)

        def wallet_gen(wallet_dir, ip):
            """
            :param wallet_dir: volumes/srcwallet; volumes/dstwallet
            :param ip: 127.0.0.1
            :return: ('volumes/srcwallet', 'Q...', 100)
            """
            IntegrationTest.writeout("Generating 3rd party {} wallet".format(wallet_dir))
            tempwallet_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), wallet_dir)
            gen_cmd = subprocess.Popen(["qrl", "--wallet_dir", tempwallet_dir, "--host", ip, "-m", "wallet_gen"],
                                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            gen_cmd.wait(timeout=10)
            return read_machine_decodable_output(gen_cmd.stdout.read().decode())

        def wallet_ls(wallet_dir, ip):
            """
            :param wallet_dir: volumes/srcwallet; volumes/dstwallet
            :param ip: 127.0.0.1
            :return: ('volumes/srcwallet', 'Q...', 100)
            """
            tempwallet_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), wallet_dir)
            ls_cmd = subprocess.Popen(
                ["qrl", "--wallet_dir", tempwallet_dir, "--host", ip, "-m", "wallet_ls"],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT
            )
            ls_cmd.wait(timeout=10)
            return read_machine_decodable_output(ls_cmd.stdout.read().decode())

        IntegrationTest.writeout("Beginning Send QRL Integration Test")
        try:
            for s in self.node_states.values():
                s.find_ip_Qaddress_wallet()
            node_1 = self.node_states["node_1"]
            node_2 = self.node_states["node_2"]
    
            src_loc, src_addr, src_bal_old = wallet_gen('volumes/srcwallet', node_1.ip)
            dst_loc, dst_addr, dst_bal_old = wallet_gen('volumes/dstwallet', node_1.ip)
    
            amount = 50
            fee = 13
            IntegrationTest.writeout("qrl tx_transfer {},{}".format(amount, fee))
            tx_transfer = subprocess.Popen(
                ["qrl", "--wallet_dir", src_loc, "-r", "--host", node_1.ip, "tx_transfer", "--src",
                 src_addr, "--dst", dst_addr, "--amount", str(amount), "--fee", str(fee)],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT
            )
            tx_transfer.wait(timeout=10)
            resp = tx_transfer.stdout.read().decode()
            if 'True' not in resp:
                IntegrationTest.writeout("qrl tx_transfer error: {}".format(resp))
                self.test_successful = False
                return
    
            IntegrationTest.writeout("TX sent. Waiting a bit...")
            sleep(120)
    
            _, _, src_bal_new = wallet_ls('volumes/srcwallet', node_2.ip)
            _, _, dst_bal_new = wallet_ls('volumes/dstwallet', node_2.ip)
            IntegrationTest.writeout("src balance {}->{}".format(src_bal_old, src_bal_new))
            IntegrationTest.writeout("dst balance {}->{}".format(dst_bal_old, dst_bal_new))
    
            if (src_bal_new == src_bal_old - (amount + fee)) and (dst_bal_new == (dst_bal_old + amount)):
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
