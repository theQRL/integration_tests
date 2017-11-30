#!/usr/bin/env python
from qrl_testing.IntegrationTest import IntegrationTest, TOTAL_NODES, LogEntry


class CheckNodesSynchronize(IntegrationTest):
    def __init__(self):
        super().__init__(max_running_time_secs=600)

    def custom_process_log_entry(self, log_entry: LogEntry):
        if log_entry.node_id is not None:
            self.update_node_state(log_entry.node_id, log_entry)

            if self.all_nodes_synced:
                print("All nodes in sync! Uptime: {} secs".format(self.running_time))
                return self.successful_test()


if __name__ == '__main__':
    test = CheckNodesSynchronize()
    test.start()
