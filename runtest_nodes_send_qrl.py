#!/usr/bin/env python
import threading
import time

from qrl_testing.IntegrationTest import IntegrationTest, LogEntry

class SendQRLToEachOther(IntegrationTest):
    def __init__(self):
        super().__init__(max_running_time_secs=600)


if __name__ == '__main__':
    test = SendQRLToEachOther()
    test.start()