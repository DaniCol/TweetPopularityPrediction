#!/bin/bash

export KAFKA_PATH=/kafka-2.4.1-src
chmod +x ./kafka.sh
./kafka.sh --help 
./kafka.sh start --zooconfig zookeeper.properties --serverconfig server.properties 
