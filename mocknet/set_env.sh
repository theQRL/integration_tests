#!/usr/bin/env bash
# Distributed under the MIT software license, see the accompanying
# file LICENSE or http://www.opensource.org/licenses/mit-license.php.
SCRIPT_PATH="$( cd "$(dirname "$0")" ; pwd -P )"
TMP_PATH="$( cd ${SCRIPT_PATH}/../tmp ; pwd -P )"
SOURCE_PATH=${TMP_PATH}/src
# VENV_PATH=${TMP_PATH}/venv

echo "SCRIPT_PATH    ${SCRIPT_PATH}"
echo "TMP_PATH       ${TMP_PATH}"
echo "SOURCE_PATH    ${SOURCE_PATH}"
echo "VENV_PATH      ${VENV_PATH}"
