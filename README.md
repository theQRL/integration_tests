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

Run pytest
`pytest`

To run a specific scenario use -m flag

`pytest -s -m "runfor10minutes"`

To avoid running a scenario
`pytest -s  -m "not runfor10minutes"`


### Limitations

Docker for Mac has some limitations that result in problems when trying to connect from the host to the containers.
https://docs.docker.com/docker-for-mac/networking/#known-limitations-use-cases-and-workarounds

Typically in Linux, you can route traffic between your host and each of the containers without trouble using a Bridge.
This is unfortunately not possible in OSX.
