#!/usr/bin/env python
import threading

from qrl_testing.IntegrationTest import IntegrationTest, TOTAL_NODES, LogEntry

class RunFor10Minutes(IntegrationTest):
    TEN_MINUTES_SECS = 600

    def __init__(self):
        super().__init__(max_running_time_secs=620)
        self.node_state = dict()

        myThread = threading.Timer(self.TEN_MINUTES_SECS, IntegrationTest.successful_test)
        myThread.start()


    def custom_process_log_entry(self, log_entry: LogEntry):
        pass

if __name__ == '__main__':
    test = RunFor10Minutes()
    test.start()
