#!/bin/sh

export DOCKER_UID=$( id -u ${USER} )
export DOCKER_GID=$( id -g ${USER} )
export NUM_NODES=4

echo "*****************************"
echo ${USER}
echo ${DOCKER_UID}
echo ${DOCKER_GID}
echo ${NUM_NODES}
echo "*****************************"
echo

echo "****************************************************************"
echo "                       BOOTSTRAPPING"
echo "****************************************************************"
export BOOT_PHASE=bootstrap
export LOCALNET_ONLY=1
docker-compose up --scale node=${NUM_NODES}
python3 ./scripts/collect_wallets.py # Get Addresses and prepare genesis block

echo "****************************************************************"
echo "                       STARTING LOCALNET"
echo "****************************************************************"
export BOOT_PHASE=start
export LOCALNET_ONLY=1
docker-compose up --scale node=${NUM_NODES}
