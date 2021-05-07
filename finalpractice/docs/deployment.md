
# Instructions for deploying app (how an operator should deploy system on a k8s cluster)

## Deploying Flask API Test Environment to Kubernetes

########### info for cloning repo

```bash
git clone blahblahblah
cd deploy/test/redis
```

Create a Persistent Volume Claim for Redis data:

```bash
kubectl apply -f test-redis-pvc.yml
```

Create a Deployment for the Redis database:

```bash
kubectl apply -f test-redis-deployment.yml
```

Create a Service for the Redis database:

```bash
kubectl apply -f test-redis-service.yml
```

Now that the Redis Service has been created, there are manual changes that need to be executed within the api and worker deployments to update the Redis Service IP. First, check the Redis service Cluster-IP using:

```bash
kubectl get services -- selector "username=kz"
```

Change to api directory and update the flask deployment yml file to use this Redis service IP:

```bash
cd ../api
vim test-flask-deployment.yml
```

Manually replace the value of the environment variable named REDIS_IP:

```bash
env:

  ...

- name: REDIS_IP
  value: "<enter Redis Service IP here>"
```

Create a Deployment for the flask API:

```bash
kubectl apply -f test-flask-deployment.yml
```

Create a service for the flask API:

```bash
kubectl apply -f test-flask-service.yml
```

Redirect to the worker directory and update the worker deployment yml file to use this same Redis service IP:

```bash
cd ../worker
vim test-worker-deployment.yml
```

Manually replace the value of the environment variable named REDIS_IP in the same way:

```bash
env:

  ...

- name: REDIS_IP
  value: "<enter Redis Service IP here>"
```

Create a Deployment for the worker:

```bash
kubectl apply -f test-worker-deployment.yml
```


