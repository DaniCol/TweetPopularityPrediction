#include <cppkafka/cppkafka.h>
#include <string>

#include "../include/tweetoscopeConsumer.hpp"
#include "../include/tweetoscopeCollectorParams.hpp"

tweetoscope::Consumer::Consumer(tweetoscope::params::collector& params)
  : cppkafka::Consumer(
      cppkafka::Configuration{
        { "metadata.broker.list", params.kafka.brokers},
        { "enable.auto.commit", false },
        { "auto.offset.reset", "earliest" },
        { "group.id", "tweetoscopeConsumer" }
      }
    ), 
  topic(params.topic.in) {}

void tweetoscope::Consumer::subscribe_topic(){
  this->subscribe({this->topic});
}

std::string tweetoscope::Consumer::get_topic(){
    return this->topic;
}