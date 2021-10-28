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