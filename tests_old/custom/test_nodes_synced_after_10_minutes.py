import multiprocessing
import os
import subprocess
import time

import pytest
from tests_old.helpers.logs_parser import TestLogParser, TOTAL_NODES, LogEntry


class RunFor10Minutes(TestLogParser):
    TEN_MINUTES_SECS = 700

    def __init__(self, timeout_event, shared_success_value):
        super().__init__(max_running_time_secs=720)
        self.node_state = dict()
        self.could_sync = False
        self.timeout_event = timeout_event
        self.shared_success_value = shared_success_value

    def custom_process_log_entry(self, log_entry: LogEntry):
        if log_entry.node_id is not None:
            self.node_state[log_entry.node_id] = log_entry.sync_state
            if len(self.node_state) == TOTAL_NODES and not self.could_sync:
                if all(s == 'synced' for s in self.node_state.values()):
                    TestLogParser.writeout("******************** NODES SYNCED ********************")
                    self.could_sync = True

        if time.time() - self.start_time > self.TEN_MINUTES_SECS:
            if self.could_sync:
                # test successful
                self.shared_success_value.value = 1
            else:
                # test failed
                self.shared_success_value.value = 0
            self.timeout_event.set()


@pytest.fixture(scope="function")
def setup():
    yield
    current_path = os.path.dirname(__file__)
    script_path = os.path.join(current_path, '..', 'qrlnet/reset_net.sh')
    subprocess.call([script_path])


@pytest.mark.runfor10minutes
def test_nodes_synced():
    success_value = multiprocessing.Value('i', 0)
    timeout_event = multiprocessing.Event()
    test = RunFor10Minutes(timeout_event, success_value)
    w1 = multiprocessing.Process(
        name='nodes',
        target=test.start,
        args=(),
    )
    w1.start()
    while w1.is_alive():
        # process is still alive and we are still waiting for the time to pass
        if timeout_event.is_set():
            if success_value.value != 1:
                w1.terminate()
                assert False
            else:
                w1.terminate()
                assert True
                return
    # process got killed , test failed
    assert False
