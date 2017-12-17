#!/bin/bash -u

#RUN pip install -i https://testpypi.python.org/pypi --extra-index-url https://pypi.python.org/simple/  --upgrade qrl

# Check node IP addresses
ifconfig | perl -nle 's/dr:(\S+)/print $1/e' > ${HOME}/.qrl/node_ip
cat ${HOME}/.qrl/node_ip | grep -v '127.0.0.1'

# Get source code
rm -rf ${HOME}/QRL
if [ -z ${INTEGRATION_TESTINPLACE:-} ]; then
    git clone -b ${REPO_BRANCH} https://github.com/${REPO_SLUG}.git ${HOME}/QRL
    cd ${HOME}/QRL
    GITHASH=$(git -C ${HOME}/QRL/ rev-parse HEAD)
    echo "Repo hash: $GITHASH"
else
    echo "Copying local source"
    ls /volumes/source
    rsync -qiar --progress /volumes/source/QRL/ ${HOME}/QRL --exclude tests_integration --exclude .git
    ls ${HOME}/QRL
fi

# Get all dependencies
sudo -H pip3 install -r ${HOME}/QRL/requirements.txt | grep -v 'Requirement already satisfied' | cat

# Execute phase
echo "Boot phase: ${BOOT_PHASE}"
case "${BOOT_PHASE}" in
        freeze)
            tail -f /dev/null
            ;;
        bootstrap)
            echo "Collect Wallets"
            python3 ${HOME}/QRL/start_qrl.py -q --get-wallets > ${HOME}/.qrl/wallet_address
            ;;
         
        start)
            python3 ${HOME}/QRL/start_qrl.py -l DEBUG
            ;;
        *)
            echo $"Usage: $0 {bootstrap|start}"
            exit 1
esac
