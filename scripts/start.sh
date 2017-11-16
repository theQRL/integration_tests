#!/bin/bash -u

export USERNAME=$(awk -v val=${DOCKER_UID} -F ":" '$3==val{print $1}' /etc/passwd)
mkdir -p /home/${USERNAME}

# Get volume name based on container name
EASYNAME=$(python3 /root/scripts/get_name.py)
echo "EasyName: ${EASYNAME}"
VOLUME_NAME="/volumes${EASYNAME}"

ls /volumes/source

# Copy scripts and configuration
cp /root/scripts/run_user.sh  /home/${USERNAME}/run_user.sh
mkdir -p ${VOLUME_NAME}
ln -s ${VOLUME_NAME} /home/${USERNAME}/.qrl

if [[ -v LOCALNET_ONLY ]]; then
    echo "Restricting to LOCALNET"
    cp /root/scripts/config.yml  ${VOLUME_NAME}/config.yml
    cp /root/scripts/genesis.yml  /home/${USERNAME}/genesis.yml
fi

# Fix permissions
chown -R ${USERNAME}:${USERNAME} /home/${USERNAME}
chown -R ${USERNAME}:${USERNAME} ${VOLUME_NAME}
chmod -R a+rwx /home/${USERNAME}

# Launch user script
sudo BOOT_PHASE=${BOOT_PHASE} INTEGRATION_TESTINPLACE=${INTEGRATION_TESTINPLACE} REPO_SLUG=${REPO_SLUG} REPO_BRANCH=${REPO_BRANCH} EASYNAME=${EASYNAME} -i -u ${USERNAME} /home/${USERNAME}/run_user.sh
