import concurrent.futures
import io
import os
import shutil
import subprocess
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Queue

import yaml


class MockNetSuccess(Exception):
    pass


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
        self.data_dir = os.path.join(self.this_dir, 'data')

        # Clear mocknet data
        shutil.rmtree(self.data_dir, ignore_errors=True)

    def prepare_source(self):
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
        node_data_dir = os.path.join(self.data_dir, "node{:03}".format(node_idx))
        os.makedirs(node_data_dir, exist_ok=True)

        port_count = 5
        config = {
            'peer_list': ["127.0.0.1:{0}".format(10000 + num * port_count, ) for num in range(node_idx)],
            'mining_enabled': False,
            'p2p_local_port': 10000 + node_idx * port_count,
            'p2p_public_port': 10000 + node_idx * port_count,
            'admin_api_port': 10000 + node_idx * port_count + 1,
            'public_api_port': 10000 + node_idx * port_count + 2,
            'mining_api_port': 10000 + node_idx * port_count + 3,
            'grpc_proxy_port': 10000 + node_idx * port_count + 4
        }

        config_file = os.path.join(node_data_dir, 'config.yml')
        with open(config_file, 'w') as f:
            yaml.dump(config, stream=f, Dumper=yaml.Dumper)

        p = subprocess.Popen("{}/run_node.sh --qrldir {}".format(self.this_dir, node_data_dir),
                             shell=True,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT)

        # Enqueue any output
        for line in io.TextIOWrapper(p.stdout, encoding="utf-8"):
            s = "Node{:2} | {}".format(node_idx, line)
            self.log_queue.put(s)

    def run(self):
        result = None

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
        except MockNetSuccess:
            pass
        except Exception:
            self.writeout_error("Exception detected")
            raise

        test_future.cancel()
        for node in self.nodes:
            node.cancel()
        self.writeout("Finished")
        return result
