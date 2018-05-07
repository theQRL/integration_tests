#!/usr/bin/env bash
# Distributed under the MIT software license, see the accompanying
# file LICENSE or http://www.opensource.org/licenses/mit-license.php.
source ${BASH_SOURCE%/*}/set_env.sh
###############

echo
source ${VENV_PATH}/bin/activate
export PYTHONPATH=${SOURCE_PATH}/src
cpulimit -l 30 -- ${SOURCE_PATH}/start_qrl.py --mockGetMeasurement 1000 --miningAddress Q010500327b3cd777e1ecab93df873ea335de3413283ff2ba4a7ff577ef979eb99a54e06590f466 -l DEBUG "$@"

