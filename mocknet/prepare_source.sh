#!/usr/bin/env bash
export REPO_SLUG='theQRL/QRL'
export REPO_BRANCH='master'

SCRIPT_PATH="$(dirname "$(readlink --canonicalize-existing "$0")")"
SOURCE_PATH=${SCRIPT_PATH}/src

git clone -b ${REPO_BRANCH} https://github.com/${REPO_SLUG}.git ${SOURCE_PATH} --depth=1
pip3 install -U -r ${SOURCE_PATH}/requirements.txt
