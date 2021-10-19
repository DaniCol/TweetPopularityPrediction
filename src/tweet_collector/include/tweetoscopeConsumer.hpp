#pragma once
#include <string>
#include <cppkafka/cppkafka.h>
#include "tweetoscopeCollectorParams.hpp"

namespace tweetoscope{
  class Consumer : public cppkafka::Consumer {
    private:
      // Class attribute
      std::string topic;
        
    public:
      // Class constructor
      Consumer(tweetoscope::params::collector& params);

      // Class method
      void subscribe_topic();
      std::string get_topic();
  };
}
