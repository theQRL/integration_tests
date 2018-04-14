#!/usr/bin/env bash
SCRIPT_PATH="$(dirname "$(readlink --canonicalize-existing "$0")")"
SOURCE_PATH=${SCRIPT_PATH}/src
VENV_PATH=${SCRIPT_PATH}/venv

echo
source ${VENV_PATH}/bin/activate
export PYTHONPATH=${SOURCE_PATH}/src
${SOURCE_PATH}/start_qrl.py -l DEBUG "$@"

