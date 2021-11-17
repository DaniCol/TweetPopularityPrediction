#include <cppkafka/cppkafka.h>
#include <string>

#include "../include/tweetoscopeProducer.hpp"
#include "../include/tweetoscopeCollectorParams.hpp"

tweetoscope::Producer::Producer(tweetoscope::params::collector& params, std::string out_topic)
  : cppkafka::Producer(
      cppkafka::Configuration{
        { "metadata.broker.list", params.kafka.brokers},
        { "log.connection.close", false}
      }
    ),
    topic(out_topic){}

void tweetoscope::Producer::post_msg(std::string key, std::string msg){
  this->produce(cppkafka::MessageBuilder(this->topic).key(key).payload(msg));
}

void tweetoscope::Producer::post_msg(std::string msg){
  this->produce(cppkafka::MessageBuilder(this->topic).payload(msg));
}