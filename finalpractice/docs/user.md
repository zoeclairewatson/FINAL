
## Instructions for using app (how to interact with API)

Once everything has been deployed, you want to first find the IP address of the flask deployment.

To do this you call the command below:
```
kubectl get pods -o wide
```
It should return something like this
```
NAME                                              READY   STATUS        RESTARTS   AGE     IP              NODE                         NOMINATED NODE   READINESS GATES
kz-test-flask-deployment-54956584f6-4565k         1/1     Running       0          37s     10.244.4.53     c02                          <none>           <none>
kz-test-pvc-deployment-5c9c566dc4-gn8lt           1/1     Running       0          23m     10.244.13.235   c11                          <none>           <none>
kz-test-worker-deployment-569b877574-thsxl        1/1     Running       0          20s     10.244.4.54     c02                          <none>           <none>
py-debug-deployment-5cc8cdd65f-gkwnt              1/1     Running       0          24d     10.244.4.206    c02                          <none>           <none>
redis-client-debug-deployment-5f88f47c96-2d66j    1/1     Running       0          14d     10.244.4.230    c02                          <none>           <none>
redis-client-debug-deployment-5f88f47c96-lghcb    1/1     Running       0          14d     10.244.10.130   c009.rodeo.tacc.utexas.edu   <none>           <none>
```
In this example output the IP address would be 10.244.4.53.

Now you are going to want to exec into the python debugger deployment. Here is the general command
```
kubectl exec -it <python-debugger-deployment-name-here> -- /bin/bash
```
For the example output it would be:
```
kubectl exec -it py-debug-deployment-5cc8cdd65f-gkwnt -- /bin/bash
```

Once you are inside the python debugger you are first going to want to install vim. This will be useful for the create route later. Here are the commands:
```
apt-get update
apt-get install vim
```
It will take a minute for vim to be installed.

The next step you will need to do is make sure the flask connection is properly working. You will need to curl and use the default hello world route.
```
curl <flask_IP>:5000/helloWorld
```
For the example output above, the line would be:
```
curl 10.244.4.54:5000/helloWorld
```
It should print out the following:
```
Hello World!!
```
Hit the enter key a few times to fix the indentation.

Next you will need to load in the data from the json file. The raw data set is in a file called animal_center_data_file.json. The load route will load this into the redis database. 
Here is a general example of the command:
```
curl <flask_IP>:5000/load
```
For the example output:
```
curl 10.244.4.54:5000/load
```
It should then print out the following:
```
You have loaded the data set from the json file!
```
Hit the enter key a few times to fix the indentation.

Once you have loaded the json file you are now free to curl any of the CRUD (create, read, update, delete) routes or to give it a job for analysis.

First let's look at the read route. To read an animal you will need its Animal ID. This is a string of an A followed by 6 digits. For example, Fancy's Animal ID is A781976.
Here is the general example of the command:
```
curl <flask_IP>:5000/get_animal?Animal_ID='<animal_id>'
```
Here is the command to get Fancy's information:
```
curl 10.244.4.54:5000/get_animal>?Animal_ID='A781976'
```

