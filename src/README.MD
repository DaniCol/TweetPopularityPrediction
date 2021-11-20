# Tweetoscope
--- 
## Build the different pre-processing algorithms

### Build tweet-generator 

To build the tweet-generator, you need first to go to tweet_generator directory 

```
cd <path_to_directory>/tweet_generator
```

Then run the following command: 

```
chmod +x ./script/build.sh
./script/build.sh 
```

This script will run the different commands to build the tweet-generator executable.  
The output file will be find in the `bin` folder.

To run the tweet-generator, use the following commands:

```
cd <path_to_directory>/tweet-generator 
./bin/tweet-generator params.config
```

If you want to delete all the files created by the make command, use the following commands:

```
chmod +x ./script/clean.sh
./script/clean.sh 
```

### Build tweet-collector 

To build the tweet-collector, you need first to go to tweet_collector directory 

```
cd <path_to_directory>/tweet_collector
```

Then run the following command: 

```
chmod +x ./script/build.sh
./script/build.sh 
```

This script will run the different commands to build the tweet-collector executable.  
The output file will be find in the `bin` folder.  
It also builds all the test executables. The output files will be find in the `test/bin` folder. 

To run the tweet-collector, use the following commands:

```
cd <path_to_directory>/tweet-generator 
./bin/tweet-collector params.config
```

If you want to delete all the files created by the make command, use the following commands:

```
chmod +x ./script/clean.sh
./script/clean.sh 
```

## Run the different microservices a terminal
Procedure to launch all microservices in a terminal

### Zookeeper instance and Kafka Broker
You have two possibilities:

- Use the script provided by the teacher
  - `export KAFKA_PATH=/path/to/kafka`
  - `./kafka.sh start --zooconfig zookeeper.properties --serverconfig server.properties `
  - To stop kafka use : `./kafka.sh stop`
- Use the command line
  - `export KAFKA_PATH=/path/to/kafka`
  - In a first terminal : `$KAFKA_PATH/bin/zookeeper-server-start.sh $KAFKA_PATH/config/zookeeper.properties`
  - In a second terminal : `$KAFKA_HOME/bin/kafka-server-start.sh $KAFKA_HOME/config/server.properties`
### Logger
- Open a new terminal
  - Go to logger directory : `cd <path_to_directory>/logger`
  - Run : `python logger.py --broker-list localhost:9092 --logs_topic logs`

You can also specify the level of the logger and the source. By default they are set to all.  
- Levels : 
  - DEBUG
  - INFO
  - WARNING
  - ERROR
  - CRITICAL
- Sources : 
  - "collector"
  - "hawkes_estimator"
  - "predictor"
  - "learner"
### Learner
- Open a new terminal
  - Go to logger directory : `cd <path_to_directory>/learner`
  - Run : `python learner.py --broker-list localhost:9092`
### Predictor
- Open a new terminal
  - Go to logger directory : `cd <path_to_directory>/predictor`
  - Run : `python main.py --broker-list localhost:9092`
### Hawkes Estimator
- Open a new terminal
  - Go to logger directory : `cd <path_to_directory>/hawkes_estimator`
  - Run : `python heawkes_estimator.py --broker-list localhost:9092`
### Tweet Collector
- Open a new terminal
  - Go to logger directory : `cd <path_to_directory>/tweet_collector`
  - Run : `./bin/tweet-collector params.config`
### Tweet Generator
- Open a new terminal
  - Go to logger directory : `cd <path_to_directory>/tweet_generator`
  - Run : `./bin/tweet-generator params.config`