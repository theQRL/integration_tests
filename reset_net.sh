#!/bin/sh
docker-compose kill
docker-compose rm -f
rm -rf volumes
