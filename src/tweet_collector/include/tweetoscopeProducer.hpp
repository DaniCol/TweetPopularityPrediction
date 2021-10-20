#pragma once
#include <string>
#include <cppkafka/cppkafka.h>
#include "tweetoscopeCollectorParams.hpp"

namespace tweetoscope{
  class Producer : public cppkafka::Producer {
    private:
      // Class attribute
      std::string topic;
    public:
      // Class constructor
      Producer(tweetoscope::params::collector& params, std::string out_topic);

      // Class method
      void post_msg(std::string key, std::string msg);
  };
}