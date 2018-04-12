#!/bin/bash -u


sh ../../qrlnet/clone_repo.sh

git clone https://github.com/cyyber/testing_data ~/testing_data --depth=1
mv ~/testing_data/fork_recovery/.qrl_150 ~/.qrl1
mv ~/testing_data/fork_recovery/.qrl_200 ~/.qrl2
