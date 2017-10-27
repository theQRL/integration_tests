#!/bin/sh

export DOCKER_UID=$( id -u ${USER} )
export DOCKER_GID=$( id -g ${USER} )
export NUM_NODES=4

echo "****************************************************************"
echo "****************************************************************"
echo "                       STARTING LOCALNET"
echo "****************************************************************"
echo "****************************************************************"
export BOOT_PHASE=bootstrap
docker-compose up --scale node=${NUM_NODES}
