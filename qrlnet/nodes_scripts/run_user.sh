#!/bin/bash -u

#RUN pip install -i https://testpypi.python.org/pypi --extra-index-url https://pypi.python.org/simple/  --upgrade qrl

##########################################
# Get source code
rm -rf ${HOME}/QRL
if [ -z ${INTEGRATION_TESTINPLACE:-} ]; then
    echo "Cloning source from github"
    git clone -b ${REPO_BRANCH} https://github.com/${REPO_SLUG}.git ${HOME}/QRL
    cd ${HOME}/QRL
    GITHASH=$(git -C ${HOME}/QRL/ rev-parse HEAD)
    echo "Repo hash: $GITHASH"
else
    echo "Copying source from local deployment"
    ls /volumes/source
    # Do not exclude .git, otherwise pip install -e /home/testuser/QRL will fail
    rsync -qiar --progress /volumes/source/QRL/ ${HOME}/QRL --exclude tests_integration
    ls ${HOME}/QRL
fi

#########################################
# Install dependencies
sudo -H pip3 install -U pip | grep -v 'Requirement already satisfied' | cat
sudo -H pip3 install -U -r ${HOME}/QRL/requirements.txt | grep -v 'Requirement already satisfied' | cat
sudo -H pip3 install -e ${HOME}/QRL | grep -v 'Requirement already satisfied' | cat

#########################################
# Patch source code genesis
mkdir -p /home/${USERNAME}/.qrl/wallet/
sudo python3 /home/${USERNAME}/scripts/prepare_node_config.py

sed -i 's|self.genesis_difficulty = 5000|self.genesis_difficulty = 10|g' ${HOME}/QRL/qrl/core/config.py


#########################################
# Execute phase
# TODO: We can probably remove this soon
echo "Boot phase: ${BOOT_PHASE}"
case "${BOOT_PHASE}" in
    freeze)
        # TODO: We can probably remove this soon
        tail -f /dev/null
        ;;
    start)
        nice python3 ${HOME}/QRL/start_qrl.py -l DEBUG --miningCreditWallet=Q0105001cdd844d816b76eab7d1c846b05a7c5cdcef3c4665d2f050a0f41f2bd2f7b824e6d093a5
        ;;

    *)
        echo $"Usage: $0 {bootstrap|start}"
        exit 1
esac
