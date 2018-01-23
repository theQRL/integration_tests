#!/usr/bin/env python3
from __future__ import print_function

import socket
import sys

import docker


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def get_main_ip(container):
    return container.attrs['NetworkSettings']['Networks']['qrlnet_default']['IPAddress']


def get_container_from_name(container_name):
    client = docker.from_env()
    for cont in client.containers.list():
        if cont.id.startswith(container_name):
            return cont


def get_container_from_hash(container_hash):
    client = docker.from_env()
    for cont in client.containers.list():
        if cont.id.startswith(container_hash):
            return cont


if __name__ == '__main__':
    hostname = socket.gethostname()
    c = get_container_from_hash(hostname)
    if c is not None:
        print(c.name)
