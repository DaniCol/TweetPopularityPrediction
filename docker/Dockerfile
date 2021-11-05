# Image based on the default ubuntu image 
FROM ubuntu

# Install Everything  
RUN mkdir /install_script
COPY ./install_script/install_basics.sh  /install_script/install_basics.sh 
RUN /install_script/install_basics.sh 

# Get packages from the internet
RUN git clone https://github.com/HerveFrezza-Buet/gaml 
RUN wget https://archive.apache.org/dist/kafka/2.4.1/kafka-2.4.1-src.tgz 

COPY ./install_script/install_gaml.sh  /install_script/install_gaml.sh 
RUN /install_script/install_gaml.sh

COPY ./install_script/install_kafka.sh  /install_script/install_kafka.sh 
RUN /install_script/install_kafka.sh 

COPY ./install_script/install_boost.sh  /install_script/install_boost.sh 
RUN /install_script/install_boost.sh 

COPY ./install_script/install_cppkafka.sh  /install_script/install_cppkafka.sh 
RUN /install_script/install_cppkafka.sh

COPY ./install_script/install_python_packages.sh  /install_script/install_python_packages.sh 
RUN /install_script/install_python_packages.sh

COPY ./entrypoint.sh entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]
