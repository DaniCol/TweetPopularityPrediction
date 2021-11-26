## Run the pipeline with docker compose 
### Launch Zookeeper and Kafka Broker
- Go to docker directory : `cd <path_to_directory>/docker`
- Run : `docker-compose -f docker-compose-middleware.yml -p middleware up -d`
### Launch dashboard
- Go to docker directory : `cd <path_to_directory>/docker`
- Run : `docker-compose -f docker-compose-dashboard.yaml -p dashboard up -d`
### Launch all micro services
- Go to docker directory : `cd <path_to_directory>/docker`
- Run : `docker-compose -f docker-compose-services.yml -p services up -d`

## Stop the pipeline with docker compose 


### Stop all micro services
- Go to docker directory : `cd <path_to_directory>/docker`
- Run : `docker-compose -f docker-compose-services.yml -p services down`
### Launch dashboard
- Go to docker directory : `cd <path_to_directory>/docker`
- Run : `docker-compose -f docker-compose-dashboard.yaml -p dashboard down`
### Stop Zookeeper and Kafka Broker
- Go to docker directory : `cd <path_to_directory>/docker`
- Run : `docker-compose -f docker-compose-middleware.yml -p middleware down`

## Clean Docker container in the background

```
docker stop $(docker ps -a -q)
docker rm $(docker ps -a -q)
```
