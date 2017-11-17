#!/usr/bin/env python
import threading
import time

from qrl_testing.IntegrationTest import IntegrationTest, TOTAL_NODES, LogEntry

class RunFor10Minutes(IntegrationTest):
    TEN_MINUTES_SECS = 600

    def __init__(self):
        super().__init__(max_running_time_secs=620)
        self.node_state = dict()

    def custom_process_log_entry(self, log_entry: LogEntry):
        if time.time() - self.start_time > self.TEN_MINUTES_SECS:
            self.successful_test()

if __name__ == '__main__':
    test = RunFor10Minutes()
    test.start()
