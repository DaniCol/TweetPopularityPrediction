## Deploy the application on a Kubernetes cluster
### On Minikube
- Open a new terminal
  - Go to docker directory : `cd <path_to_directory>/kubernetes/minikube`
  - Launch Minikube : `minikube start`
  - Create a secret to access Gitlab Private Container Registry : `chmod +x build_secret.sh && ./build_secret.sh`
  - Launch Zookeeper and Kafka : `kubectl apply -f zookeeper-and-kafka.yml`
  - Launch Dashboard : `kubectl apply -f dashboard.yml`
  - Launch Tweetoscope app : `kubectl apply -f tweetoscopeapp.yml`

When grafana pod is running (`kubectl get pods`):
- Post forwart port 3000 to access grafana dashboard in your machine: `kubectl port-forward deployment/grafana 3000:3000`
- You can now access to grafana dashboard on your web browser by visiting http://localhost:3000
  
If you want to watch logs collected by Logger : `kubectl logs <logger_pod_name>` 

When you are done:
- Delete Tweetoscope app : `kubectl delete -f tweetoscopeapp.yml`
- Delete Dashboard : `kubectl delete -f dashboard.yml`
- Delete Zookeeper and Kafka : `kubectl delete -f zookeeper-and-kafka.yml`
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
    - `scp dashboard-intercell.yml cpusdi1_22@phome.metz.supelec.fr:/usr/users/cpusdi1/cpusdi1_22`
    - `scp tweetoscopeapp-intercell.yml cpusdi1_22@phome.metz.supelec.fr:/usr/users/cpusdi1/cpusdi1_22`

- Go back to the first terminal
  - Create a secret to access Gitlab Private Container Registry : `chmod +x build_secret_intercell.sh && ./build_secret_intercell.sh`
  - Launch Zookeeper and Kafka : `kubectl -n cpusdi1-22-ns apply -f zookeeper-and-kafka-intercell.yml`
  - Launch Dashboard : `kubectl -n cpusdi1-22-ns apply -f dashboard-intercell.yml`
  - Launch Tweetoscope app : `kubectl -n cpusdi1-22-ns apply -f tweetoscopeapp-intercell.yml`
  - Watch logs for Logger : `kubectl -n cpusdi1-22-ns logs <logger_pod_name>` 

When you are done:
- Delete Tweetoscope app : `kubectl -n cpusdi1-22-ns delete -f tweetoscopeapp-intercell.yml`
- Delete Dashboard : `kubectl -n cpusdi1-22-ns delete -f dashboard-intercell.yml`
- Delete Zookeeper and Kafka : `kubectl -n cpusdi1-22-ns delete -f zookeeper-and-kafka-intercell.yml`
