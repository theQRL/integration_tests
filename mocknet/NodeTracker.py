# coding=utf-8
# Distributed under the MIT software license, see the accompanying
# file LICENSE or http://www.opensource.org/licenses/mit-license.php.
import time
from queue import Empty


class NodeLogTracker(object):
    MAX_IDLE_TIME = 60
    MAX_NO_ADDITION_TIME = 120  # Increased to 2 minutes for CI stability

    def __init__(self, mocknet, max_idle_time=None, max_no_addition_time=None):
        self.node_status = {}
        self.node_last_event = {}
        self.node_last_addition = {}
        self.mocknet = mocknet
        
        # Allow configurable timeouts, with defaults
        self.max_idle_time = max_idle_time if max_idle_time is not None else self.MAX_IDLE_TIME
        self.max_no_addition_time = max_no_addition_time if max_no_addition_time is not None else self.MAX_NO_ADDITION_TIME

        self.abort_triggers = [
            "<_Rendezvous of RPC that terminated with (StatusCode.UNKNOWN",
            "Traceback (most recent call last):",
            "Headerhash false for block",
            "Failed PoW Validation"
        ]

        # FIXME: Move this to regex
        self.add_block_triggers = [
            "Apply block #",
            "Added Block #"
        ]

        self.abort_requested_at = None

    def synced_count(self):
        count = 0
        for k, v in self.node_status.items():
            if v == 'synced':
                count += 1
        return count

    def track(self, output=True):
        msg = ''
        try:
            msg = self.mocknet.log_queue.get(block=True, timeout=1)
            self.parse(msg)
            if output:
                print(msg, end='')

            if self.abort_requested_at is None:
                for s in self.abort_triggers:
                    if s in msg:
                        self.abort_requested_at = time.time()
                        self.mocknet.writeout_error('ABORT REQUESTED!!!!!!')
                        break

        except Empty:
            pass

        if self.abort_requested_at is not None:
            if time.time() - self.abort_requested_at > 0.5:
                raise Exception("ABORT TRIGGERED")

        return msg

    def check_idle_nodes(self):
        for k, v in self.node_last_event.items():
            if time.time() - v > self.max_idle_time:
                raise Exception("{} - no event for more than {} secs".format(k, self.max_idle_time))

    def check_last_addition(self):
        for k, v in self.node_last_addition.items():
            if time.time() - v > self.max_no_addition_time:
                raise Exception("{} - no addition for more than {} secs".format(k, self.max_no_addition_time))

    def parse(self, msg):
        parts = msg.split('|')
        if len(parts) > 4:
            node_id = parts[0].strip()
            status = parts[3].strip()
            self.node_status[node_id] = status
            self.node_last_event[node_id] = time.time()

            for v in self.add_block_triggers:
                if v in msg:
                    self.node_last_addition[node_id] = time.time()
                    break

    def get_status(self, node_id):
        return self.node_status.get(node_id, 'unknown')
