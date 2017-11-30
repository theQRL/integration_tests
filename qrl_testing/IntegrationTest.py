import re
import io
import os
import signal
import subprocess
import threading

import time
from collections import namedtuple

TOTAL_NODES = 6

ignore_errors = {
    "liberror-perl",
    "<class 'twisted.internet.error.ConnectionRefusedError'>: Connection was refused by other side: 111: Connection refused.",
    "<class 'twisted.internet.error.ConnectionDone'>: Connection was closed cleanly.",
    "<class 'twisted.internet.error.ConnectError'>: An error occurred while connecting: 113: No route to host.",
    "<class 'twisted.internet.error.TimeoutError'>: User timeout caused connection failure."
}

fatal_errors = {
    "error",
    "fatal:",
    "Traceback (most recent call last)",
    "cp: cannot stat '/home/travis/genesis.yml': No such file or directory"
}

LogEntry = namedtuple('LogEntry', 'full node_id time version synced rest')

class NodeState:
    def __init__(self, ip='', Qaddress='', synced=False, grpc_started=False):
        self.ip = ip
        self.Qaddress = Qaddress
        self.synced = synced
        self.grpc_started = False

        self.wallet_dir = ''  # path to its wallet dir in volumes

    def __repr__(self):
        return "ip: {} Qaddress: {} synced: {}".format(self.ip, self.Qaddress, self.synced)

class IntegrationTest(object):
    def __init__(self, max_running_time_secs):
        self.max_running_time_secs = max_running_time_secs
        self.start_time = time.time()
        self.regex_ansi_escape = re.compile(r'\x1b[^m]*m')

        self.node_state = {}
        """
        {
            "node_1": NodeState(
                ip = "172.17.0.9"
                Qaddress = "Q..."
                synced = True
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
        sync_status = []
        for node_id in self.node_state:
            sync_status.append(self.node_state[node_id].synced)

        return all(sync_status) and (len(self.node_state) == TOTAL_NODES)
    
    @property
    def all_nodes_grpc_started(self):
        grpc_started_status = []
        for node_id in self.node_state:
            grpc_started_status.append(self.node_state[node_id].grpc_started)

        return all(grpc_started_status) and (len(self.node_state) == TOTAL_NODES)

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

    def update_node_synced(self, node_id, state:str):
        node_id = node_id.strip()
        
        if state == 'synced':
            state_bool = True
        else:
            state_bool = False
                
        state = self.node_state.get(node_id, NodeState())
        state.synced = True
        self.node_state[node_id] = state

    def update_node_grpc_started(self, node_id, msg:str):
        node_id = node_id.strip()

        if "grpc node - started" in msg:
            state = self.node_state[node_id]
            state.grpc_started = True
            self.node_state[node_id] = state

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
                                 node_id=entry_parts[0],
                                 time=entry_parts[1],
                                 version=entry_parts[2],
                                 synced=entry_parts[3],
                                 rest=entry_parts[4])
        else:
            log_entry = LogEntry(full='',
                                 node_id=None,
                                 time=None,
                                 version=None,
                                 synced=None,
                                 rest=None)

        return log_entry

    def process_log_entry(self, entry_raw: str):
        print('[{:08.3f}] {}'.format(self.running_time, entry_raw), end='')
        self.check_errors(entry_raw)

        log_entry = self.parse_entry(entry_raw)
        self.custom_process_log_entry(log_entry)

    def custom_process_log_entry(self, log_entry: LogEntry):
        pass
