#!/usr/bin/env bash
export REPO_SLUG='theQRL/QRL'
export REPO_BRANCH='master'

SCRIPT_PATH="$(dirname "$(readlink --canonicalize-existing "$0")")"
SOURCE_PATH=${SCRIPT_PATH}/src
VENV_PATH=${SCRIPT_PATH}/venv

rm -rf ${SOURCE_PATH}
rm -rf ${VENV_PATH}

echo
python3 -m venv ${VENV_PATH}
source ${VENV_PATH}/bin/activate
git clone -b ${REPO_BRANCH} https://github.com/${REPO_SLUG}.git ${SOURCE_PATH} --depth=1
pip install -U -r ${SOURCE_PATH}/requirements.txt

