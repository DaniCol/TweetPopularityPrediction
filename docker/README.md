## Run the pipeline without docker compose

To build each docker image : 

```
docker build -t hawkes -f Dockerfile.Hawkes ..
docker build -t learner -f Dockerfile.Learner ..
docker build -t broker -f Dockerfile.KafkaBroker ..
docker build -t logger -f Dockerfile.Logger ..
docker build -t predictor -f Dockerfile.Predictor ..
docker build -t topics -f Dockerfile.Topics ..
docker build -t tweetcollector -f Dockerfile.TweetCollector ..
docker build -t tweetgenerator -f Dockerfile.TweetGenerator ..
```

To run each docker image :

```
launch_zookeeper.sh
docker run --rm -it --network host hawkes
docker run --rm -it --network host learner
docker run --rm -it -e lvl='DEBUG' -e src='collector' -e topic='cascade_series' --network host logger 
```

EtC. etc. 

## Run te pipeline with docker compose 

```
docker-compose -f docker-compose-middleware.yml up
docker-compose -f docker-compose-services.yml up
```
Bien penser à lancer middleware en premier et services en 2eme. 
Avant de relancer middleware, clean docker containers.  

## CLEAN DOCKER CONTAINERS IN THE BACKGROUND 

```
docker stop $(docker ps -a -q)
docker rm $(docker ps -a -q)
```

## Commentaires 

L'image topics creations est sûrement inutile.
L'image Logger sert juste à débugger, pas besoin de la lancer pr tester la pipeline. 
Pb au niveau de l'image HawkesProcessor. Error sur le script python dans le consumer. 
