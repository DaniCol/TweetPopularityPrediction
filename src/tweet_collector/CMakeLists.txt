# Works with 3.11 and tested through 3.21
cmake_minimum_required(VERSION 3.11...3.21)

# Project name and a few useful settings. Other commands can pick up the results
project(
  TweetCollector
  VERSION 0.3
  DESCRIPTION "Tweet collector structure"
  LANGUAGES CXX)

# Only do these if this is the main project, and not if it is included through add_subdirectory
if(CMAKE_PROJECT_NAME STREQUAL PROJECT_NAME)

  # Set up specific C++ flags 
  set(CMAKE_CXX_STANDARD 17)
  set(CMAKE_CXX_STANDARD_REQUIRED True)

  # Let's nicely support folders in IDEs
  set_property(GLOBAL PROPERTY USE_FOLDERS ON)
endif()


# Search for dependencies
find_package(CppKafka REQUIRED)
find_package(Boost REQUIRED)


# Project hierarchy

# The compiled library code is here
add_subdirectory(src)

# The executable code is here
add_subdirectory(app)

# The test codes is here
add_subdirectory(test)