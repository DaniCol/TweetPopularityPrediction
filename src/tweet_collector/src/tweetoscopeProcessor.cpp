#include <chrono>
#include <ctime>

#include "../include/tweetoscopeProcessor.hpp"

tweetoscope::Processor::Processor(
                        ref_producer serie_producer, 
                        ref_producer properties_producer, 
                        tweetoscope::timestamp max_duration,
                        std::vector<tweetoscope::timestamp> observation_windows)
                        : serie_producer(serie_producer),
                        properties_producer(properties_producer),
                        max_duration(max_duration),
                        cascades(),
                        partial_cascades(),
                        symbol_table() 
                        {
                            for(auto& window: observation_windows)
                                partial_cascades.insert(std::make_pair(window,std::queue<tweetoscope::refw_cascade>()));
                        } ;

void tweetoscope::Processor::process(tweetoscope::tweet& msg){
    
    if(msg.type == "tweet")
        process_tweet(msg);
    else
        process_retweet(msg);
    extract_cascade(msg.time);
}

void tweetoscope::Processor::process_tweet(tweetoscope::tweet& tweet){

    std::cout <<"PROCESS TWEET " << tweet.cid << std::endl;

    ref_cascade ref = tweetoscope::make_cascade(tweet);
    refw_cascade refw = ref;

    ref->location = cascades.push(ref);
    cascades.update(ref->location,ref);

    symbol_table.insert((std::make_pair(tweet.cid,refw)));

    // partial_cascades.at();

}


void tweetoscope::Processor::process_retweet(tweetoscope::tweet& retweet){

    try{
        auto cascade = symbol_table.at(retweet.cid).lock();

        if(cascade!=nullptr){

            // std::cout <<"PROCESS RETWEET" << key << std::endl;

            cascade->update_cascade(retweet);
            
            cascades.update(cascade->location,cascade);
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
            // std::cout << current_tweet_time << std::endl;
            // std::cout << cascade->get_last_event_time() << std::endl;

            tweetoscope::timestamp duration_between_tweets = abs(current_tweet_time - cascade->get_last_event_time());

            // std::cout << "Duration between tweets : " << duration_between_tweets << "|| Max duration: " << this->max_duration << std::endl;

            if(duration_between_tweets > this->max_duration){
                // std::cout << "POPPED" << std::endl;
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
