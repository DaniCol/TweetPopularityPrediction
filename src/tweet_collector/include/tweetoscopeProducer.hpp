#pragma once
#include <string>
#include <cppkafka/cppkafka.h>
#include <memory>
#include "tweetoscopeCollectorParams.hpp"

namespace tweetoscope{

  class Producer;

  using ref_producer = std::shared_ptr<tweetoscope::Producer>;
  class Producer : public cppkafka::Producer {
    private:
      // Class attribute
      std::string topic;
    public:
      // Class constructor
      Producer(tweetoscope::params::collector& params, std::string out_topic);

      // Class method
      void post_msg(std::string key, std::string msg);
      void post_msg(std::string msg);
  };

  inline ref_producer make_producer(tweetoscope::params::collector& params, std::string out_topic){
    return std::make_shared<tweetoscope::Producer>(params, out_topic);
  }
}