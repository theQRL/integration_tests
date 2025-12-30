> [!NOTE]
> This code relates to version 1.x of QRL, the world's first open-source PQ blockchain, which has been securing digital assets since December 2016.
> The next generation of QRL, version 2.0, is in development and has its own repositories. See [this discussion page](https://github.com/orgs/theQRL/discussions/2).

[![CircleCI](https://circleci.com/gh/theQRL/integration_tests.svg?style=svg)](https://circleci.com/gh/theQRL/integration_tests)
[![MIT licensed](https://img.shields.io/badge/license-MIT-blue.svg)](https://raw.githubusercontent.com/theQRL/qrllib/master/LICENSE)

# QRL Integration Tests

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

When running locally, it might be useful to run the `debug` job
Example:
```bash
circleci build --job debug
```
This job is not run in the CI server but can be used locally to test different scenarios, filter specific tests, etc.
