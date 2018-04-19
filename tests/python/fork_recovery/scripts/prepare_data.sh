#!/usr/bin/env bash
# Distributed under the MIT software license, see the accompanying
# file LICENSE or http://www.opensource.org/licenses/mit-license.php.
SCRIPT_PATH="$( cd "$(dirname "$0")" ; pwd -P )"

cd SCRIPT_PATH/../../.../../
mkdir -p tmp/data
cd tmp/data

# Get Fork Testing Data
git clone https://github.com/cyyber/testing_data --depth=1

rm -rf ~/project/mocknet/data/node000
rm -rf ~/project/mocknet/data/node001

mv testing_data/fork_recovery/.qrl_150 ~/project/mocknet/data/node000
mv testing_data/fork_recovery/.qrl_200 ~/project/mocknet/data/node001
