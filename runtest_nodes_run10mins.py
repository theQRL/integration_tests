#!/usr/bin/env python
from qrl_testing.IntegrationTest import IntegrationTest, TOTAL_NODES, LogEntry


class RunFor10Minutes(IntegrationTest):
    def __init__(self):
        super().__init__(max_running_time_secs=600)
        self.node_state = dict()

    def custom_process_log_entry(self, log_entry: LogEntry):
        pass

if __name__ == '__main__':
    test = RunFor10Minutes()
    test.start()
