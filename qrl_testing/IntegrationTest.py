import re
import io
import os
import signal
import subprocess
import threading

import time
from collections import namedtuple
from enum import Enum

TOTAL_NODES = 4

ignore_errors = {
    "liberror-perl",
    "<class 'twisted.internet.error.ConnectionRefusedError'>: Connection was refused by other side: 111: Connection refused.",
    "<class 'twisted.internet.error.ConnectionDone'>: Connection was closed cleanly.",
    "<class 'twisted.internet.error.ConnectError'>: An error occurred while connecting: 113: No route to host.",
    "<class 'twisted.internet.error.TimeoutError'>: User timeout caused connection failure."
}

fatal_errors = {
    "sudo: unknown user",
    "error",
    "fatal:",
    "Traceback (most recent call last)",
    "cp: cannot stat '/home/travis/genesis.yml': No such file or directory"
}

LogEntry = namedtuple('LogEntry', 'full node_id time version sync_status rest')

class SyncStatus(Enum):
    SYNCED = 'synced'
    UNSYNCED = 'unsynced'
    SYNCING = 'syncing'
    UNDEFINED = ''

class NodeState:
    def __init__(self, node_id:str):
        self.node_id = node_id  # node_2
        self.ip = ''
        self.Qaddress = ''
        self.sync_status = SyncStatus('')
        self.grpc_started = False
        self.wallet_dir = ''

    def __repr__(self):
        return "<NodeState ip: {} Qaddress: {} sync_status: {} grpc_started: {}>".format(self.ip, self.Qaddress, self.sync_status, self.grpc_started)

    def find_ip_Qaddress_wallet(self):
        tests_integration_path = os.path.dirname(os.path.dirname(__file__))
        volumes_path = os.path.join(tests_integration_path, 'volumes/', 'testsintegration_{}'.format(self.node_id))

        ip_file = os.path.join(volumes_path, "node_ip")
        with open(ip_file) as f:
            self.ip = f.readline().strip()

        wallet_address_file = os.path.join(volumes_path, "wallet_address")
        with open(wallet_address_file) as f:
            self.Qaddress = f.readline().strip()
        
        self.wallet_dir = os.path.join(volumes_path, "wallet/")

    def update(self, log_entry: LogEntry):
        self.sync_status = SyncStatus(log_entry.sync_status)

        if 'grpc public service - started' in log_entry.rest:
            self.grpc_started = True

class IntegrationTest(object):
    def __init__(self, max_running_time_secs):
        self.max_running_time_secs = max_running_time_secs
        self.start_time = time.time()
        self.regex_ansi_escape = re.compile(r'\x1b[^m]*m')

        self.node_states = {}
        """
        {
            "node_1": NodeState(
                ip = "172.17.0.9"
                Qaddress = "Q..."
                sync_status = SyncStatus.SYNCED
            )
            ...
        }
        """
        IntegrationTest.writeout("******************** INTEGRATION TEST STARTED ********************")

    @property
    def running_time(self):
        return time.time() - self.start_time

    @property
    def all_nodes_synced(self):
        s = [n.sync_status == SyncStatus.SYNCED for n in self.node_states.values()]
        return all(s) and (len(self.node_states) == TOTAL_NODES)
    
    @property
    def all_nodes_grpc_started(self):
        grpc_started_status = [n.grpc_started for n in self.node_states.values()]
        return all(grpc_started_status) and (len(self.node_states) == TOTAL_NODES)

    @staticmethod
    def writeout(text):
        print("\033[0m\033[45m{} {} {}\033[0m".format('*'*20, text, '*'*20))

    @staticmethod
    def max_time_error():
        IntegrationTest.writeout("******************** MAX RUNNING TIME ERROR ********************")
        os.kill(os.getpid(), signal.SIGABRT)

    @staticmethod
    def successful_test():
        IntegrationTest.writeout("******************** SUCCESS! ********************")
        quit(0)

    def update_node_state(self, node_id, log_entry: LogEntry):
        """
        This function is called each time a line is output, don't put anything
        intensive here
        """
        state = self.node_states.get(node_id, NodeState(node_id=node_id))
        state.update(log_entry)
        self.node_states[node_id] = state

    def fail_test(self):
        def fail_exit():
            self.writeout("******************** FAILED!")
            os.kill(os.getpid(), signal.SIGABRT)

        # Fail after 2 secs to the output is available
        IntegrationTest.writeout("******************** FAILURE TRIGGERED! ********************")
        self.fail_timer = threading.Timer(2, fail_exit)
        self.fail_timer.start()

    def start(self):
        current_path = os.path.dirname(__file__)
        script_path = os.path.join(current_path, '..', 'start_net.sh')
        proc = subprocess.Popen([script_path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        myThread = threading.Timer(self.max_running_time_secs, IntegrationTest.max_time_error)
        myThread.start()

        try:
            for line in io.TextIOWrapper(proc.stdout, encoding="utf-8"):
                self.process_log_entry(line)
        except Exception as e:
            print(e)
        finally:
            if myThread.is_alive():
                myThread.cancel()
            proc.kill()

    def check_errors(self, entry_raw: str):
        # Detect errors but ignore acceptable ones
        entry_raw = entry_raw.lower()

        possible_error = False
        for e in fatal_errors:
            if e.lower() in entry_raw:
                possible_error = True
                break

        if possible_error:
            ignore = False
            for e in ignore_errors:
                if e.lower() in entry_raw:
                    ignore = True
                    break

            if not ignore:
                self.fail_test()

    def _remove_ansi_colors(self, s):
        return self.regex_ansi_escape.sub('', s)

    def parse_entry(self, entry_raw: str):
        # FIXME: Improve this
        entry_raw = self._remove_ansi_colors(entry_raw)
        entry_parts = entry_raw.split('|')
        if len(entry_parts) > 4:
            log_entry = LogEntry(full='',
                                 node_id=entry_parts[0].strip(),
                                 time=entry_parts[1].strip(),
                                 version=entry_parts[2],
                                 sync_status=entry_parts[3],
                                 rest=entry_parts[4])
        else:
            log_entry = LogEntry(full='',
                                 node_id=None,
                                 time=None,
                                 version=None,
                                 sync_status=None,
                                 rest=None)

        return log_entry

    def process_log_entry(self, entry_raw: str):
        print('[{:08.3f}] {}'.format(self.running_time, entry_raw), end='')
        self.check_errors(entry_raw)

        log_entry = self.parse_entry(entry_raw)
        self.custom_process_log_entry(log_entry)

    def custom_process_log_entry(self, log_entry: LogEntry):
        pass
