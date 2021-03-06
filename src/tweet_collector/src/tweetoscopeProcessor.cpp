#include <ctime>
#include "../include/tweetoscopeProcessor.hpp"

tweetoscope::Processor::Processor(
                        ref_producer serie_producer, 
                        ref_producer properties_producer,
                        ref_producer logs_producer, 
                        tweetoscope::timestamp max_duration,
                        int min_size_cascade,
                        std::vector<tweetoscope::timestamp> observation_windows)
                        : serie_producer(serie_producer),
                        properties_producer(properties_producer),
                        logs_producer(logs_producer),
                        max_duration(max_duration),
                        min_cascade_size(min_cascade_size),
                        cascades(),
                        partial_cascades(),
                        symbol_table() 
                        {
                            for(auto& window: observation_windows)
                                partial_cascades.insert(std::make_pair(window,std::queue<tweetoscope::refw_cascade>()));
                        } ;

void tweetoscope::Processor::process(tweetoscope::tweet& msg){
    
    // Pop old cascades
    extract_cascade(msg.time);

    // Update partial cascade
    extract_from_partial_cascade(msg.time);

    // Process tweet and retweet
    if(msg.type == "tweet")
        process_tweet(msg);
    else
        process_retweet(msg);
}

void tweetoscope::Processor::process_tweet(tweetoscope::tweet& tweet){

    std::cout <<"PROCESS TWEET " << tweet.cid << std::endl;
    // Publish in logs -> Processing new tweet
    this->logs_producer->post_msg(
        "{\"t\": " + std::to_string(std::time(nullptr)) + ", "
         "\"level\": \"INFO\","
         "\"source\": \"collector\","
         "\"message\": \"Processing new tweet -> {Cascade : " + std::to_string(tweet.cid) + "}\"}"
    );
    ref_cascade ref = tweetoscope::make_cascade(tweet);
    refw_cascade refw = ref;

    ref->location = cascades.push(ref);
    cascades.update(ref->location,ref);

    // Add the cascade to the symbol table
    symbol_table.insert((std::make_pair(tweet.cid,refw)));

    // Add the cascade to partial cascades
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

        }
        else{
            // Publish in logs -> Tweet id not found in symbol -> process retweet and miss tweet
            this->logs_producer->post_msg(
                "{\"t\": " + std::to_string(std::time(nullptr)) + ", "
                 "\"level\": \"WARNING\","
                 "\"source\": \"collector\","
                 "\"message\": \"Process retweet but cascade is terminated -> {Cascade : " + std::to_string(retweet.cid) + "}\"}"
        );
        }

    }catch(std::exception& e) {
        std::cout << "Exception caught : " << e.what() << std::endl;
        // Publish in logs -> Tweet id not found in symbol -> process retweet and miss tweet
        this->logs_producer->post_msg(
            "{\"t\": " + std::to_string(std::time(nullptr)) + ", "
             "\"level\": \"ERROR\","
             "\"source\": \"collector\","
             "\"message\": \"Process retweet and missed tweet -> {Cascade : " + std::to_string(retweet.cid) + "}\"}"
        );
    }

}

void tweetoscope::Processor::extract_cascade(tweetoscope::timestamp current_tweet_time){

    while(!cascades.empty() && 
          current_tweet_time - (cascades.top())->get_last_event_time() > this->max_duration){
        // Kill the cascade
        auto cascade = cascades.top();
        cascade->kill();

        // Publish in cascade properties
        for(auto& time_window : cascade->get_windows()){
            this->publish_cascade_properties(cascade, time_window);
        }

        // Publish in logs -> Cascade is terminated
        this->logs_producer->post_msg(
            "{\"t\": " + std::to_string(std::time(nullptr)) + ", "
             "\"level\": \"INFO\","
             "\"source\": \"collector\","
             "\"message\": \"Cascade is terminated -> {Cascade : " + std::to_string(cascade->get_cid()) + "; End time : " + std::to_string(cascade->get_last_event_time()) + "}\"}"
        );
        // Pop from the priority queue
        cascades.pop();   
    }
}

void tweetoscope::Processor::extract_from_partial_cascade(tweetoscope::timestamp current_tweet_time){
    std::map<tweetoscope::timestamp, std::queue<tweetoscope::refw_cascade>>::iterator it;
    for (it = partial_cascades.begin(); it != partial_cascades.end(); it++){
        bool too_old = true;
        while(!(it->second.empty()) 
                && !(it->second.front().expired()) 
                && current_tweet_time - it->second.front().lock()->get_first_event_time() > it->first){
                
                auto cascade = it->second.front().lock();

                cascade->add_time_window(it->first);

                // Publish in cascade properties
                this->publish_cascade_serie(cascade, it->first);
                
                // Pop from the queue
                it->second.pop();
        }
    }
}

void tweetoscope::Processor::publish_cascade_serie(tweetoscope::ref_cascade ref, tweetoscope::timestamp time_window){
    this->serie_producer->post_msg(ref->partial_cascade_to_json(time_window));

    // Publish in logs -> Cascade is terminated
    this->logs_producer->post_msg(
        "{\"t\": " + std::to_string(std::time(nullptr)) + ", "
         "\"level\": \"DEBUG\","
         "\"source\": \"collector\","
         "\"message\": \"Size sent -> {Cascade : " + std::to_string(ref->get_cid()) + "}\"}"
    );
}

void tweetoscope::Processor::publish_cascade_properties(tweetoscope::ref_cascade ref, tweetoscope::timestamp time_window){
    this->properties_producer->post_msg(std::to_string(time_window), ref->cascade_to_json());

    // Publish in logs -> Cascade serie send
    this->logs_producer->post_msg(
        "{\"t\": " + std::to_string(std::time(nullptr)) + ", "
         "\"level\": \"DEBUG\","
         "\"source\": \"collector\","
         "\"message\": \"Cascade serie sent -> {Time window : " + std::to_string(time_window) + "; Cascade : " + std::to_string(ref->get_cid()) + "}\"}"
    );
}
