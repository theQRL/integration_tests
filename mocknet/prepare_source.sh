#!/usr/bin/env bash
# Distributed under the MIT software license, see the accompanying
# file LICENSE or http://www.opensource.org/licenses/mit-license.php.
export REPO_SLUG='theQRL/QRL'
export REPO_BRANCH='master'
echo

SCRIPT_PATH="$(dirname "$(readlink --canonicalize-existing "$0")")"
SOURCE_PATH=${SCRIPT_PATH}/src
VENV_PATH=${SCRIPT_PATH}/venv

# Clean up
rm -rf ${VENV_PATH}
rm -rf ${SOURCE_PATH}

# Prepare clean virtual environment to run the tests
python3 -m venv ${VENV_PATH}
source ${VENV_PATH}/bin/activate

# Get source code
git clone -b ${REPO_BRANCH} https://github.com/${REPO_SLUG}.git ${SOURCE_PATH} --depth=1

# Install dependencies
pip install -U setuptools
pip install -U pip
pip install -U mock
pip install -U -r ${SOURCE_PATH}/requirements.txt
