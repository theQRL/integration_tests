#!/usr/bin/env python3

"""
Start nodes, wait for them to sync, and then wait for each to have 3 blocks.
"""

import sys, os
import grpc

import qrlbase_pb2_grpc
import qrlbase_pb2
import qrl_pb2_grpc
import qrl_pb2

from qrl_testing.IntegrationTest import IntegrationTest, TOTAL_NODES, LogEntry

#--- Node Communication ---
# TODO: Some of this should be common library code, maybe in qrl_testing.IntegrationTest
#       Once we have more tests it should become clear which pieces should be refactored.

def get_nodes_info():
    """
    Return the nodes' information as reported by Docker.
    These are returned in "container-number" order and this ordering can be relied upon.
    The container-number corresponds to the "--index" command-line option of docker-compose.
    """
    import docker
    cli = docker.Client(base_url='unix://var/run/docker.sock')
    nodes = cli.containers()
    nodes.sort(key=lambda x: x['Labels']['com.docker.compose.container-number'])
    return nodes

def get_grpc_ports():
    """Return the localhost grpc communication ports as an array sorted in container-number order"""
    nodes = get_nodes_info()
    grpc_ports = [x['Ports'][0]['PublicPort'] for x in nodes]
    return grpc_ports

def get_channel(port: int):
    """Return an insecure_channel for the given grpc port"""
    channel = grpc.insecure_channel('127.0.0.1:' + str(port))
    return channel

def get_PublicAPIStub(port: int):
    """Return the PublicAPI stub for the given grpc port"""
    stub = qrl_pb2_grpc.PublicAPIStub(get_channel(port))
    return stub


class CheckNodesSynchronize(IntegrationTest):
    def __init__(self):
        super().__init__(max_running_time_secs=600)
        self.node_state = dict()

    def extract_data(self, log_entry: LogEntry):
        """Extract all relevant data from the given log_entry"""
        if log_entry.node_id is not None:
            self.node_state[log_entry.node_id] = log_entry.sync_state

    def nodes_synchronized(self):
        """Return True if nodes are all in sync"""
        if len(self.node_state) == TOTAL_NODES and all(s == 'synced' for s in self.node_state.values()):
            return True
        return False

    def custom_process_log_entry(self, log_entry: LogEntry):
        self.extract_data(log_entry)
        if not self.nodes_synchronized():
            return
        print("All nodes in sync -- waiting on block generation. Uptime: {} secs".format(self.running_time))

        block_heights = []
        for i, port in enumerate(get_grpc_ports()):
            stub = get_PublicAPIStub(port)
            response = stub.GetNodeState(qrl_pb2.GetNodeStateReq())
            block_heights.append(response.info.block_height)

        print("Blocks by node index: " + repr(block_heights))
        if all(x >= 3 for x in block_heights):
            return self.successful_test()

if __name__ == '__main__':
    test = CheckNodesSynchronize()
    test.start()
