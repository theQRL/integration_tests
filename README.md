[![Build Status](https://img.shields.io/travis/theQRL/integration_tests/master.svg?label=Integration_Tests)](https://travis-ci.org/theQRL/integration_tests) 
[![MIT licensed](https://img.shields.io/badge/license-MIT-blue.svg)](https://raw.githubusercontent.com/theQRL/qrllib/master/LICENSE)

# QRL Integration Tests

This project periodically runs integration tests on a 6 node testnet

## How to run integration tests

Clone this repo

You will need at least python 3.5

### Installing Docker CE / Docker compose

Follow the corresponding instructions:

|   |   |
|---|---|
|Windows | https://docs.docker.com/docker-for-windows/install/   |
|Linux   | https://docs.docker.com/engine/installation/linux/docker-ce/ubuntu/ |
|OSX     | https://docs.docker.com/docker-for-mac/install/ | 
|||

Install docker compose

`pip3 install docker-compose`

### Start Integration Tests

`python3 run_inittest.py`
