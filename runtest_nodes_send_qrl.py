#!/usr/bin/env python
from concurrent.futures import ThreadPoolExecutor

from qrl_testing.IntegrationTest import IntegrationTest, TOTAL_NODES, LogEntry
from qrl_testing.NodeInterface import NodeInterface

pool = ThreadPoolExecutor(3)


class SendQRLToEachOther(IntegrationTest):

    def __init__(self):
        super().__init__(max_running_time_secs=600)
        self.node_state = dict()
        self.test_running = False

    @staticmethod
    def send_qrl_test(instance):
        """
        Why doesn't futures work with normal methods of a class?
        """
        IntegrationTest.writeout("FUUUUUUCK")
        node = NodeInterface('172.19.0.3', debug=True)
        print(str(node))

    def custom_process_log_entry(self, log_entry: LogEntry):
        if log_entry.node_id is not None:
            self.update_node_synced(log_entry.node_id, log_entry.synced)

            if self.all_nodes_synced:
                    print("All nodes in sync! Uptime: {} secs".format(self.running_time))
                    # future = pool.submit(self.writeout, "WTF")
                    if not self.test_running:
                        pool.submit(self.send_qrl_test, self)
                        self.test_running = True
if __name__ == '__main__':
    test = SendQRLToEachOther()
    test.start()
