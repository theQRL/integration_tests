import concurrent.futures
import io
import os
import shutil
import subprocess
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Queue


class MockNet(object):
    def __init__(self,
                 test_function,
                 timeout_secs=60,
                 node_count=0):
        self.pool = ThreadPoolExecutor()

        self.node_count = node_count
        self.test_function = test_function
        self.timeout_secs = timeout_secs

        self.nodes = []
        self.log_queue = Queue()
        self.this_file = os.path.realpath(__file__)
        self.this_dir = os.path.dirname(self.this_file)
        self.src_dst = os.path.join(self.this_dir, "src")

        self.src_pythonpath = "{}/src".format(self.src_dst)

    def prepare_source(self):
        shutil.rmtree(self.src_dst, ignore_errors=True)
        cmd = "{}/prepare_source.sh".format(self.this_dir)
        p = subprocess.Popen(cmd, shell=True)
        p.wait()

    @staticmethod
    def writeout(text):
        print("\033[0m\033[44m{} {:^35} {}\033[0m".format('*' * 20, text, '*' * 20))

    @staticmethod
    def writeout_error(text):
        print("\033[0m\033[40m{} {:^35} {}\033[0m".format('*' * 20, text, '*' * 20))

    def start_node(self, node_idx):
        p = subprocess.Popen("{}/run_node.sh".format(self.this_dir),
                             shell=True,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT)

        # Enqueue any output
        for line in io.TextIOWrapper(p.stdout, encoding="utf-8"):
            s = "Node{:2} | {}".format(node_idx, line)
            self.log_queue.put(s)

    def run(self):
        print("")
        self.writeout("Starting mocknet")
        test_future = self.pool.submit(self.test_function, self)

        # TODO: Launch mocknet
        for node_idx in range(self.node_count):
            self.nodes.append(self.pool.submit(self.start_node, node_idx))

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
        return result
