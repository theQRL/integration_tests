#!/usr/bin/env python
import time

from qrl_testing.IntegrationTest import IntegrationTest, TOTAL_NODES, LogEntry

class RunFor10Minutes(IntegrationTest):
    TEN_MINUTES_SECS = 600

    def __init__(self):
        super().__init__(max_running_time_secs=620)
        self.node_state = dict()
        self.could_sync = False

    def custom_process_log_entry(self, log_entry: LogEntry):
        if log_entry.node_id is not None:
            self.node_state[log_entry.node_id] = log_entry.sync_status
            if len(self.node_state) == TOTAL_NODES and not self.could_sync:
                if all(s == 'synced' for s in self.node_state.values()):
                    IntegrationTest.writeout("******************** NODES SYNCED ********************")
                    self.could_sync = True

        if time.time() - self.start_time > self.TEN_MINUTES_SECS:
            if self.could_sync:
                self.successful_test()
            else:
                self.fail_test()

if __name__ == '__main__':
    test = RunFor10Minutes()
    test.start()
