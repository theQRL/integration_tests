#!/usr/bin/env python
from .logs_parser import TestLogParser, TOTAL_NODES, LogEntry


class CheckNodesSynchronize(TestLogParser):
    def __init__(self, sync_event):
        super().__init__(max_running_time_secs=600)
        self.node_state = dict()
        self.sync_event = sync_event

    def custom_process_log_entry(self, log_entry: LogEntry):
        if log_entry.node_id is not None:
            self.node_state[log_entry.node_id] = log_entry.sync_state
            if len(self.node_state) == TOTAL_NODES:
                if all(s == 'synced' for s in self.node_state.values()):
                    self.sync_event.set()


def wait_for_sync(sync_event):
    test = CheckNodesSynchronize(sync_event)
    test.start()
