#!/usr/bin/env python3

# Author: Burton Swan <eucalypts@protonmail.com>

import logging
import os
import pytest
import subprocess
import sys


log = logging.getLogger('test_coin_transfer')


def get_qrl_src():
    """Pull the latest QRL source code."""
    repo_url = 'https://github.com/theQRL/QRL.git'
    try:
        subprocess.check_call(['git', 'clone', repo_url])
    except subprocess.CalledProcessError:
        raise


def test_create_wallet():
    """Generate a wallet via wallet_gen"""
    try:
        subprocess.check_call(['python3', 'QRL/qrl/cli.py', 'wallet_gen'])
    except subprocess.CalledProcessError as error:
        log.error(error)
        raise
    assert True


def test_add_wallet():
    """Add a wallet via wallet_add"""
    try:
        subprocess.check_call(['python3', 'QRL/qrl/cli.py', 'wallet_add'])
    except subprocess.CalledProcessError as error:
        log.error(error)
        raise
    assert True


def test_list_wallet():
    """List all existing wallets via wallet_ls for validation.

    Check points:
    1. There should be 2 wallets in total.
    2. Each wallet should have a unique index.
    3. Each wallet should have a unique address.
    """

    try:
        wallet_list = subprocess.check_output(
            ['python3', 'QRL/qrl/cli.py', 'wallet_ls'])
    except subprocess.CalledProcessError as error:
        log.error(error)
        raise

    # TODO: Output from wallet_ls need to be parsered to check the details.
    assert True


def clean_up():
    """Remove cloned QRL repo and all wallets created."""
    try:
        subprocess.check_call(['rm', '-rf', 'QRL'])
    except subprocess.CalledProcessError:
        raise
    try:
        subprocess.check_call(['rm', '-rf', 'wallet.qrl'])
    except subprocess.CalledProcessError:
        raise


def main():
    """Run this scenario in sequence."""
    get_qrl_src()
    test_create_wallet()
    test_add_wallet()
    test_list_wallet()
    clean_up()
    return 0


if __name__ == '__main__':
    sys.exit(main())
