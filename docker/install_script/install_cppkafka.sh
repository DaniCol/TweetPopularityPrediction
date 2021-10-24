#!/bin/sh

apt-get install -y libtool
apt install -y libssl-dev
apt install -y librdkafka-dev
git clone https://github.com/mfontanini/cppkafka.git
cd /cppkafka
mkdir build
cd build
cmake ..
make
make install
