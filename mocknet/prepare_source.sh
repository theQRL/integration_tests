#!/usr/bin/env bash
# Distributed under the MIT software license, see the accompanying
# file LICENSE or http://www.opensource.org/licenses/mit-license.php.
source ${BASH_SOURCE%/*}/set_env.sh
###############

echo
export REPO_SLUG='theQRL/QRL'
export REPO_BRANCH='master'

# Clean up
rm -rf ${VENV_PATH}
rm -rf ${SOURCE_PATH}

# Prepare clean virtual environment to run the tests
python3 -m venv ${VENV_PATH} --system-site-packages
source ${VENV_PATH}/bin/activate

# Get source code
git clone -b ${REPO_BRANCH} https://github.com/${REPO_SLUG}.git ${SOURCE_PATH} --depth=1

cp ${SOURCE_PATH}/src/qrl/generated/* qrl/generated/

# Install dependencies
pip install -U setuptools
pip install -U pip
pip install -U mock
pip install -U -r ${SOURCE_PATH}/requirements.txt
