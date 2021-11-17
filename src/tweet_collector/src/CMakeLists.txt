file(GLOB_RECURSE SRC_FILES ${TweetCollector_SOURCE_DIR}/src/*.cpp)
file(GLOB_RECURSE HEADER_FILES ${TweetCollector_SOURCE_DIR}/include/*.hpp)

# Make an automatic library - will be static or dynamic based on user setting
add_library(tweet_collector_library ${SRC_FILES} ${HEADER_FILES})

# We need this directory, and users of our library will need it too
target_include_directories(tweet_collector_library PUBLIC ../)

# This depends on boost and cppkafka
target_link_libraries(tweet_collector_library PRIVATE Boost::boost)
target_link_libraries(tweet_collector_library PRIVATE CppKafka::cppkafka)

# All users of this library will need at least C++17
target_compile_features(tweet_collector_library PUBLIC cxx_std_17)

# IDEs should put the headers in a nice place
source_group(
  TREE "${PROJECT_SOURCE_DIR}/include"
  PREFIX "Header Files"
  FILES ${HEADER_LIST})
