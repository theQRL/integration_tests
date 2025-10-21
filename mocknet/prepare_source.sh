#!/usr/bin/env bash
# Distributed under the MIT software license, see the accompanying
# file LICENSE or http://www.opensource.org/licenses/mit-license.php.
source ${BASH_SOURCE%/*}/set_env.sh
###############

echo
export REPO_SLUG='theQRL/QRL'
export REPO_BRANCH='noble'

# Clean up
rm -rf ${VENV_PATH}
rm -rf ${SOURCE_PATH}

if [ ! -z ${TESTINPLACE:-} ]; then
    rsync -qar . ${SOURCE_PATH} --exclude tests_integration # > /dev/null
else
    # Get source code
    git clone -b ${REPO_BRANCH} https://github.com/${REPO_SLUG}.git ${SOURCE_PATH} --depth=1
    cp ${SOURCE_PATH}/src/qrl/generated/* qrl/generated/
fi

# Prepare clean virtual environment to run the tests
python3 -m venv ${VENV_PATH} --system-site-packages
source ${VENV_PATH}/bin/activate

# Install dependencies
pip install -U setuptools
pip install -U mock
pip install -U -r ${SOURCE_PATH}/requirements.txt
