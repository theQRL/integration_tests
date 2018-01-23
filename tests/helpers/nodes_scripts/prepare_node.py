import sys
import socket
import json

sys.path.append("/root/scripts/")


def prepare():
    from test_metadata import wallets, transactions, genesis_balance
    from docker_helper import get_container_from_hash

    hostname = socket.gethostname()
    c = get_container_from_hash(hostname)
    if not c:
        return

    docker_name = c.name

    node_number = int(docker_name.split('node_')[1])
    with open('/home/testuser/.qrl/wallet/wallet.json', 'w') as f:
        json.dump([wallets[node_number - 1]], f)

    with open('/home/testuser/QRL/qrl/core/genesis.json', 'r') as f:
        genesis = json.load(f)

    genesis['transactions'] = transactions
    genesis['genesis_balance'] = genesis_balance

    with open('/home/testuser/.qrl/genesis.json', 'w') as f:
        json.dump(genesis, f)


if __name__ == '__main__':
    prepare()
