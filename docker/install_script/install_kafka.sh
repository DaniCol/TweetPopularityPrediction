#!/bin/sh

# Install Kafka 
tar zxvf kafka-2.4.1-src.tgz 
rm kafka-2.4.1-src.tgz

# Build kafka
cd ./kafka-2.4.1-src 
./gradlew jar -PscalaVersion=2.12.10
