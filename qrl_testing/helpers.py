import docker
import json
from collections import namedtuple
from decimal import Decimal
from .IntegrationTest import IntegrationTest

AddressRepr = namedtuple('AddressRepr', ['number', 'address', 'balance'])
WalletRepr = namedtuple('WalletRepr', ['location', 'addresses'])


def parse_human_readable_output(o: str):
    o = o.splitlines()

    location = o[0].split()[-1]
    addresses = []
    for line in o[3:]:
        i, address, balance = line.split()
        a = AddressRepr(number=i, address=address, balance=Decimal(balance))
        addresses.append(a)

    w = WalletRepr(location=location, addresses=addresses)
    return w


def parse_tx_push_output(o: str):
    lastline_idx = o.rfind('}\n') + 1
    tmp_json_output = o[:lastline_idx]
    lastline = o[lastline_idx:].strip()
    return json.loads(tmp_json_output), lastline


def wallet_gen(container: docker.models.containers.Container, wallet_dir: str):
    """
    :param wallet_dir: '/home/testuser/srcwallet'
    :return: WalletRepr(location='/home/testuser/srcwallet', addresses=[AddressRepr(...),]
    """
    IntegrationTest.writeout("Generating 3rd party {} wallet".format(wallet_dir))
    o = container.exec_run(["qrl", "--wallet_dir", wallet_dir, "wallet_gen"]).decode()
    return parse_human_readable_output(o)


def wallet_ls(container: docker.models.containers.Container, wallet_dir: str):
    """
    :param wallet_dir: '/home/testuser/srcwallet'
    :return: WalletRepr(location='/home/testuser/srcwallet', addresses=[AddressRepr(...),]
    """
    IntegrationTest.writeout("Reading wallet in {}".format(wallet_dir))
    o = container.exec_run(["qrl", "--wallet_dir", wallet_dir, "wallet_ls"]).decode()
    return parse_human_readable_output(o)


def tx_push(container: docker.models.containers.Container, txblob: str):
    output = container.exec_run(
        ["qrl", "tx_push", "--txblob", txblob]).decode().strip()
    _, lastline = parse_tx_push_output(output)
    IntegrationTest.writeout("tx_push signed transaction to network: {}".format(lastline))
    return _, lastline
