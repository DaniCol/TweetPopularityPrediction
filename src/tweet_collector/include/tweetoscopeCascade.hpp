#pragma once
#include <iostream>
#include <vector>
#include <string>
#include <memory>
#include <boost/heap/binomial_heap.hpp>

#include "tweetoscopeCollectorParams.hpp"
#include "tweetoscopeTweetReader.hpp"

namespace tweetoscope{

  class Cascade;

  using ref_cascade = std::shared_ptr<tweetoscope::Cascade>;
  using refw_cascade = std::weak_ptr<tweetoscope::Cascade>;

  // This is the comparison functor for boost queues.
  struct ref_cascade_comparator {
      bool operator()(ref_cascade op1, ref_cascade op2) const; // Defined later.
  };

  // We define our queue type.
  using priority_queue = boost::heap::binomial_heap<ref_cascade,
                        boost::heap::compare<ref_cascade_comparator>>;

  
  using history = std::vector<std::pair<tweetoscope::timestamp, double>>;
  std::ostream& operator<<(std::ostream& os, Cascade const& cascade);

  class Cascade {
    private:
      // Class attributes
      tweetoscope::timestamp      last_event_time;
      tweetoscope::history        tweets;
      tweetoscope::cascade::idf   cid;
      std::string                 msg;
      unsigned int                n_tots;
      bool                        alive;
        
    public:
      priority_queue::handle_type location; // This is "where" the element
                    // is in the queue. This is
                    // needed when we change the
                    // priority

    public:
      // Class constructors
      Cascade(tweetoscope::tweet& tweet);
      Cascade(const Cascade&) = default;

      // Class operators
      inline bool operator<(const Cascade& other) const {
        return this->last_event_time < other.last_event_time;
      }

      inline bool operator>(const Cascade& other) const {
        return this->last_event_time > other.last_event_time;
      }

      // Class methods
      bool is_dead();
      void kill();
      void update_cascade(tweetoscope::tweet& tweet);
      tweetoscope::timestamp get_last_event_time() const; 
      tweetoscope::cascade::idf get_cid() const;
      std::string cascade_to_json() const;
      std::string partial_cascade_to_json(tweetoscope::timestamp time_window) const;

      friend std::ostream& operator<<(std::ostream& os, Cascade const& cascade);
  };

  inline ref_cascade make_cascade(tweetoscope::tweet& tweet){
      return std::make_shared<tweetoscope::Cascade>(tweet);
  }
}
