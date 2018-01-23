#!/bin/bash -u

# TODO: Use a bash trap here
pushd . > /dev/null
cd $( dirname "${BASH_SOURCE[0]}" )

# Default values
export NUM_NODES=4
export LOCALNET_ONLY=1
export REPO_SLUG=theQRL/QRL
export REPO_BRANCH=pow
export DOCKER_UID=$( id -u ${USER} )
export DOCKER_GID=$( id -g ${USER} )

# Dump some state information
echo "*****************************"
echo "user        : ${USER}"
echo "docker UID  : ${DOCKER_UID}"
echo "docker GID  : ${DOCKER_GID}"
echo "num_nodes   : ${NUM_NODES}"
echo "repo slug   : ${REPO_SLUG}"
echo "repo branch : ${REPO_BRANCH}"
echo "*****************************"
echo

if [ ! -z ${INTEGRATION_TESTINPLACE:-} ]; then
    # Symlink source code inside the integration test volumes
    mkdir -p volumes/source
    SOURCE_DIR=$(readlink -m ..)
    echo "SOURCE DIR: ${SOURCE_DIR}"
    rsync -qiar --progress ${SOURCE_DIR} volumes/source --exclude tests_integration --exclude .git
fi

echo "****************************************************************"
echo "                       STARTING LOCALNET"
echo "****************************************************************"
export BOOT_PHASE=start
docker-compose up --scale node=${NUM_NODES}

popd > /dev/null
