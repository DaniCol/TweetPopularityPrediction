#include <chrono>
#include <ctime>

#include "../include/tweetoscopeProcessor.hpp"

void tweetoscope::Processor::process(tweetoscope::cascade::idf key, tweetoscope::tweet& msg){
    
    if(msg.type == "tweet"){
        process_tweet(key, msg);
        return;
    }

    process_retweet(msg);

}

void tweetoscope::Processor::process_tweet(tweetoscope::cascade::idf key, tweetoscope::tweet& tweet){

    std::cout <<"PROCESS TWEET" << key << std::endl;

    ref_cascade ref = tweetoscope::make_cascade(key,tweet);
    refw_cascade refw = ref;

    std::cout << *ref << std::endl;

    ref->location = this->cascades.push(ref);

    symbol_table.insert(std::make_pair(key,refw));
    
    auto symbol = symbol_table.at(key).lock();
    std::cout << *symbol << std::endl;

    // extract_cascade(tweet.time);
}


void tweetoscope::Processor::process_retweet(tweetoscope::tweet& retweet){
    // std::cout <<"PROCESS RETWEET" << std::endl;
    
}

void tweetoscope::Processor::extract_cascade(tweetoscope::timestamp current_tweet_time){

    bool clear = false;

    while(!clear){
        auto cascade = cascades.top();
        if(cascade!=nullptr){
            std::cout << "Duration : " << current_tweet_time - cascade->get_last_event_time() << std::endl;
            std::cout << "Max Duration : " << this->max_duration << std::endl;

            if(current_tweet_time - cascade->get_last_event_time() > this->max_duration){
                std::cout << "POPPED: " << *cascade << std::endl;
                cascades.pop();
            }else{
                clear = true;
            }
        } else{
            clear = true;
        }
    }
}

void tweetoscope::Processor::publish_cascade_serie(){}

void tweetoscope::Processor::publish_cascade_properties(){}

std::string tweetoscope::Processor::create_serie_msg(){return "0";}

std::string tweetoscope::Processor::create_properties_msg(){return "0";}
