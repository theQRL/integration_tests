from time import sleep
import pytest
import json
import decimal
from collections import namedtuple

from qrlnet.nodes_scripts.docker_helper import get_container_from_name

AddressRepr = namedtuple('AddressRepr', ['number', 'address', 'balance'])
WalletRepr = namedtuple('WalletRepr', ['location', 'addresses'])


def parse_wallet_response(o: str):
    # strip() is needed before splitlines(), otherwise splitlines() will have a '' as the last line
    o = o.strip().splitlines()

    location = o[0].split()[-1]
    addresses = []
    for line in o[3:]:
        i, address, balance = line.split()
        a = AddressRepr(number=i, address=address, balance=decimal.Decimal(balance))
        addresses.append(a)

    w = WalletRepr(location=location, addresses=addresses)
    return w


def wait_blocks(x, node):
    state_initial = json.loads(node.exec_run("qrl --json state").decode())
    """
      "info": {
        "uptime": "25",
        "blockHeight": "1023", // might be absent when testnet has just started
        "version": "0.61.3.post0.dev1+nge4c5f93.dirty",
        "networkId": "The Burning Ice",
        "state": "UNSYNCED",
        "numKnownPeers": 44,
        "numConnections": 4
      }
    }
     """
    while 'blockHeight' not in state_initial["info"]:
        print("node does not have a blockHeight yet, waiting")
        sleep(10)
        state_initial = json.loads(node.exec_run("qrl --json state").decode())

    height = int(state_initial["info"]["blockHeight"])
    while height < int(state_initial["info"]["blockHeight"]) + x:
        sleep(30)
        state = json.loads(node.exec_run("qrl --json state").decode())
        height = int(state["info"]["blockHeight"])


def printloud(text):
    # FIXME: accepts *args just like print()
    print("\032[0m\032[45m{} {} {}\032[0m".format('*' * 15, text, '*' * 15), flush=True)


def wallet_ls(node):
    return node.exec_run("qrl --wallet_dir /home/testuser/.qrl/wallet wallet_ls").decode()


def wallet_gen(node):
    return node.exec_run("qrl --wallet_dir /home/testuser/.qrl/wallet wallet_gen").decode()


@pytest.mark.balances_available
def test_balances_available():
    node_1 = get_container_from_name('node_1')

    node_1_gen = wallet_gen(node_1)
    wait_blocks(2, node_1)
    node_1_ls = wallet_ls(node_1)

    try:
        parse_wallet_response(node_1_ls)
    except decimal.InvalidOperation:
        assert False

    assert True

@pytest.mark.wallet_transfer
def test_wallet_transfer():
    node_1 = get_container_from_name('node_1')
    node_2 = get_container_from_name('node_2')

    print("wallet_transfer test started, generating wallets", flush=True)
    node_1_gen = wallet_gen(node_1)

    wait_blocks(2, node_1)
    src_wallet_1 = parse_wallet_response(wallet_ls(node_1))

    node_2_gen = wallet_gen(node_2)
    dst_wallet_1 = parse_wallet_response(wallet_ls(node_2))

    amount = 50
    fee = 13

    print("Sending transaction", flush=True)
    output = node_1.exec_run(
        ["qrl", "--wallet_dir", src_wallet_1.location, "-r", "tx_transfer", "--src",
         src_wallet_1.addresses[0].number, "--dst", dst_wallet_1.addresses[0].address,
         "--amounts", str(amount), "--fee", str(fee), "--ots_key_index", "0"]).decode().strip()
    if 'SUBMITTED' not in output:
        print("tx_transfer does not appear to have succeeded", output, flush=True)
        assert False

    print("TX sent. Waiting for 3 blocks to go by...", flush=True)
    wait_blocks(3, node_1)

    src_wallet_2 = parse_wallet_response(wallet_ls(node_1))
    dst_wallet_2 = parse_wallet_response(wallet_ls(node_2))

    src_balance_correct = src_wallet_2.addresses[0].balance == (src_wallet_1.addresses[0].balance - (amount + fee))
    dst_balance_correct = dst_wallet_2.addresses[0].balance == (dst_wallet_1.addresses[0].balance + amount)
    if src_balance_correct and dst_balance_correct:
        assert True
    else:
        print("src_balance_correct", src_balance_correct, src_wallet_2.addresses[0].balance)
        print("dst_balance_correct", dst_balance_correct, dst_wallet_2.addresses[0].balance)
        assert False
