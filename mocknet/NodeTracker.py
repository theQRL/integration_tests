# coding=utf-8
# Distributed under the MIT software license, see the accompanying
# file LICENSE or http://www.opensource.org/licenses/mit-license.php.

class NodeLogTracker(object):
    def __init__(self):
        self.node_status = {}

    def synced_count(self):
        count = 0
        for k, v in self.node_status.items():
            if v == 'synced':
                count += 1
        return count

    def parse(self, msg):
        print(msg, end='')
        parts = msg.split('|')
        if len(parts) > 4:
            node_id = parts[0].strip()
            status = parts[3].strip()
            self.node_status[node_id] = status

    def get_status(self, node_id):
        return self.node_status.get(node_id, 'unknown')
