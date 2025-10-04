#!/usr/bin/env python3
# coding=utf-8
# Distributed under the MIT software license, see the accompanying
# file LICENSE or http://www.opensource.org/licenses/mit-license.php.

import concurrent.futures
import contextlib
import io
import multiprocessing
import os
import shutil
import signal
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Queue
from os.path import pardir
from time import sleep

import yaml

from mocknet.NodeTracker import NodeLogTracker

LOCALHOST_IP = '127.0.0.1'
PORT_COUNT = 6  # Number of ports assigned to each node
START_PORT = 10000  # Port from which assignment will start


def kill_process_group(pid):
    try:
        pgrp = os.getpgid(pid)
        os.killpg(pgrp, signal.SIGKILL)
        MockNet.writeout('[Mocknet] killed pid %d' % pid)
    except Exception as e:
        MockNet.writeout('[Mocknet] killing pid %d : %s' % (pid, str(e)))


@contextlib.contextmanager
def clean_up(mocknet,
             test_future,
             pid_queue,
             stop_event):
    try:
        yield
    finally:
        MockNet.writeout('[Mocknet] cleaning up')
        stop_event.set()
        while not pid_queue.empty():
            pid = pid_queue.get_nowait()
            kill_process_group(pid)

        MockNet.writeout('[Mocknet] waiting')
        test_future.result(timeout=2)
        MockNet.writeout('[Mocknet] monitor done')

        mocknet.pool.shutdown()
        mocknet.log_queue.cancel_join_thread()

        cmd = "ps aux | grep python"
        p = subprocess.Popen(cmd, shell=True)
        p.wait()

        MockNet.writeout('[Mocknet] clean up finished')


class MockNet(object):
    def __init__(self,
                 test_function,
                 timeout_secs=60,
                 node_count=0,
                 node_args="",
                 remove_data=True):
        print("")
        self.writeout("Starting mocknet")

        try:
            if sys.argv[1] == 'enableMining':
                self.mining_enabled = True
                self.run_script = 'run_mining_node.sh'
            else:
                self.mining_enabled = False
                self.run_script = 'run_node.sh'
        except Exception as e:
            self.mining_enabled = False
            self.run_script = 'run_node.sh'

        self.writeout("Mining Enabled: {}".format(self.mining_enabled))

        if node_count > 0:
            self.pool = ThreadPoolExecutor(max_workers=node_count * 2)
        else:
            self.pool = ThreadPoolExecutor()

        self.node_count = node_count
        self.test_function = test_function
        self.timeout_secs = timeout_secs

        self.nodes = []
        self.node_args = node_args
        self.log_queue = Queue()
        self.this_file = os.path.realpath(__file__)
        self.this_dir = os.path.dirname(self.this_file)
        self.data_dir = os.path.join(self.this_dir, pardir, 'tmp', 'data')

        self.nodes_pids = Queue()
        self.stop_event = multiprocessing.Event()
        self.stop_event.clear()

        # Addresses exposing gRPC services
        self._admin_addresses = []
        self._public_addresses = []
        self._mining_addresses = []
        self._debug_addresses = []

        self.start_time = None

        if remove_data:
            shutil.rmtree(self.data_dir, ignore_errors=True)

    def prepare_source(self):
        cmd = "{}/prepare_source.sh".format(self.this_dir)
        p = subprocess.Popen(cmd, shell=True)
        p.wait()

    @property
    def running(self):
        return not self.stop_event.is_set()

    @property
    def uptime(self):
        if self.start_time is None:
            return 0

        return time.time() - self.start_time

    @staticmethod
    def writeout(text):
        print("\033[0m\033[44m{} {:^35} {}\033[0m".format('*' * 20, text, '*' * 20))

    @staticmethod
    def writeout_error(text):
        print("\033[0m\033[40m{} {:^35} {}\033[0m".format('*' * 20, text, '*' * 20))

    @staticmethod
    def calc_port(node_idx, count=0):
        return START_PORT + node_idx * PORT_COUNT + count

    @staticmethod
    def ip_port(ip, port):
        return "{0}:{1}".format(ip, port)

    @property
    def admin_addresses(self):
        return self._admin_addresses

    @property
    def public_addresses(self):
        return self._public_addresses

    @property
    def mining_addresses(self):
        return self._mining_addresses

    @property
    def debug_addresses(self):
        return self._debug_addresses

    def append_api_addresses(self, config):
        self._admin_addresses.append(self.ip_port(LOCALHOST_IP, config['admin_api_port']))
        self._public_addresses.append(self.ip_port(LOCALHOST_IP, config['public_api_port']))
        self._mining_addresses.append(self.ip_port(LOCALHOST_IP, config['mining_api_port']))
        self._debug_addresses.append(self.ip_port(LOCALHOST_IP, config['debug_api_port']))

    def get_peers(self, node_idx):
        return [self.ip_port(LOCALHOST_IP, self.calc_port(num)) for num in range(node_idx)]

    def start_node(self, node_idx: int, stop_event: multiprocessing.Event):
        node_data_dir = os.path.join(self.data_dir, "node{:03}".format(node_idx))
        os.makedirs(node_data_dir, exist_ok=True)

        config = {
            'genesis_timestamp': 1528402558,
            'genesis_prev_headerhash': 'Thirst of Quantas',
            'peer_list': self.get_peers(node_idx),
            'mining_enabled': self.mining_enabled,
            'debug_api_enabled': True,
            'p2p_local_port': self.calc_port(node_idx),
            'p2p_public_port': self.calc_port(node_idx),
            'admin_api_port': self.calc_port(node_idx, 1),
            'public_api_port': self.calc_port(node_idx, 2),
            'mining_api_port': self.calc_port(node_idx, 3),
            'debug_api_port': self.calc_port(node_idx, 4),
            'grpc_proxy_port': self.calc_port(node_idx, 5),
        }

        self.append_api_addresses(config)

        config_file = os.path.join(node_data_dir, 'config.yml')
        with open(config_file, 'w') as f:
            yaml.dump(config, stream=f, Dumper=yaml.Dumper)

        if not stop_event.is_set():
            p = subprocess.Popen("{}/{} --qrldir {} {}".format(
                self.this_dir,
                self.run_script,
                node_data_dir,
                self.node_args),
                shell=True,
                preexec_fn=os.setsid,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT)

            self.nodes_pids.put(p.pid)

            # Enqueue any output
            for line in io.TextIOWrapper(p.stdout, encoding="utf-8"):
                s = "Node{:2} | {}".format(node_idx, line)
                if stop_event.is_set():
                    break
                self.log_queue.put(s, block=False)

            if stop_event.is_set():
                kill_process_group(p.pid)

    def run(self):
        MockNet.writeout('[Mocknet] run')
        self.stop_event.clear()
        self.start_time = time.time()

        test_future = self.pool.submit(self.test_function)

        with clean_up(self, test_future, self.nodes_pids, self.stop_event):
            for node_idx in range(self.node_count):
                if test_future.running():
                    MockNet.writeout('[Mocknet] launch node %d' % node_idx)
                    self.nodes.append(self.pool.submit(self.start_node, node_idx, self.stop_event))
                    sleep(1)
            try:
                remaining_time = self.timeout_secs - self.uptime
                MockNet.writeout('[Mocknet] remaining time: %d' % remaining_time)
                result = test_future.result(remaining_time)
            except concurrent.futures.TimeoutError:
                self.writeout_error("TIMEOUT")
                raise TimeoutError
            except Exception:
                self.writeout_error("Exception detected")
                raise

            self.writeout("Finished")
            return result


if __name__ == '__main__':
    def func_monitor_log():
        node_logtracker = NodeLogTracker(mocknet)
        while mocknet.running:
            node_logtracker.track()


    mocknet = MockNet(func_monitor_log,
                      timeout_secs=600,
                      node_count=4,
                      node_args="--mocknet")
    mocknet.prepare_source()
    mocknet.run()
