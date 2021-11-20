#include <iomanip>
#include <iostream>
#include <string>
#include <vector>

#include "../include/tweetoscopeCascade.hpp"
#include "../include/tweetoscopeCollectorParams.hpp"
#include "../include/tweetoscopeTweetReader.hpp"


tweetoscope::Cascade::Cascade(tweetoscope::tweet& tweet)
    : last_event_time(tweet.time),
      first_event_time(tweet.time),
      tweets({{tweet.time, tweet.magnitude}}),
      cid(tweet.cid),
      msg(tweet.msg),
      n_tots(1),
      alive(true),
      windows() {}

bool tweetoscope::Cascade::is_dead() {
    return !this->alive;
}

void tweetoscope::Cascade::kill() {
    this->alive = false;
}

void tweetoscope::Cascade::update_cascade(tweetoscope::tweet& tweet) {
    // increse by 1 the size of the cascade
    this->n_tots += 1;

    // update the tweets vector
    this->tweets.push_back({tweet.time, tweet.magnitude});

    // update the last_event_time
    this->last_event_time = tweet.time;
}

tweetoscope::timestamp tweetoscope::Cascade::get_last_event_time() const{
    return this->last_event_time;
};

tweetoscope::timestamp tweetoscope::Cascade::get_first_event_time() const{
    return this->first_event_time;
};

tweetoscope::cascade::idf tweetoscope::Cascade::get_cid() const{
    return this->cid;
}


std::string tweetoscope::Cascade::cascade_to_json() const{
    return "{\"type\": \"size\", " 
            "\"cid\": " + std::to_string(this->cid) + ", " 
            "\"n_tot\": " + std::to_string(this->n_tots) + ", "
            "\"t_end\": " + std::to_string(this->last_event_time) + "}";
}


std::string tweetoscope::Cascade::partial_cascade_to_json(tweetoscope::timestamp time_window) const{
    // Generate the tweets array 
    // ex : 
    //      tweets = [(1, 1000), (23, 63), (45, 79), ...]
    std::string tweets = "[";
    for(auto& t: this->tweets){
        tweets += "[" + std::to_string(t.first) + "," + std::to_string(t.second) + "],";
    }
    // Remove the last ","
    if(!(this->tweets.empty())) tweets.pop_back();

    // Close the array
    tweets += "]";

    // Return the msg as a Json
    return "{\"type\": \"serie\", "
            "\"cid\": " + std::to_string(this->cid) + ", "
            "\"msg\": \"Empty msg\", "
            "\"T_obs\" :" + std::to_string(time_window) + ", "
            "\"tweets\": " + tweets + "}";
}


bool tweetoscope::ref_cascade_comparator::operator()(
    tweetoscope::ref_cascade op1,
    tweetoscope::ref_cascade op2) const {
        return *op1 > *op2;
}

void tweetoscope::Cascade::add_time_window(tweetoscope::timestamp time_window){
    this->windows.push_back(time_window);
}

std::vector<tweetoscope::timestamp> tweetoscope::Cascade::get_windows() const{
    return this->windows;
} 

std::ostream& tweetoscope::operator<<(std::ostream& os, tweetoscope::Cascade const& cascade) {
    std::cout.precision(0);
    os << "id : " << std::to_string(cascade.cid) << std::endl;
    os << "msg : " << cascade.msg << std::endl;
    for(auto& t : cascade.tweets){
        os << std::left  << std::fixed << std::setw(6) << t.first
           << " | "
           << std::right  << std::fixed << std::setw(9) << t.second
           << std::endl;
    } 
    os << std::endl;
    return os;
}
