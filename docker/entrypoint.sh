#!/bin/sh

export RDK_PREFIX=/usr/local 
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$RDK_PREFIX/lib
export KAFKA_PATH=/kafka-2.4.1-src
cd /home/tweetoscope
/bin/bash "$@"
