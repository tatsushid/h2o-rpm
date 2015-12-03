#!/bin/sh

set -e

echo "------------------------------------- libuv compile has been started"

cd /tmp

git clone --recursive https://github.com/libuv/libuv

cd libuv
git checkout v1.7.5

sh autogen.sh
./configure --prefix=/usr --enable-shared="" --disable-shared
make
make install

echo "------------------------------------- libuv has been complied and installed"
