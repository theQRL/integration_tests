#!/usr/bin/env python
import json
import traceback
import threading
import docker
from scripts.docker_helper import get_container_from_name
from collections import namedtuple
from time import sleep
from decimal import Decimal

from qrl_testing.IntegrationTest import IntegrationTest, LogEntry

AddressRepr = namedtuple('AddressRepr', ['number', 'address', 'balance'])
WalletRepr = namedtuple('WalletRepr', ['location', 'addresses'])


class DoubleSpendOTSIndex(IntegrationTest):

    def __init__(self, max_running_time_secs=None):
        super().__init__(max_running_time_secs=max_running_time_secs)
        self.test_thread = threading.Thread(target=self.doublespend_ots_index)
        self.test_successful = None

    def doublespend_ots_index(self):
        environment = {
            "LANG": "C.UTF-8",
            "LC_ALL": "C.UTF-8"
        }

        def parse_human_readable_output(o: str):
            o = o.splitlines()

            location = o[0].split()[-1]
            addresses = []
            for line in o[3:]:
                i, address, balance = line.split()
                a = AddressRepr(number=i, address=address, balance=Decimal(balance))
                addresses.append(a)

            w = WalletRepr(location=location, addresses=addresses)
            return w

        def parse_tx_push_output(o: str):
            lastline_idx = output.rfind('}\n')+1
            tmp_json_output = output[:lastline_idx]
            lastline = output[lastline_idx:].strip()
            return json.loads(tmp_json_output), lastline

        def prepare_container(c: docker.models.containers.Container) -> None:
            IntegrationTest.writeout("preparing container {} for IntegrationTest interaction".format(c.name))
            IntegrationTest.writeout(c.exec_run("sudo -H pip3 install -e /home/testuser/QRL").decode())
            IntegrationTest.writeout(c.exec_run("qrl --help", environment=environment).decode())

        def wallet_gen(container: docker.models.containers.Container, wallet_dir: str):
            """
            :param wallet_dir: /home/testuser/srcwallet; /home/testuser/dstwallet
            :return: WalletRepr(location='/home/testuser/srcwallet', addresses=[AddressRepr(...),]
            """
            IntegrationTest.writeout("Generating 3rd party {} wallet".format(wallet_dir))
            o = container.exec_run(["qrl", "--wallet_dir", wallet_dir, "wallet_gen"], environment=environment).decode()
            return parse_human_readable_output(o)

        def wallet_ls(container: docker.models.containers.Container, wallet_dir: str):
            """
            :param wallet_dir: /home/testuser/srcwallet; /home/testuser/dstwallet
            :return: WalletRepr(location='/home/testuser/srcwallet', addresses=[AddressRepr(...),]
            """
            o = container.exec_run(["qrl", "--wallet_dir", wallet_dir, "wallet_ls"], environment=environment).decode()
            return parse_human_readable_output(o)

        try:
            IntegrationTest.writeout("Beginning DoubleSpend OTS Index Test")
            node_1 = get_container_from_name('testsintegration_node_1')
            prepare_container(node_1)
            src_wallet_1 = wallet_gen(node_1, '/home/testuser/srcwallet')
            dst_wallet_1 = wallet_gen(node_1, '/home/testuser/dstwallet')

            IntegrationTest.writeout("tx_prepare an unsigned transaction")
            tx_blob = node_1.exec_run(
                ["qrl", "--wallet_dir", src_wallet_1.location, "tx_prepare", "--src", src_wallet_1.addresses[0].number,
                 "--dst",
                 dst_wallet_1.addresses[0].address,
                 "--amount", "10", "--fee", "3"], environment=environment).decode().strip()

            IntegrationTest.writeout("tx_sign the transaction blob")
            tx_blob_signed = node_1.exec_run(
                ["qrl", "--wallet_dir", src_wallet_1.location, "tx_sign", "--src", src_wallet_1.addresses[0].number,
                 "--txblob", tx_blob],
                 environment = environment).decode().strip()

            output = node_1.exec_run(
                ["qrl", "tx_push", "--txblob", tx_blob_signed], environment=environment
            ).decode().strip()
            _, lastline = parse_tx_push_output(output)
            IntegrationTest.writeout("tx_push signed transaction to network 1/3: {}".format(lastline))

            output = node_1.exec_run(
                ["qrl", "tx_push", "--txblob", tx_blob_signed], environment=environment
            ).decode().strip()
            _, lastline = parse_tx_push_output(output)
            IntegrationTest.writeout("tx_push signed transaction to network 2/3: {}".format(lastline))

            output = node_1.exec_run(
                ["qrl", "tx_push", "--txblob", tx_blob_signed], environment=environment
            ).decode().strip()
            _, lastline = parse_tx_push_output(output)
            IntegrationTest.writeout("tx_push signed transaction to network 3/3: {}".format(lastline))

            IntegrationTest.writeout("Wait a bit. If the tx is confirmed, the network shouldn't accept the tx_blob_signed again.")
            sleep(120)

            IntegrationTest.writeout("tx_push: the tx should be confirmed by now, so this time it should be rejected")
            output = node_1.exec_run(
                ["qrl", "tx_push", "--txblob", tx_blob_signed], environment=environment
            ).decode().strip()
            _, lastline = parse_tx_push_output(output)
            IntegrationTest.writeout("tx_push signed transaction to network 4/3: {}".format(lastline))

            src_wallet_2 = wallet_ls(node_1, '/home/testuser/srcwallet')
            dst_wallet_2 = wallet_ls(node_1, '/home/testuser/dstwallet')
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
    test = DoubleSpendOTSIndex(max_running_time_secs=6000)
    test.start()
