#!/usr/bin/env python
import threading
import pytest
import os
import multiprocessing
import subprocess

from tests.helpers.nodes_logs_parser import IntegrationTest, LogEntry, TOTAL_NODES


class RunFor1MinuteAfterSync(IntegrationTest):
    ONE_MINUTE_SECS = 60

    def __init__(self, sync_event):
        super().__init__(max_running_time_secs=620)
        self.node_state = dict()
        self.delayed_success_thread = None
        self.sync_event = sync_event

    def custom_process_log_entry(self, log_entry: LogEntry):
        if self.delayed_success_thread is None:
            if log_entry.node_id is not None:
                self.node_state[log_entry.node_id] = log_entry.sync_state

                if len(self.node_state) == TOTAL_NODES:
                    if all(s == 'synced' for s in self.node_state.values()):
                        print("All nodes in sync! Uptime: {} secs".format(self.running_time))
                        self.delayed_success_thread = threading.Timer(self.ONE_MINUTE_SECS, self.sync_event.set)
                        self.delayed_success_thread.start()


@pytest.fixture(scope="function")
def setup():
    yield
    current_path = os.path.dirname(__file__)
    script_path = os.path.join(current_path, '..', 'helpers/reset_net.sh')
    subprocess.call([script_path])


@pytest.mark.oneminaftersync
def test_nodes_synced():
    sync_event = multiprocessing.Event()
    test = RunFor1MinuteAfterSync(sync_event)
    w1 = multiprocessing.Process(
        name='nodes',
        target=test.start,
        args=(),
    )
    w1.start()
    synced = False
    while w1.is_alive():
        # process is still alive and we are still waiting for the time to pass
        if sync_event.is_set():
            w1.terminate()
            assert True
            return
    if not synced:
        raise Exception('NotSyncedException')
    assert False
