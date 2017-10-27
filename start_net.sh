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
echo

echo "****************************************************************"
echo "****************************************************************"
echo "                       STARTING LOCALNET"
echo "****************************************************************"
echo "****************************************************************"
export BOOT_PHASE=bootstrap
docker-compose up --scale node=${NUM_NODES}
