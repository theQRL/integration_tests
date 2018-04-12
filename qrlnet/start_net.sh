#!/bin/bash -u

# TODO: Use a bash trap here
pushd . > /dev/null
cd $( dirname "${BASH_SOURCE[0]}" )

# Default values
export NUM_NODES_DEFAULT=4
export REPO_SLUG_DEFAULT=theQRL/QRL
export REPO_BRANCH_DEFAULT=master
export LOCALNET_ONLY=1
export DOCKER_UID=$( id -u ${USER} )
export DOCKER_GID=$( id -g ${USER} )


# Apply default values if not previously set
if [ -z ${NUM_NODES:-} ]; then
    export NUM_NODES=${NUM_NODES_DEFAULT}
fi

if [ -z ${REPO_SLUG:-} ]; then
    export REPO_SLUG=${REPO_SLUG_DEFAULT}
fi

if [ -z ${REPO_BRANCH:-} ]; then
    export REPO_BRANCH=${REPO_BRANCH_DEFAULT}
fi

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
    SOURCE_DIR=$(readlink -m ../..)
    echo "SOURCE DIR: ${SOURCE_DIR}"
    # Do not exclude .git, otherwise pip install -e /home/testuser/QRL will fail
    rsync -qar ${SOURCE_DIR} volumes/source --exclude tests_integration > /dev/null
fi

echo "****************************************************************"
echo "                       STARTING LOCALNET"
echo "****************************************************************"
export BOOT_PHASE=start
docker-compose up --scale node=${NUM_NODES}

popd > /dev/null
