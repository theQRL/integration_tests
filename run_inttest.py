from qrl_testing.IntegrationTest import IntegrationTest, TOTAL_NODES, LogEntry


class CheckNodesSynchronize(IntegrationTest):
    def __init__(self):
        super().__init__(max_running_time_secs=600)
        self.node_state = dict()

    def custom_process_log_entry(self, log_entry: LogEntry):
        if log_entry.node_id is not None:

            self.node_state[log_entry.node_id] = log_entry.sync_state
            if len(self.node_state) == TOTAL_NODES:
                if all(s == 'synced' for s in self.node_state.values()):
                    print("All nodes in sync! Uptime: {} secs".format(self.running_time))
                    return self.successful_test()


if __name__ == '__main__':
    test = CheckNodesSynchronize()
    test.start()
