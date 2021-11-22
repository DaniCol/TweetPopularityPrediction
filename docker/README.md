## Run the pipeline with docker compose 
### Launch Zookeeper and Kafka Broker
- Open a new terminal
  - Go to logger directory : `cd <path_to_directory>/docker`
  - Run : `docker-compose -f docker-compose-middleware.yml -p middleware up`

### Launch all micro services
- Open a new terminal
  - Go to logger directory : `cd <path_to_directory>/docker`
  - Run : `docker-compose -f docker-compose-services.yml up`

## Stop the pipeline with docker compose 


### Stop all micro services
- Open a new terminal
  - Go to logger directory : `cd <path_to_directory>/docker`
  - Run : `docker-compose -f docker-compose-services.yml down`

### Stop Zookeeper and Kafka Broker
- Open a new terminal
  - Go to logger directory : `cd <path_to_directory>/docker`
  - Run : `docker-compose -f docker-compose-middleware.yml -p middleware down`

## Clean Docker container in the background

```
docker stop $(docker ps -a -q)
docker rm $(docker ps -a -q)
```
