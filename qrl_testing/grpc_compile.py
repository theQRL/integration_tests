import grpc
import qrlbase_pb2
import qrlbase_pb2_grpc

import subprocess
import os
import shutil
import argparse

"""
This should belong in scripts/, but it needs ../qrl_testing/qrlbase_pb2
and Python doesn't let you import ..qrl_testing.module
"""

def grpc_compile(server):
    """
    server is a ip:addr string
    """
    channel = grpc.insecure_channel(server)
    stub = qrlbase_pb2_grpc.BaseStub(channel)

    ip, port = server.split(":")

    request = qrlbase_pb2.GetNodeInfoReq()
    response = stub.GetNodeInfo(request)

    version = "v{}".format(response.version)
    print("{} is running {}".format(ip, version))

    base_path = os.path.dirname(os.path.abspath(__file__))
    destination = os.path.join(base_path, 'tmp')
    try:
        os.mkdir(destination)
    except FileExistsError:
        print(version, "already exists, removing and trying again")
        shutil.rmtree(destination)
        os.mkdir(destination)

    with open(os.path.join(destination, 'qrl.proto'), 'w') as f:
        f.write(response.grpcProto)

    os.chdir(destination)
    proc = subprocess.run("python -m grpc_tools.protoc -I=. --python_out=. --grpc_python_out=. qrl.proto".split(" "))

    if proc.returncode == 0:
        print("Successfully generated qrl gRPC code from qrl.proto")
    else:
        print("Failed to generate qrl gRPC code from qrl.proto", proc.stderr)

    with open('__init__.py', 'a'):  # touch tmp/__init__.py
        pass

parser = argparse.ArgumentParser(description='Given a gRPC server, downloads and compiles the gRPC interfaces to communicate with them')
parser.add_argument('server', help='specify server in ip:addr format')
args = parser.parse_args()
grpc_compile(args.server)
