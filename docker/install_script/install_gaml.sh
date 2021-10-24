#!/bin/sh

cd gaml
mkdir -p gaml/build
cd gaml/build
cmake .. -DCMAKE_INSTALL_PREFIX=/usr
make -j
make install
cd ../..
