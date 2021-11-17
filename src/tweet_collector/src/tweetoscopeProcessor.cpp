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

    // Add the cascade to the symbol table
    symbol_table.insert((std::make_pair(tweet.cid,refw)));

    // Add the cascade to partial cascade
    std::map<tweetoscope::timestamp, std::queue<tweetoscope::refw_cascade>>::iterator it;
    for (it = partial_cascades.begin(); it != partial_cascades.end(); it++){
        it->second.push(refw);
    }
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

    while(!cascades.empty() && 
          current_tweet_time - cascades.top()->get_last_event_time() > this->max_duration){
        // Kill the cascade
        auto cascade = cascades.top();
        cascade->kill();

        // Publish in cascade properties
        this->publish_cascade_properties();

        // Pop from the priority queue
        cascades.pop();   
    }
}

void tweetoscope::Processor::publish_cascade_serie(){}

void tweetoscope::Processor::publish_cascade_properties(){}

std::string tweetoscope::Processor::create_serie_msg(){return "0";}

std::string tweetoscope::Processor::create_properties_msg(){return "0";}
