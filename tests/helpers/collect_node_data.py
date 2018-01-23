#!/usr/bin/env python3
import glob

node_ip_sources = []
for filename in glob.iglob('../../volumes/**/node_ip', recursive=True):
    node_ip_sources.append(filename)
print(node_ip_sources)
# Get all ips
node_ips = []
for s in node_ip_sources:
    with open(s) as f:
        tmp = f.readline().strip()
        if '127.0.0.1' not in tmp:
            node_ips.append(tmp)

node_ips = sorted(node_ips)
with open('./nodes_scripts/config.yml', 'w') as f:
    if len(node_ips) > 0:
        f.write("peer_list:\n")
        for ip in node_ips:
            f.write("- '{}'\n".format(ip, ))
