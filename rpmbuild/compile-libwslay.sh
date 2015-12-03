#!/bin/sh

set -e

echo "------------------------------------- libwslay complie has been started"

cd /tmp

git clone --recursive https://github.com/tatsuhiro-t/wslay

cd wslay

autoreconf -i
automake
autoconf

sed -r -i 's/^(SUBDIRS = lib tests examples) doc.*/\1/' Makefile.in

./configure --prefix=/usr --enable-shared="" --disable-shared
make
make install

echo "------------------------------------- libwslay has been complied and installed"
