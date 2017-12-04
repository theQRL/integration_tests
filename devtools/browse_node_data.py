#!/usr/bin/env python3

import sys, os
import docker

cli = docker.Client(base_url='unix://var/run/docker.sock')
nodes = cli.containers()
nodes.sort(key=lambda x: x['Labels']['com.docker.compose.container-number'])

for node in nodes:
    node_index = int(node['Labels']['com.docker.compose.container-number'])
    node_id = node['Id'][:12]
    print('----- Node #{}: {} -----'.format(node_index, node_id))
    import code; code.interact(local=dict(globals(), **locals()))
