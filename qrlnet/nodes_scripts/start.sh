#!/bin/bash -u

###########################################3
# We need to set the container user id to match the host id to avoid permission problems in the host
export USERNAME="testuser"
id -g $DOCKER_GID &> /dev/null || groupadd -g $DOCKER_GID $USERNAME
id -u $DOCKER_UID &> /dev/null || useradd -u $DOCKER_UID -g $DOCKER_GID $USERNAME

###########################################3
# Create a home directory for the testuser
mkdir -p /home/${USERNAME}

###########################################3
# Get fixed volume name based on container name so we have persistent storage between container instantiations
EASYNAME=$(python3 /root/scripts/docker_helper.py)
echo "EasyName: ${EASYNAME}"
mkdir -p /volumes
chown -R ${USERNAME}:${USERNAME} /volumes
VOLUME_NAME="/volumes/${EASYNAME}"

###########################################3
# Copy scripts and configuration to the testuser
mkdir -p /home/${USERNAME}/scripts
cp /root/scripts/run_user.sh  /home/${USERNAME}/run_user.sh
cp /root/scripts/*  /home/${USERNAME}/scripts
mkdir -p ${VOLUME_NAME}
ln -sf ${VOLUME_NAME} /home/${USERNAME}/qrl

###########################################3
# If the network is restricted to localnet. Override the node configuration with a smaller set of ips
if [[ -v LOCALNET_ONLY ]]; then
    echo "Restricting to LOCALNET"
    # FIXME: Right now there is not setting. It will always restrict to local net
fi

###########################################3
# Fix permissions in case something is not set properly
chown -R ${USERNAME}:${USERNAME} /home/${USERNAME}
chown -R ${USERNAME}:${USERNAME} ${VOLUME_NAME}
chmod -R a+rwx /home/${USERNAME}

###########################################3
# Launch user script
sudo BOOT_PHASE=${BOOT_PHASE} \
     INTEGRATION_TESTINPLACE=${INTEGRATION_TESTINPLACE} \
     REPO_SLUG=${REPO_SLUG} REPO_BRANCH=${REPO_BRANCH} \
     EASYNAME=${EASYNAME} -i -u ${USERNAME} \
     /home/${USERNAME}/run_user.sh
