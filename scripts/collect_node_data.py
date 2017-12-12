#!/usr/bin/env python3
import glob

wallet_sources = []
for filename in glob.iglob('./volumes/**/wallet_address', recursive=True):
    wallet_sources.append(filename)

node_ip_sources = []
for filename in glob.iglob('./volumes/**/node_ip', recursive=True):
    node_ip_sources.append(filename)

# Get all wallets
wallets = []
for s in wallet_sources:
    with open(s) as f:
        wallets.append(f.readline().strip())

wallets = sorted(wallets)
with open('./scripts/genesis.yml', 'w') as f:
    f.write("genesis_info:\n")
    for w in wallets:
        if len(w) < 1:
            print("ERROR. EMPTY ADDRESS")
        f.write("  {} : 200000000000000\n".format(w, ))

print(wallets)

# Get all ips
node_ips = []
for s in node_ip_sources:
    with open(s) as f:
        tmp = f.readline().strip()
        if '127.0.0.1' not in tmp:
            node_ips.append(tmp)

node_ips = sorted(node_ips)
with open('./scripts/config.yml', 'w') as f:
    if len(node_ips) > 0:
        f.write("peer_list:\n")
        for ip in node_ips:
            f.write("- '{}'\n".format(ip, ))
