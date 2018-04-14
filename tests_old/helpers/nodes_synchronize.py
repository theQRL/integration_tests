#!/usr/bin/env python
from .logs_parser import TestLogParser, TOTAL_NODES, LogEntry


class CheckNodesSynchronize(TestLogParser):
    def __init__(self, sync_event):
        """
        max_running_time_secs must be longer, because the tests_old run after this class.
        Unlike other TestLogParser children, this class is only used to check when it's ok to start tests_old on the net.
        """
        super().__init__(max_running_time_secs=1800)
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
