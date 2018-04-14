import concurrent.futures
import io
import subprocess

from pebble import ProcessPool


class MockNet(object):
    def __init__(self,
                 test_function,
                 timeout_secs=60,
                 nodes=0):
        self.pool = ProcessPool(max_workers=10, max_tasks=1)

        self.nodes = nodes
        self.test_function = test_function
        self.timeout_secs = timeout_secs

    @staticmethod
    def writeout(text):
        print("\033[0m\033[44m{} {:^35} {}\033[0m".format('*' * 20, text, '*' * 20))

    @staticmethod
    def writeout_error(text):
        print("\033[0m\033[40m{} {:^35} {}\033[0m".format('*' * 20, text, '*' * 20))

    def start_node(self, node_idx):
        print("Starting node %d", node_idx)
        p = subprocess.Popen("start_qrl.py",
                             shell=True,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)

        for line in io.TextIOWrapper(p.stdout, encoding="utf-8"):
            print(line)

    def run(self):
        print("")
        self.writeout("Starting mocknet")
        test_future = self.pool.schedule(self.test_function)

        # TODO: Launch mocknet
        for node_idx in range(self.nodes):
            self.pool.schedule(self.start_node, node_idx)

        try:
            result = test_future.result(self.timeout_secs)
        except concurrent.futures.TimeoutError:
            test_future.cancel()
            self.writeout_error("TIMEOUT")
            raise TimeoutError
        except:
            self.writeout_error("Exception detected")
            raise

        self.writeout("Finished")
