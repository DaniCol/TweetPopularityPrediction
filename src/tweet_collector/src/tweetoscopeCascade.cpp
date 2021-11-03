#include <iomanip>
#include <iostream>
#include <string>
#include <vector>

#include "../include/tweetoscopeCascade.hpp"
#include "../include/tweetoscopeCollectorParams.hpp"
#include "../include/tweetoscopeTweetReader.hpp"


tweetoscope::Cascade::Cascade(tweetoscope::tweet& tweet)
    : last_event_time(tweet.time),
      tweets({{tweet.time, tweet.magnitude}}),
      cid(tweet.cid),
      msg(tweet.msg),
      n_tots(1),
      alive(true) {}

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

tweetoscope::cascade::idf tweetoscope::Cascade::get_cid() const{
    return this->cid;
}


bool tweetoscope::ref_cascade_comparator::operator()(
    tweetoscope::ref_cascade op1,
    tweetoscope::ref_cascade op2) const {
        return *op1 > *op2;
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
