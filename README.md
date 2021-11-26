# Tweetoscope
--- 
## Project
### Presentation
The goal of this project is to detect as soon as possible tweets that are likely to become popular, where popularity of a tweet is defined as the number of times this tweet will be retweeted.  
The idea is to design “elastic” microservices, based on Kafka and Kubernetes, that scale properly with an arbitrarily large number of tweets. 
### Architecture
Our solution is divided in small microservices that are connected to each other through Kafka 

<img src="https://pennerath.pages.centralesupelec.fr/tweetoscope/graphviz-images/ead74cb4077631acad74606a761525fe2a3228c1.svg" alt="Project architecture"/>  

## Getting Started 

### Run the project in terminals 

You can find a documentation to
- build the `tweet-generator` <a href="https://gitlab-student.centralesupelec.fr/2018colombod/tweetoscope_2021_06/-/tree/master/src#build-tweet-generator" title="tweet-generator-build">[here]</a>
- build the `tweet-collector` <a href="https://gitlab-student.centralesupelec.fr/2018colombod/tweetoscope_2021_06/-/tree/master/src#build-tweet-collector" title="tweet-generator-build">[here]</a>
- Run all the microservices in a terminal <a href="https://gitlab-student.centralesupelec.fr/2018colombod/tweetoscope_2021_06/-/tree/master/src#run-the-different-microservices-a-terminal" title="run-microservices">[here]</a>

### Run the project using docker-compose
Our project is fully deployable with docker-compose.  

You will find <a href="https://gitlab-student.centralesupelec.fr/2018colombod/tweetoscope_2021_06/-/blob/master/docker/README.md#run-the-pipeline-with-docker-compose" title="docker-compose">[here]</a> a detailed documentation to launch the project with docker-compose.

### Run the project using Kubernetes
Our project is fully deployable in Kubernetes.  

You will find <a href="https://gitlab-student.centralesupelec.fr/2018colombod/tweetoscope_2021_06/-/tree/master/kubernetes#on-minikube" title="docker-compose">[here]</a> a detailed documentation to launch the project on Minikube.  

You will find <a href="https://gitlab-student.centralesupelec.fr/2018colombod/tweetoscope_2021_06/-/tree/master/kubernetes#on-intercell" title="docker-compose">[here]</a> a detailed documentation to launch the project on Intercell.


