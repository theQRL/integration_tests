#!/usr/bin/env bash
# Distributed under the MIT software license, see the accompanying
# file LICENSE or http://www.opensource.org/licenses/mit-license.php.
source ${BASH_SOURCE%/*}/set_env.sh
###############

echo
export PYTHONPATH=${SOURCE_PATH}/src
python ${SOURCE_PATH}/start_qrl.py -l DEBUG "$@"

