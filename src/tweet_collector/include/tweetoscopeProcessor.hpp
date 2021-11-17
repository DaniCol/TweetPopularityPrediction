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

    class Processor;

    using ref_processor = std::shared_ptr<tweetoscope::Processor>;
    
    class Processor{

        private:
        // Class attributes
            ref_producer serie_producer;
            ref_producer properties_producer;
            tweetoscope::timestamp max_duration;
            int min_cascade_size;

            tweetoscope::priority_queue cascades;
            std::map<tweetoscope::timestamp, std::queue<tweetoscope::refw_cascade>> partial_cascades;
            std::map<tweetoscope::cascade::idf, tweetoscope::refw_cascade> symbol_table;

        // Class methods
            void process_tweet(tweetoscope::tweet& tweet);
            void process_retweet(tweetoscope::tweet& retweet);
            void extract_cascade(tweetoscope::timestamp current_tweet_time);
            void extract_from_partial_cascade(tweetoscope::timestamp current_tweet_time);


        public:
        // Class constructors
            Processor(  ref_producer serie_producer, 
                        ref_producer properties_producer, 
                        tweetoscope::timestamp max_duration,
                        int min_size_cascade,
                        std::vector<tweetoscope::timestamp> observation_windows);

            Processor(const Processor&) = default;
            Processor& operator=(const Processor&) = default;

            ~Processor() = default;


        // Class methods
            void process(tweetoscope::tweet& msg);
            void publish_cascade_serie(tweetoscope::ref_cascade ref, tweetoscope::timestamp time_window);
            void publish_cascade_properties(tweetoscope::ref_cascade ref, tweetoscope::timestamp time_window);

    };

    inline ref_processor make_processor(ref_producer serie_producer, 
                        ref_producer properties_producer, 
                        tweetoscope::timestamp max_duration,
                        int min_size_cascade,
                        std::vector<tweetoscope::timestamp> observation_windows){
        return std::make_shared<tweetoscope::Processor>(
            serie_producer,
            properties_producer,
            max_duration,
            min_size_cascade,
            observation_windows
            );
    }
}
