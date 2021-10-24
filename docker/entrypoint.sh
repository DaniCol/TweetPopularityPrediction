#!/bin/sh

export RDK_PREFIX=/usr/local 
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$RDK_PREFIX/lib

/bin/bash "$@"