include_directories(${CMAKE_CURRENT_SOURCE_DIR})
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${TweetGenerator_SOURCE_DIR}/bin)

# Define the target
add_executable(tweet-generator tweet-generator.cpp)

# Add the include directories for the headers of the boost unit test framework
target_include_directories(tweet-generator PUBLIC .)
target_include_directories(tweet-generator PUBLIC ${GAML_INCLUDE_DIRS})

target_link_libraries(tweet-generator PRIVATE pthread)
target_link_libraries(tweet-generator PRIVATE CppKafka::cppkafka)
target_link_libraries(tweet-generator PRIVATE ${GAML_LIBRARIES})

target_compile_features(tweet-generator PRIVATE cxx_std_17)

# IDEs should put the headers in a nice place
source_group(
  TREE "${PROJECT_SOURCE_DIR}/include"
  PREFIX "Header Files"
  FILES ${HEADER_LIST})


