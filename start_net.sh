#!/bin/sh

export DOCKER_UID=$( id -u ${USER} )
export DOCKER_GID=$( id -g ${USER} )
export NUM_NODES=6

echo "*****************************"
echo ${USER}
echo ${DOCKER_UID}
echo ${DOCKER_GID}
echo ${NUM_NODES}
python3 --version
echo "*****************************"
echo

echo "****************************************************************"
echo "                       BOOTSTRAPPING"
echo "****************************************************************"
export BOOT_PHASE=bootstrap
export LOCALNET_ONLY=1
docker-compose up --scale node=${NUM_NODES}
python3 ./scripts/collect_node_data.py # Get Addresses/ips and prepare genesis block

echo "****************************************************************"
echo "                       STARTING LOCALNET"
echo "****************************************************************"
cat ./scripts/config.yml
cat ./scripts/genesis.yml

export BOOT_PHASE=start
export LOCALNET_ONLY=1
docker-compose up --scale node=${NUM_NODES}
