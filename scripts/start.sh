#!/bin/bash -u

export USERNAME="testuser"
id -g $DOCKER_GID &> /dev/null || groupadd -g $DOCKER_GID $USERNAME
id -u $DOCKER_UID &> /dev/null || useradd -u $DOCKER_UID -g $DOCKER_GID $USERNAME

mkdir -p /home/${USERNAME}

# Get volume name based on container name
EASYNAME=$(python3 /root/scripts/docker_helper.py)
echo "EasyName: ${EASYNAME}"

mkdir -p /volumes
chown -R ${USERNAME}:${USERNAME} /volumes
VOLUME_NAME="/volumes/${EASYNAME}"

# Copy scripts and configuration
cp /root/scripts/run_user.sh  /home/${USERNAME}/run_user.sh
mkdir -p ${VOLUME_NAME}
ln -sf ${VOLUME_NAME} /home/${USERNAME}/.qrl

if [[ -v LOCALNET_ONLY ]]; then
    echo "Restricting to LOCALNET"
    cp /root/scripts/config.yml  ${VOLUME_NAME}/config.yml
fi

# Fix permissions
chown -R ${USERNAME}:${USERNAME} /home/${USERNAME}
chown -R ${USERNAME}:${USERNAME} ${VOLUME_NAME}
chmod -R a+rwx /home/${USERNAME}

# Launch user script
sudo BOOT_PHASE=${BOOT_PHASE} \
     INTEGRATION_TESTINPLACE=${INTEGRATION_TESTINPLACE} \
     REPO_SLUG=${REPO_SLUG} REPO_BRANCH=${REPO_BRANCH} \
     EASYNAME=${EASYNAME} -i -u ${USERNAME} \
     /home/${USERNAME}/run_user.sh

mkdir -p /home/${USERNAME}/.qrl/wallet/
rm /home/${USERNAME}/.qrl/wallet/wallet.qrl
