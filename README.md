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
