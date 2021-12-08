# Tweetoscope
--- 
## Project
The video presentation is available on Youtube with this link <a href="https://youtu.be/lFV9WzjWQNY" title="youtube_presentation">[here]</a>.  
In addition to the README files, a report is available in `./documentation/report.pdf`
### Presentation
The goal of this project is to detect as soon as possible tweets that are likely to become popular, where popularity of a tweet is defined as the number of times this tweet will be retweeted.  
The idea is to design “elastic” microservices, based on Kafka and Kubernetes, that scale properly with an arbitrarily large number of tweets. 
### Architecture
Our solution is divided in small microservices that are connected to each other through Kafka 

<img src="https://pennerath.pages.centralesupelec.fr/tweetoscope/graphviz-images/ead74cb4077631acad74606a761525fe2a3228c1.svg" alt="Project architecture"/>  

```
.  
├── README.md  
├── docker  
│   ├── README.md  
│   ├── clean_builds_bins.sh  
│   ├── dashboard  
│   ├── docker-compose-dashboard.yaml  
│   ├── docker-compose-middleware.yml  
│   ├── docker-compose-services.yml  
│   ├── middleware  
│   └── services  
├── documentation  
│   └── report.pdf  
├── kubernetes  
│   ├── README.md  
│   ├── intercell  
│   └── minikube  
└── src
    ├── README.MD
    ├── dashboard
    │   ├── README.md
    │   ├── config
    │   ├── images
    │   └── src
    ├── hawkes_estimator
    │   ├── hawkes_estimator.py
    │   ├── src
    │   └── test
    ├── learner
    │   ├── estimator.py
    │   └── learner.py
    ├── logger
    │   └── logger.py
    ├── predictor
    │   ├── main.py
    │   ├── src
    │   └── test
    ├── tweet_collector
    │   ├── CMakeLists.txt
    │   ├── app
    │   ├── include
    │   ├── params.config
    │   ├── params_deployment.config
    │   ├── script
    │   ├── src
    │   └── test
    └── tweet_generator
        ├── CMakeLists.txt
        ├── data
        ├── params.config
        ├── params_deployment.config
        ├── script
        └── src  
```

## Getting Started 

### Run the project in terminals 

You can find a documentation to
- build the `tweet-generator` <a href="https://gitlab-student.centralesupelec.fr/2018colombod/tweetoscope_2021_06/-/tree/master/src#build-tweet-generator" title="tweet-generator-build">[here]</a>
- build the `tweet-collector` <a href="https://gitlab-student.centralesupelec.fr/2018colombod/tweetoscope_2021_06/-/tree/master/src#build-tweet-collector" title="tweet-generator-build">[here]</a>
- Run all the microservices in a terminal <a href="https://gitlab-student.centralesupelec.fr/2018colombod/tweetoscope_2021_06/-/tree/master/src#run-the-different-microservices-a-terminal" title="run-microservices">[here]</a>
- Information about the dashboard <a href="https://gitlab-student.centralesupelec.fr/2018colombod/tweetoscope_2021_06/-/tree/22-final-documentation-ameliorations/src/dashboard#dashboard" title="dashboard-info">[here]</a>

### Run the project using docker-compose
Our project is fully deployable with docker-compose.  

You will find <a href="https://gitlab-student.centralesupelec.fr/2018colombod/tweetoscope_2021_06/-/blob/master/docker/README.md#run-the-pipeline-with-docker-compose" title="docker-compose">[here]</a> a detailed documentation to launch the project with docker-compose.

### Run the project using Kubernetes
Our project is fully deployable in Kubernetes.  

You will find <a href="https://gitlab-student.centralesupelec.fr/2018colombod/tweetoscope_2021_06/-/tree/master/kubernetes#on-minikube" title="docker-compose">[here]</a> a detailed documentation to launch the project on Minikube.  

You will find <a href="https://gitlab-student.centralesupelec.fr/2018colombod/tweetoscope_2021_06/-/tree/master/kubernetes#on-intercell" title="docker-compose">[here]</a> a detailed documentation to launch the project on Intercell.


