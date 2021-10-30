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