# Set the output directory
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${TweetCollector_SOURCE_DIR}/test/bin)

# List every unitary test file
file(
	GLOB 
	testfiles
	test*.cpp
)

# For every example
foreach(f ${testfiles})
  # We build the name of the target by removing the extension ".cpp" 
  get_filename_component(testname ${f} NAME_WE) 

  # Actually define the target
  add_executable(${testname} ${f}) 
  
  # All users of this library will need at least C++17
  target_compile_features(${testname} PRIVATE cxx_std_17)

  # Should be linked to our tweet_collector_library
  target_link_libraries(${testname} PRIVATE tweet_collector_library)

endforeach(f)