#!/bin/bash
docker run -it --mount type=bind,source=$(pwd),destination=/home/tweetoscope --net=host tweetoscope

