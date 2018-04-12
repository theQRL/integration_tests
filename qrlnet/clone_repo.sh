#!/bin/bash -u


# Default values
export REPO_SLUG=theQRL/QRL
export REPO_BRANCH=master
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

echo "Cloning source from github"
git clone -b ${REPO_BRANCH} https://github.com/${REPO_SLUG}.git ${HOME}/QRL --depth=1
cd ${HOME}/QRL
GITHASH=$(git -C ${HOME}/QRL/ rev-parse HEAD)
echo "Repo hash: $GITHASH"
