#!/bin/bash

kubectl create secret docker-registry tweetoscope-key \
--docker-server=gitlab-student.centralesupelec.fr:4567 \
--docker-username=deploy_access_token \
--docker-password=WE8WzyvN-LFwKxLjRghm
