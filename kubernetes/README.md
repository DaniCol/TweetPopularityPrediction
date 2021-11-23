## Deploy the application on a Kubernetes cluster
### On Minikube
- Open a new terminal
  - Go to docker directory : `cd <path_to_directory>/kubernetes/minikube`
  - Launch Minikube : `minikube start`
  - Create a secret to access Gitlab Private Container Registry : `chmod +x build_secret.sh && ./build_secret`
  - Launch Zookeeper and Kafka : `kubectl apply -f zookeeper-and-kafka.yml`
  - Launch Tweetoscope app : `kubectl apply -f tweetoscopeapp.yml`
  - Watch logs for Logger : `kubectl logs <logger_pod_name>` 

When you are done:
- Delete Zookeeper and Kafka : `kubectl delete -f zookeeper-and-kafka.yml`
- Delete Tweetoscope app : `kubectl delete -f tweetoscopeapp.yml`
- Delete Minikube : `minikube delete`

### On Intercell
- Open a first terminal
  - Connect to the frontal server of the Intercell cluster : `ssh cpusdi1_22@phome.metz.supelec.fr`
  - Connect to your assigned node: `ssh ic22`

- Open a second terminal
  - Go to docker directory : `cd <path_to_directory>/kubernetes/intercell`
  - Transfert files to Intercel :
    - `scp build_secret_intercell.sh cpusdi1_22@phome.metz.supelec.fr:/usr/users/cpusdi1/cpusdi1_22`
    - `scp zookeeper-and-kafka-intercell.yml cpusdi1_22@phome.metz.supelec.fr:/usr/users/cpusdi1/cpusdi1_22`
    - `scp tweetoscopeapp-intercell.yml cpusdi1_22@phome.metz.supelec.fr:/usr/users/cpusdi1/cpusdi1_22`

- Go back to the first terminal
  - Create a secret to access Gitlab Private Container Registry : `chmod +x build_secret.sh && ./build_secret`
  - Launch Zookeeper and Kafka : `kubectl -n cpusdi1-22-ns apply -f zookeeper-and-kafka.yml`
  - Launch Tweetoscope app : `kubectl -n cpusdi1-22-ns apply -f tweetoscopeapp.yml`
  - Watch logs for Logger : `kubectl -n cpusdi1-22-ns logs <logger_pod_name>` 

When you are done:
- Delete Zookeeper and Kafka : `kubectl -n cpusdi1-22-ns delete -f zookeeper-and-kafka.yml`
- Delete Tweetoscope app : `kubectl -n cpusdi1-22-ns delete -f tweetoscopeapp.yml`


```
docker stop $(docker ps -a -q)
docker rm $(docker ps -a -q)
```
