# Image based on the default ubuntu image 
FROM ubuntu

# Install Basics 
RUN DEBIAN_FRONTEND=noninteractive apt-get update --yes; DEBIAN_FRONTEND=noninteractive apt-get install -y wget ; DEBIAN_FRONTEND=noninteractive apt-get install -y curl ; DEBIAN_FRONTEND=noninteractive apt install -y build-essential pkg-config python-dev python-six cython python-numpy coinor-libipopt1v5 coinor-libipopt-dev ; DEBIAN_FRONTEND=noninteractive apt install -y default-jdk

# Install Kafka 
RUN wget https://archive.apache.org/dist/kafka/2.4.1/kafka-2.4.1-src.tgz ; tar zxvf kafka-2.4.1-src.tgz

# Build kafka
RUN cd ./kafka-2.4.1-src ; ./gradlew jar -PscalaVersion=2.12.10

# Install Boost 
RUN apt install -y libboost-all-dev ; apt install -y aptitude ; aptitude search boost


#RUN wget https://boostorg.jfrog.io/native/main/release/1.77.0/source/boost_1_77_0.tar.gz ; tar xzvf boost_1_77_0.tar.gz ; cd boost_1_77_0/