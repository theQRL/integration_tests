#!/bin/sh
SCRIPT_PATH="$(dirname "$(readlink --canonicalize-existing "$0")")"

rm -rf ~/.qrl
mkdir -p $HOME/.qrl
cp ${SCRIPT_PATH}/scripts/config.yml $HOME/.qrl/config.yml
cp ${SCRIPT_PATH}/scripts/genesis.yml $HOME/.qrl/genesis.yml
