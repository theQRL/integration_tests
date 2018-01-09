#!/usr/bin/env python
from __future__ import print_function
import docker
import socket

import sys


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def get_main_ip(container):
    return container.attrs['NetworkSettings']['Networks']['integrationtests_default']['IPAddress']


def get_container_from_name(container_name):
    client = docker.from_env()
    containers = client.containers.list()
    for cont in containers:
        if container_name in cont.name:
            return cont

    names = ', '.join([cont.name for cont in containers])
    raise Exception("couldn't find {} - valid names are {}".format(container_name, names))


def get_container_from_hash(container_hash):
    client = docker.from_env()
    containers = client.containers.list()
    for cont in containers:
        if cont.id.startswith(container_hash):
            return cont

    ids = ', '.join([cont.id for cont in containers])
    raise Exception("couldn't find {} - valid hashes are {}".format(container_hash, ids))

if __name__ == '__main__':
    hostname = socket.gethostname()
    c = get_container_from_hash(hostname)
    if c is not None:
        print(c.name)
