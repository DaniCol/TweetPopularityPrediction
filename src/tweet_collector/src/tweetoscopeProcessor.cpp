#include <chrono>
#include <ctime>

#include "../include/tweetoscopeProcessor.hpp"

void tweetoscope::Processor::process(tweetoscope::cascade::idf key, tweetoscope::tweet& msg){
    
    if(msg.type == "tweet"){
        process_tweet(key, msg);
        return;
    }

    process_retweet(key,msg);

}

void tweetoscope::Processor::process_tweet(tweetoscope::cascade::idf key, tweetoscope::tweet& tweet){

    std::cout <<"PROCESS TWEET" << key << std::endl;

    ref_cascade ref = tweetoscope::make_cascade(key,tweet);
    
    refw_cascade refw = ref;

    ref->location = this->cascades.push(ref);

    symbol_table.insert((std::make_pair(key,refw)));

    extract_cascade(tweet.time);

}


void tweetoscope::Processor::process_retweet(tweetoscope::cascade::idf key, tweetoscope::tweet& retweet){

    try{
        auto cascade = symbol_table.at(key).lock();

        if(cascade!=nullptr){

            // std::cout <<"PROCESS RETWEET" << key << std::endl;

            cascade->update_cascade(retweet);

            // std::cout << *cascade << std::endl;
        }

    }catch(std::exception& e) {
        std::cout << "Exception caught : " << e.what() << std::endl;
    }

}

void tweetoscope::Processor::extract_cascade(tweetoscope::timestamp current_tweet_time){

    bool clear = false;

    while(!clear){

        auto cascade = cascades.top();

        if(cascade!=nullptr){
            std::cout << current_tweet_time << std::endl;
            std::cout << cascade->get_last_event_time() << std::endl;

            tweetoscope::timestamp duration_between_tweets = abs(current_tweet_time - cascade->get_last_event_time());

            std::cout << "Duration between tweets : " << duration_between_tweets << "|| Max duration: " << this->max_duration << std::endl;

            if(duration_between_tweets > this->max_duration){
                std::cout << "POPPED" << std::endl;
                cascade->kill();
                cascades.pop();
                
                // std::cout << cascade->is_dead() << std::endl;
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
