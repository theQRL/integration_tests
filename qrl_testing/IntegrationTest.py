import io
import os
import signal
import subprocess
import threading

import time
from collections import namedtuple

TOTAL_NODES = 6

ignore_errors = {
    "liberror-perl",
    "<class 'twisted.internet.error.ConnectionRefusedError'>: Connection was refused by other side: 111: Connection refused.",
    "<class 'twisted.internet.error.ConnectionDone'>: Connection was closed cleanly.",
    "<class 'twisted.internet.error.ConnectError'>: An error occurred while connecting: 113: No route to host.",
    "<class 'twisted.internet.error.TimeoutError'>: User timeout caused connection failure."
}

fatal_errors = {
    "error",
    "fatal: Remote branch experiments not found in upstream origin",
    "Traceback (most recent call last)",
    "cp: cannot stat '/home/travis/genesis.yml': No such file or directory"
}

LogEntry = namedtuple('LogEntry', 'full node_id time version sync_state rest')


class IntegrationTest(object):
    def __init__(self, max_running_time_secs):
        self.max_running_time_secs = max_running_time_secs
        self.start_time = time.time()

    @property
    def running_time(self):
        return time.time() - self.start_time

    @staticmethod
    def max_time_error():
        print("******************** MAX RUNNING TIME ERROR")
        os.kill(os.getpid(), signal.SIGABRT)

    @staticmethod
    def successful_test():
        print("******************** SUCCESS!")
        quit(0)

    def fail_test(self):
        def fail_exit():
            print("******************** FAILED!")
            os.kill(os.getpid(), signal.SIGABRT)

        # Fail after 2 secs to the output is available
        self.fail_timer = threading.Timer(2, fail_exit)
        self.fail_timer.start()

    def start(self):
        proc = subprocess.Popen(["./start_net.sh"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        myThread = threading.Timer(self.max_running_time_secs, IntegrationTest.max_time_error)
        myThread.start()

        try:
            for line in io.TextIOWrapper(proc.stdout, encoding="utf-8"):
                self.process_log_entry(line)
        except Exception as e:
            print(e)
        finally:
            if myThread.is_alive():
                myThread.cancel()
            proc.kill()

    def check_errors(self, entry_raw: str):
        # Detect errors but ignore acceptable ones
        entry_raw = entry_raw.lower()

        possible_error = False
        for e in fatal_errors:
            if e.lower() in entry_raw:
                possible_error = True
                break

        if possible_error:
            ignore = False
            for e in ignore_errors:
                if e.lower() in entry_raw:
                    ignore = True
                    break

            if not ignore:
                self.fail_test()

    def parse_entry(self, entry_raw: str):
        # FIXME: Improve this
        entry_parts = entry_raw.split('|')
        if len(entry_parts) > 4:
            log_entry = LogEntry(full='',
                                 node_id=entry_parts[0],
                                 time=entry_parts[1],
                                 version=entry_parts[2],
                                 sync_state=entry_parts[3],
                                 rest=entry_parts[4])
        else:
            log_entry = LogEntry(full='',
                                 node_id=None,
                                 time=None,
                                 version=None,
                                 sync_state=None,
                                 rest=None)

        return log_entry

    def process_log_entry(self, entry_raw: str):
        print('[{:08.3f}] {}'.format(self.running_time, entry_raw), end='')
        self.check_errors(entry_raw)

        log_entry = self.parse_entry(entry_raw)
        self.custom_process_log_entry(log_entry)

    def custom_process_log_entry(self, log_entry: LogEntry):
        pass
