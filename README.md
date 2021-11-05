# Tweetoscope
--- 
## Getting Started 

### Build the docker image 

To build the docker image, you need first to go to the docker directory 

```
cd <path_to_directory>/docker
```

Then run the following command : 

```
docker build -t tweetoscope . 
```

It will take a while to build the docker. Once the process is over, you can run the docker image with the run_image.bash script. 
It creates a container mounted in the current tweetoscope directory so that you can have access to the main repo while beeing inside a docker container. 

To do so, run the following commands : 

```
cd <path_to_directory> 
sudo chmod +x run_image.bash 
bash run_image.bash
```

### Run the hawkes estimator only (in a docker container)

0. Start docker 

```
cd <path_to_your_repo>
bash run_image.bash
```

1. Start kafka 

```
cd /home/tweetoscope/docker/kafka
./start_kafka.sh
```

2. Create data to publish on the cascade_series topic

Go to the following directory :

```
cd /home/tweetoscope/src/hawkes_estimator/app
python3 publish_fake_data.py --broker-list localhost:9092
```

3. Launch the hawkes_estimator

You need to open another terminal of the same container.
To do so, get the id or name of your running container with 

```
docker ps 
```

Then open a new terminal and run the following commands

```
docker exec -it ID bash 
```

You need to reexport the kafka path, so repeat the 1st step in this terminal. 

Finally, you can run the hawkes_estimator with this command

```
cd /home/tweetoscope/src/hawkes_estimator/app
python3 hawkes_estimator.py --broker-list localhost:9092
```

4. In a 3rd terminal, you can read the cascade_properties topic. Repeat step 3 but launch instead

```
cd /home/tweetoscope/src/kafka_logger/debug_kafka.py
python3 debug_kafka.py --broker-list localhost:9092
```


