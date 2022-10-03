# fastapi-kafka
A sample project for event-driven microservices built with FastAPI and Kafka pub/sub

## Local Development Environment
This project supports `docker-compose` and `kubernetes` with `minikube`

## Docker Compose
### Starting services
All services required to run the project have been dockerized and can be initiated with the generic `docker-compose up`, as seen below:
```shell
$ COMPOSE_DOCKER_CLI_BUILD=1 DOCKER_BUILDKIT=1 docker-compose up -d --build  # Use Docker Buildkit for multi-stage builds
```


## Local Kubernetes with Minikube

### Starting a local cluster
```shell
$ minikube start
😄  minikube v1.27.0 on Ubuntu 20.04
❗  Kubernetes 1.25.0 has a known issue with resolv.conf. minikube is using a workaround that should work for most use cases.
❗  For more information, see: https://github.com/kubernetes/kubernetes/issues/112135
✨  Automatically selected the docker driver
📌  Using Docker driver with root privileges
👍  Starting control plane node minikube in cluster minikube
🚜  Pulling base image ...
🔥  Creating docker container (CPUs=2, Memory=3900MB) ...
🐳  Preparing Kubernetes v1.25.0 on Docker 20.10.17 ...
    ▪ Generating certificates and keys ...
    ▪ Booting up control plane ...
    ▪ Configuring RBAC rules ...
🔎  Verifying Kubernetes components...
    ▪ Using image gcr.io/k8s-minikube/storage-provisioner:v5
🌟  Enabled addons: default-storageclass, storage-provisioner
💡  kubectl not found. If you need it, try: 'minikube kubectl -- get pods -A'
🏄  Done! kubectl is now configured to use "minikube" cluster and "default" namespace by default
$
```

### Starting a dashboard for monitoring
```shell
$ minikube dashboard
🔌  Enabling dashboard ...
    ▪ Using image docker.io/kubernetesui/dashboard:v2.6.0
    ▪ Using image docker.io/kubernetesui/metrics-scraper:v1.0.8
🤔  Verifying dashboard health ...
🚀  Launching proxy ...
🤔  Verifying proxy health ...
🎉  Opening http://127.0.0.1:33625/api/v1/namespaces/kubernetes-dashboard/services/http:kubernetes-dashboard:/proxy/ in your default browser...
```

### Building the producer image
```shell
$ docker build --target dev -t producer-app:1.0.0 -f ./producer/Dockerfile .
[+] Building 5.3s (12/12) FINISHED                                                                                                                                         
 => [internal] load build definition from Dockerfile                                                                                                                  1.0s
 => => transferring dockerfile: 38B                                                                                                                                   0.1s
 => [internal] load .dockerignore                                                                                                                                     0.7s
 => => transferring context: 2B                                                                                                                                       0.1s
 => [internal] load metadata for docker.io/library/python:3.8                                                                                                         0.2s
 => [base 1/6] FROM docker.io/library/python:3.8                                                                                                                      0.0s
 => [internal] load build context                                                                                                                                     2.7s
 => => transferring context: 164.75kB                                                                                                                                 1.9s
 => CACHED [base 2/6] RUN addgroup --system appuser     && adduser --system --ingroup appuser appuser                                                                 0.0s
 => CACHED [base 3/6] RUN apt-get update && apt-get install -y -q --no-install-recommends   build-essential   && apt-get purge -y --auto-remove -o APT::AutoRemove::  0.0s
 => CACHED [base 4/6] WORKDIR /home/appuser/code/                                                                                                                     0.0s
 => CACHED [base 5/6] COPY --chown=appuser:appuser ./producer/requirements.txt requirements.txt                                                                       0.0s
 => CACHED [base 6/6] RUN pip install --no-cache-dir -r requirements.txt                                                                                              0.0s
 => CACHED [dev 1/1] COPY --chown=appuser:appuser ./producer/* /home/appuser/code/                                                                                    0.0s
 => exporting to image                                                                                                                                                1.0s
 => => exporting layers                                                                                                                                               0.0s
 => => writing image sha256:3aefc9f9b77c73fe1abd9b4e947837b6a1912c484cf758af4cf03099022d3509                                                                          0.1s
 => => naming to docker.io/library/producer-app:1.0.0
$                      
```

### Pushing the producer image into a local registry
```shell
$ minikube image load producer-app:1.0.0
$
```

### Starting services inside the cluster
```shell
$  minikube kubectl -- apply -R -f ./k8s/ 
replicaset.apps/producer-app-rs created
ingress.networking.k8s.io/fastapi-producer-ingress created
service/fastapi-producer-service created
$
```