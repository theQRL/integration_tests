[![CircleCI](https://circleci.com/gh/theQRL/integration_tests.svg?style=svg)](https://circleci.com/gh/theQRL/integration_tests)
[![MIT licensed](https://img.shields.io/badge/license-MIT-blue.svg)](https://raw.githubusercontent.com/theQRL/qrllib/master/LICENSE)

# QRL Integration Tests

This project periodically runs integration tests on a 6 node testnet

## How to run integration tests

Get CircleCI CLI (https://circleci.com/docs/2.0/local-cli/#installing-the-circleci-local-cli-on-macos-and-linux-distros)

Clone this repo and run:

```bash
circleci build
```

if you want to run some specific group/job, you can select it by using:
```bash
circleci build --job JOB_NAME
```

where JOB_NAME is one of the job described in `.circleci/config.yml`.

Example:
```bash
circleci build --job tests_js
```
