#!/usr/bin/env python
from __future__ import print_function
import docker
import socket


def get_name():
    client = docker.from_env()
    hostname = socket.gethostname()

    for c in client.containers.list():
        print(c.id, c.name)
        if c.id == hostname:
            print(c.name)
            quit()


if __name__ == '__main__':
    get_name()
