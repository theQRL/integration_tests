#!/usr/bin/env python
import threading

from qrl_testing.IntegrationTest import IntegrationTest, TOTAL_NODES, LogEntry

class RunFor1MinuteAfterSync(IntegrationTest):
    ONE_MINUTE_SECS = 60

    def __init__(self):
        super().__init__(max_running_time_secs=620)
        self.node_state = dict()
        self.delayed_success_thread = None

    def custom_process_log_entry(self, log_entry: LogEntry):
        if self.delayed_success_thread is None:
            if log_entry.node_id is not None:
                self.node_state[log_entry.node_id] = log_entry.sync_status

                if len(self.node_state) == TOTAL_NODES:
                    if all(s == 'synced' for s in self.node_state.values()):
                        print("All nodes in sync! Uptime: {} secs".format(self.running_time))
                        self.delayed_success_thread = threading.Timer(self.ONE_MINUTE_SECS, IntegrationTest.successful_test)
                        self.delayed_success_thread.start()

if __name__ == '__main__':
    test = RunFor1MinuteAfterSync()
    test.start()
