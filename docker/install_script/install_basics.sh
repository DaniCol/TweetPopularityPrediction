#!/bin/sh

DEBIAN_FRONTEND=noninteractive apt-get update --yes
DEBIAN_FRONTEND=noninteractive apt-get install -y wget
DEBIAN_FRONTEND=noninteractive apt-get install -y curl 
DEBIAN_FRONTEND=noninteractive apt-get install -y git
DEBIAN_FRONTEND=noninteractive apt-get install -y cmake 
DEBIAN_FRONTEND=noninteractive apt install -y build-essential pkg-config python-dev python-six cython python-numpy coinor-libipopt1v5 coinor-libipopt-dev
DEBIAN_FRONTEND=noninteractive apt install -y default-jdk 
