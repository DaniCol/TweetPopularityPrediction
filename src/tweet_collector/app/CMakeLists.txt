# Set the output directory
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${TweetCollector_SOURCE_DIR}/bin)

# Define the target
add_executable(tweet-collector tweetoscopeCollector.cpp)

# This depends on our tweet_collector_library
target_link_libraries(tweet-collector PRIVATE tweet_collector_library)

# All users of this library will need at least C++17
target_compile_features(tweet-collector PRIVATE cxx_std_17)
