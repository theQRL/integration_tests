#!/usr/bin/env bash
# Distributed under the MIT software license, see the accompanying
# file LICENSE or http://www.opensource.org/licenses/mit-license.php.

mkdir -p mocknet/data
cd mocknet/data

# Get Fork Testing Data
git clone https://github.com/cyyber/testing_data --depth=1

mv testing_data/fork_recovery/.qrl_150 node000
mv testing_data/fork_recovery/.qrl_200 node001
