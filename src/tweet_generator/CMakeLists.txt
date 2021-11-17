# Works with 3.11 and tested through 3.21
cmake_minimum_required(VERSION 3.11...3.21)

# Project definition, this sets the variable 
project(
  TweetGenerator
  VERSION 1.0
  DESCRIPTION "Tweet generator structure"
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
find_package(PkgConfig)
pkg_check_modules(GAML REQUIRED gaml)

# Project hierarchy
add_subdirectory(src)
