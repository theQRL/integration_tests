import grpc
import qrlbase_pb2
import qrlbase_pb2_grpc

import subprocess
import os
import shutil
import argparse

parser = argparse.ArgumentParser(description='Takes a list of gRPC servers, downloads and compiles the gRPC interfaces to communicate with them')
parser.add_argument('server', nargs='+', help='specify server(s) in ip:addr format')
args = parser.parse_args()


for server in args.server:
    channel = grpc.insecure_channel(server)
    stub = qrlbase_pb2_grpc.BaseStub(channel)

    request = qrlbase_pb2.GetNodeInfoReq()
    response = stub.GetNodeInfo(request)

    version = "v{}".format(response.version)
    print("{} is running {}".format(server, version))

    base_path = os.getcwd()
    version_path = os.path.join(base_path, version)
    try:
        os.mkdir(version)
    except FileExistsError:
        print(version, "already exists, removing and trying again")
        shutil.rmtree(version)
        os.mkdir(version)

    with open(os.path.join(version_path, 'qrl.proto'), 'w') as f:
        f.write(response.grpcProto)

    os.chdir(version_path)
    proc = subprocess.run("python -m grpc_tools.protoc -I=. --python_out=. --grpc_python_out=. qrl.proto".split(" "))
    if proc.returncode == 0:
        print("Successfully generated qrl gRPC code from qrl.proto")
    else:
        print("Failed to generate qrl gRPC code from qrl.proto", proc.stderr)
