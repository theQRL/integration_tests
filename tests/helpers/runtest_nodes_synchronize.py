#!/usr/bin/env python
from .nodes_logs_parser import IntegrationTest, TOTAL_NODES, LogEntry

class CheckNodesSynchronize(IntegrationTest):
    def __init__(self,sync_event):
        super().__init__(max_running_time_secs=600)
        self.node_state = dict()
        self.sync_event = sync_event

    def custom_process_log_entry(self, log_entry: LogEntry):
        if log_entry.node_id is not None:
            self.node_state[log_entry.node_id] = log_entry.sync_state
            if len(self.node_state) == TOTAL_NODES:
                if all(s == 'synced' for s in self.node_state.values()):
                    print("All nodes in sync! Uptime: {} secs".format(self.running_time))
                    self.sync_event.set();
                    return self.successful_test()

def wait_for_sync(sync_event):
    test = CheckNodesSynchronize(sync_event)
    test.start()

if __name__ == '__main__':
    test = CheckNodesSynchronize()
    test.start()
