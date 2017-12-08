#!/usr/bin/env bash
cd $1
echo "Downloading qrl_pb2* from Github main repo"
wget https://github.com/theQRL/QRL/raw/master/qrl/generated/qrl_pb2.py
wget https://github.com/theQRL/QRL/raw/master/qrl/generated/qrl_pb2_grpc.py
echo "Patching qrl_pb2_grpc.py"
sed -i.bak -e 's/import qrl_pb2 as qrl__pb2/from . import qrl_pb2 as qrl__pb2/g' qrl_pb2_grpc.py
