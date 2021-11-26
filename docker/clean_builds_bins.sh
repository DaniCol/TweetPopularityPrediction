#!/bin/bash

# Clean tweet-collector
if [ -d ../src/tweet_collector/bin ]; then rm -Rf ../src/tweet_collector/bin; fi
if [ -d ../src/tweet_collector/build ]; then rm -Rf ../src/tweet_collector/build; fi
if [ -d ../src/tweet_collector/test/bin ]; then rm -Rf ../src/tweet_collector/test/bin; fi

# Clean tweet-generator
if [ -d ../src/tweet_generator/bin ]; then rm -Rf ../src/tweet_generator/bin; fi
if [ -d ../src/tweet_generator/build ]; then rm -Rf ../src/tweet_generator/build; fi