# demo-pipeline

A simple demonstration ETL pipeline reading data from a google sheet, 
computing a simple transformation and sending result per mail.

## How to use

### Start a kubernetes cluster

We propose using `kind` (you will need to have kind and docker desktop installed):

```
kind create cluster
```

### Install kubernetes extension 

We are using the helm chart of the k-pipe kubernetes extension, which allows running pipelines
natively on kubernetes, available from here: [https://k-pipe.github.io/helm/](https://k-pipe.github.io/helm/)

```
helm repo add k-pipe https://k-pipe.github.io/helm
kubectl create namespace k-pipe
helm install k-pipe k-pipe/operator -n k-pipe
```

### Apply manifest for pipeline definition

You should first adapt some settings in the [pipeline definition manifest](kubernetes/pipeline-definition.yml):
 * in the config of the `read` step, you may put the ID of your own input Google sheet (not required, you may also 
   keep the one that is given there, we have made it publicly readable, but if you want to edit the Google sheet,)
   you should [setup your own](https://workspace.google.com/products/sheets/)
 * change the sender's mail credentials: put server, port and user name that you would like to use for sending mails
   in the configuration of the `write` step.

Then you can apply the manifest:

```
kubectl apply -f kubernetes/pipeline-definition.yml
```

In order to create a Kubernetes secret that contains the sender's password you will have to execute 
this command (replacing XYZ with the actual passowrd, obviously):

```
kubectl create secret generic credentials --from-literal=mailPassword=XYZ
```

### Build docker images

To build the docker images and push them to the nodes of the kind cluster, use 
the [shell script in folder docker](docker/build.sh):

```
cd docker
sh build.sh
```

### Run the pipeline

The input data is found in [this google sheet](https://docs.google.com/spreadsheets/d/1MYBHYEeexCpQ7mOyRGsuSKN3ExpPOn20ylJlj5b0Eng/).
To start a pipeline run you can apply the [pipeline run manifest](kubernetes/pipeline-run.yml):

```
kubectl apply -f kubernetes/pipeline-run.yml
```


### Schedule regular pipeline runs

To run the pipeline automatically in regular intervals, apply the [pipeline schedule manifest](kubernetes/pipeline-schedule.yml):

```
kubectl apply -f kubernetes/pipeline-schedule.yml
```


