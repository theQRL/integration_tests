#!/usr/bin/env python
import yaml
import threading
import pytest
import io
import os
import multiprocessing
import subprocess
from time import sleep
from multiprocessing import Value

from tests_old.helpers.logs_parser import TestLogParser, LogEntry

TOTAL_NODES = 2
NODE_SPAWN_DELAY = 5
MONITOR_DELAY = 10
BOOTSTRAP_TIMEOUT_SEC = 300


class ForkRecovery(TestLogParser):
    ONE_MINUTE_SECS = 60

    def __init__(self, node_id, fork_recovery_event, exit_counter):
        super().__init__(max_running_time_secs=120)
        self.node_id = node_id
        self.delayed_success_thread = None
        self.fork_recovery_event = fork_recovery_event
        self.exit_counter = exit_counter
        self.non_docker = True

        self.init_config_yml(self.node_id)

    @property
    def qrl_dir(self):
        return os.path.expanduser("{0}{1}".format('~/.qrl', self.node_id))

    @property
    def qrl_code_base(self):
        return os.path.join(os.path.expanduser('~/QRL'))

    @property
    def python_path(self):
        return os.path.join(self.qrl_code_base, 'src')

    def init_config_yml(self, node_num):
        config = {'peer_list': ["127.0.0.1:{0}".format(10000 + num * 5, ) for num in range(TOTAL_NODES)],
                  'mining_enabled': False,
                  'p2p_local_port': 10000 + node_num * 5,
                  'p2p_public_port': 10000 + node_num * 5,
                  'admin_api_port': 10000 + node_num * 5 + 1,
                  'public_api_port': 10000 + node_num * 5 + 2,
                  'mining_api_port': 10000 + node_num * 5 + 3,
                  'grpc_proxy_port': 10000 + node_num * 5 + 4}

        config_file = os.path.join(self.qrl_dir, 'config.yml')
        with open(config_file, 'w') as f:
            yaml.dump(config, stream=f, Dumper=yaml.Dumper)

    def custom_process_log_entry(self, log_entry: LogEntry):
        if self.delayed_success_thread is None:
            if log_entry.rest:
                if "Received Block #201 7132f0828a2689bff7c563b2ad941092525e48e6afb66bf62a4311d3e438495e" in log_entry.rest:
                    print("Successful Fork Recovery! Uptime: {} secs".format(self.running_time))
                    self.fork_recovery_event.set()

    def start_node(self):
        proc = subprocess.Popen(["/home/travis/virtualenv/python3.5.5/bin/python3.5 "
                                 "start_qrl.py --qrldir {0} --mockGetMeasurement {1}".format(self.qrl_dir,
                                                                                             "1000000000")],
                                shell=True,
                                env={"PYTHONPATH": self.python_path},
                                cwd=self.qrl_code_base,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT)

        my_thread = threading.Timer(self.max_running_time_secs, TestLogParser.max_time_error)
        my_thread.start()

        self.monitor_success(proc)

        try:
            for line in io.TextIOWrapper(proc.stdout, encoding="utf-8"):
                self.process_log_entry(line)
        except Exception as e:
            print(e)
        finally:
            if my_thread.is_alive():
                my_thread.cancel()
            proc.kill()

    def monitor_success(self, proc):
        if self.fork_recovery_event.is_set():
            if not proc.poll():
                proc.kill()
                self.exit_counter.value += 1
                return

        threading.Timer(MONITOR_DELAY, self.monitor_success, [proc]).start()


@pytest.fixture(scope="function")
def setup():
    yield


@pytest.mark.forkrecovery
def test_nodes_synced():
    fork_recovery_event = multiprocessing.Event()
    exit_counter = Value('i', 0)
    w = []

    # current_path = os.path.dirname(__file__)
    # Bootstrap node, with fork recovery data and QRL repository
    # script_path = os.path.join(current_path, '..', '..', 'qrlnet/fork_recovery_bootstrap.sh')

    # proc = subprocess.Popen([script_path], cwd=current_path, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    # proc.wait(BOOTSTRAP_TIMEOUT_SEC)
    # print(proc.stdout.read().decode())

    for i in range(1, TOTAL_NODES + 1):
        test = ForkRecovery(i, fork_recovery_event, exit_counter)
        w1 = multiprocessing.Process(
            name='nodes',
            target=test.start_node,
        )
        w1.start()
        w.append(w1)
        sleep(NODE_SPAWN_DELAY)  # Delay before starting next node

    for w1 in w:
        while w1.is_alive():
            # process is still alive and we are still waiting for the time to pass
            if exit_counter.value == TOTAL_NODES:
                w1.terminate()

    if fork_recovery_event.is_set():
        assert True
        return

    raise Exception('NotSyncedException')
