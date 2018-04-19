#!/usr/bin/env bash
# Distributed under the MIT software license, see the accompanying
# file LICENSE or http://www.opensource.org/licenses/mit-license.php.
SCRIPT_PATH="$( cd "$(dirname "$0")" ; pwd -P )"
PROJECT_PATH=$(cd "${SCRIPT_PATH}/../../../../"; pwd)

# Get Fork Testing Data
git clone https://github.com/cyyber/testing_data --depth=1 ${PROJECT_PATH}/tmp/testing_data

ls ${PROJECT_PATH}/tmp
ls ${PROJECT_PATH}/tmp/testing_data
ls ${PROJECT_PATH}/tmp/testing_data/fork_recovery

rm -rf ${PROJECT_PATH}/tmp/data/node000
rm -rf ${PROJECT_PATH}/tmp/data/node001

mkdir -p ${PROJECT_PATH}/tmp/data/node000
mv ${PROJECT_PATH}/tmp/testing_data/fork_recovery/.qrl_150 ${PROJECT_PATH}/tmp/data/node000
mv ${PROJECT_PATH}/tmp/testing_data/fork_recovery/.qrl_200 ${PROJECT_PATH}/tmp/data/node001
