#include "../include/tweetoscopeCollectorParams.hpp"
#include "../include/tweetoscopeConsumer.hpp"
#include "../include/tweetoscopeProducer.hpp"
#include "../include/tweetoscopeCascade.hpp"
#include "../include/tweetoscopeTweetReader.hpp"
#include <string>

int main(int argc, char* argv[]) {

  if(argc != 2) {
    std::cout << "Usage : " << argv[0] << " <config-filename>" << std::endl;
    return 0;
  }
  tweetoscope::params::collector params(argv[1]);

  tweetoscope::Consumer consumer(params);
  consumer.subscribe_topic();
  
  tweetoscope::Producer producer(params, params.topic.out_series);

  std::cout << std::endl
        << "Parameters : " << std::endl
        << "----------"    << std::endl
        << std::endl
        << params << std::endl
        << std::endl;
        
  unsigned int i = 0;
  while(i < 100){
    auto msg = consumer.poll();
    if( msg && ! msg.get_error() ) {
      tweetoscope::tweet twt;
      auto key = tweetoscope::cascade::idf(std::stoi(msg.get_key()));
      auto istr = std::istringstream(std::string(msg.get_payload()));
      istr >> twt;

      tweetoscope::ref_cascade ptr_cascade = tweetoscope::make_cascade(twt);
      std::cout << *ptr_cascade << std::endl;
      i += 1;
      // producer.post_msg(std::to_string(key), std::string(msg.get_payload()));
      // std::cout << key << ": ";
      // std::cout << std::string(msg.get_payload()) << std::endl;
    }
  }
  return 0;
}