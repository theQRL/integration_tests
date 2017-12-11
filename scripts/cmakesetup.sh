#!/usr/bin/env bash
wget https://cmake.org/files/v3.10/cmake-3.10.0.tar.gz
tar zxf cmake-3.10.0.tar.gz
cd cmake-3.10.0 && ./configure --prefix=/usr && make -j2 && sudo make install