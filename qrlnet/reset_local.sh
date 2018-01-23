#!/usr/bin/env bash
SCRIPT_PATH="$(dirname "$(readlink --canonicalize-existing "$0")")"

rm -rf ~/.qrl
mkdir -p $HOME/.qrl
