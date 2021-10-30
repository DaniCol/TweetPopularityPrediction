#pragma once
#include <map>
#include <queue>
#include <memory>
#include <memory>
#include <iostream>
#include <iomanip>
#include <string>
#include <vector>
#include <boost/heap/binomial_heap.hpp>

#include "tweetoscopeCascade.hpp"
#include "tweetoscopeProducer.hpp"
#include "tweetoscopeTweetReader.hpp"

namespace tweetoscope{

    class Processor{

        private:
        // Class attributes
            ref_producer serie_producer;
            ref_producer properties_producer;
            tweetoscope::timestamp max_duration;

            tweetoscope::priority_queue cascades;
            std::map<tweetoscope::timestamp, std::queue<tweetoscope::refw_cascade>> partial_cascades;
            std::map<tweetoscope::cascade::idf, tweetoscope::refw_cascade> symbol_table;

        // Class methods
            void process_tweet(tweetoscope::cascade::idf key, tweetoscope::tweet& tweet);
            void process_retweet(tweetoscope::tweet& retweet);
            void extract_cascade(tweetoscope::timestamp current_tweet_time);


        public:
        // Class constructors
            inline Processor(ref_producer serie_producer, ref_producer properties_producer, tweetoscope::timestamp max_duration) 
                : serie_producer(serie_producer),
                  properties_producer(properties_producer),
                  max_duration(max_duration),
                  cascades(),
                  partial_cascades(), 
                  symbol_table() {} ;

            Processor(const Processor&) = default;
            Processor& operator=(const Processor&) = default;

            ~Processor() = default;


        // Class methods
            void process(tweetoscope::cascade::idf key, tweetoscope::tweet& msg);
            void publish_cascade_serie();
            void publish_cascade_properties();
            std::string create_serie_msg();
            std::string create_properties_msg();

    };

}
