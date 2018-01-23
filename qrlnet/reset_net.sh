#!/bin/bash
pushd . > /dev/null
cd $( dirname "${BASH_SOURCE[0]}" )

docker-compose stop
docker-compose rm -f
rm -rf volumes

popd > /dev/null
