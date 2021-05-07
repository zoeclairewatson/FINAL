
## Instructions for using app (how to interact with API)

Once everything has been deployed, you want to first find the IP address of the flask deployment.

To do this you call the command below:
```bash
kubectl get pods --selector "app=kz-flask" -o wide

```
It should look something like this for the output:
```bash
NAME                                        READY   STATUS    RESTARTS   AGE   IP             NODE                         NOMINATED NODE   READINESS GATES
kz-prod-flask-deployment-5ff8f4df6b-g5mkp   1/1     Running   0          19m   10.244.10.83   c009.rodeo.tacc.utexas.edu   <none>           <none>
```
In this example output the IP address would be 10.244.10.83.

Next you need the name of the python debugger deployment. Here is the command:
```bash
kubectl get pods --selector "app=py-app"
```
Here is some example output:
```bash
NAME                                   READY   STATUS    RESTARTS   AGE
py-debug-deployment-5cc8cdd65f-c22z8   1/1     Running   0          35d
```

Now you are going to want to exec into the python debugger deployment. Here is the general command
```bash
kubectl exec -it <python-debugger-deployment-name-here> -- /bin/bash
```
For the example output it would be:
```bash
kubectl exec -it py-debug-deployment-5cc8cdd65f-c22z8 -- /bin/bash
```

Once you are inside the python debugger you are first going to want to install vim. This will be useful for the create route later. Here are the commands:
```bash
apt-get update
apt-get install vim
```
It will take a minute for vim to be installed.

The next step you will need to do is make sure the flask connection is properly working. You will need to curl and use the default hello world route.
```bash
curl <flask_IP>:5000/helloWorld
```
For the example output above, the line would be:
```bash
curl 10.244.10.83:5000/helloWorld
```
It should print out the following:
```bash
Hello World!!
```
Hit the enter key a few times to fix the indentation.

Next you will need to load in the data from the json file. The raw data set is in a file called animal_center_data_file.json. The load route will load this into the redis database. 
Here is a general example of the command:
```bash
curl <flask_IP>:5000/load
```
For the example output:
```bash
curl 10.244.10.83:5000/load
You have loaded the data set from the json file
```
Hit the enter key a few times to fix the indentation.

Once you have loaded the json file you are now free to curl any of the CRUD (create, read, update, delete) routes or to give it a job for analysis.

First let's look at the read route. To read an animal you will need its Animal ID. This is a string of an A followed by 6 digits. For example, Chunk's Animal ID is A794011.
Here is the general example of the command:
```bash
curl <flask_IP>:5000/get_animal?Animal_ID='<animal_id>'
```
Here is an example of output you get using this route:
```bash
curl 10.244.10.83:5000/get_animal?Animal_ID='A794011'
[{"Animal_ID": "'A794011'", "Name": "'Chunk'", "Date_of_Entry": "'5-8-2019 18:20'", "Date_of_Birth": "'5-2-2017'", "Outcome_Type": "'Rto-Adopt'", "Outcome_Subtype": "''", "Animal_Type": "'Cat'", "Sex": "'Neutered Male'", "Age": "'2 years'", "Breed": "'Domestic Shorthair Mix'", "Color": "'Brown Tabby-White'"}]
```

Next let's look at the create route. To create an animal you will need to create a json file. First to get the format of this json file correct, curl this route:
```bash
curl <flask_IP>:5000/add_animal
```
Here is an example:
```bash
root@py-debug-deployment-5cc8cdd65f-c22z8:/# curl 10.244.10.83:5000/add_animal
    Assemble and post a json structure like this:
    curl -X POST -H "Content-type: application/json" -d @file.json host-ip:5000/add_animal
    Where 'file.json' is a file containing:
{
  "Animal_ID": "A781976",
  "Name": "Fancy",
  "DateTime": "10/16/2018 14:25",
  "Date_of_Birth": "10/8/2017",
  "Outcome_Type": "Transfer",
  "Outcome_Subtype": "Partner",
  "Animal_Type": "Dog",
  "Sex_upon_Outcome": "Intact Female",
  "Age_upon_Outcome": "1 year",
  "Breed": "German Shepherd Mix",
  "Color": "White"
}
```
To create this file do vim file.json and hit the i key and copy paste the template in and change the appropriate variables. Here is an example of a file.json:
```bash
root@py-debug-deployment-5cc8cdd65f-c22z8:/# vim file.json
root@py-debug-deployment-5cc8cdd65f-c22z8:/# cat file.json
{
        "Animal_ID": "A781976",
        "Name": "Fancy",
        "Date_of_Entry": "10-16-2018 12:25",
        "Date_of_Birth": "10-8-2017",
        "Outcome_Type": "Transfer",
        "Outcome_Subtype": "Partner",
        "Animal_Type": "Dog",
        "Sex": "Intact Female",
        "Age": "1 year",
        "Breed": "German Shepherd Mix",
        "Color": "White"
}
```
Once your json file is created and everything looks good, you can then use the post method for the add animal route. 
Here is the general example route:
```bash
curl -X POST -H  "Content-type: application/json" -d @file.json <flask_IP>:5000/add_animal
```
Here is the example route with output:
```bash
root@py-debug-deployment-5cc8cdd65f-c22z8:/# curl -X POST -H  "Content-type: application/json" -d @file.json 10.244.10.88:5000/add_animal
Added new animal with ID = A781976
```

Next let's go over how to update an animal. You must give an Animal ID parameter but you can choose as many other fields as you would like to edit your animal.
There is a get method route for update animal route to tell you how to use it.
Here is a general example route:
```bash
curl 10.244.10.88:5000/update_animal
```
Here is an example route with output:
```bash
root@py-debug-deployment-5cc8cdd65f-c22z8:/# curl 10.244.10.88:5000/update_animal
    Try a curl command like:
    curl -X POST "localhost:5000/update_animal?Animal_ID=A643424&Animal_Type=Dog"
```
So to actually update the animal you use the post method as outlined in the output.
Here is a general example route:
```bash
curl -X POST "<flask_IP>:5000/update_animal?Animal_ID=<animal_id>&Animal_Type=<animal_type>"
```
Here is an example route with output:
```bash
root@py-debug-deployment-5cc8cdd65f-c22z8:/# curl -X POST "10.244.10.88:5000/update_animal?Animal_ID=A643424&Animal_Type=Dog"
You have edited animal A643424
```
You can check if the animal is updated using the get animal function. Here is an example:
```bash
root@py-debug-deployment-5cc8cdd65f-c22z8:/# curl 10.244.10.88:5000/get_animal?Animal_ID=A643424
[{"Animal_ID": "'A643424'", "Name": "'Patches'", "Date_of_Entry": "'10-30-2015 17:23'", "Date_of_Birth": "'12-9-2009'", "Outcome_Type": "'Return to Owner'", "Outcome_Subtype": "''", "Animal_Type": "'Dog'", "Sex": "'Neutered Male'", "Age": "'5 years'", "Breed": "'Domestic Shorthair Mix'", "Color": "'Black-White'"}]
```

You can edit more than 1 field, so here is a general example editing every field of an animal:
```bash
curl -X POST "<flask_IP>:5000/update_animal?Animal_ID=<animal_id>&Name=<name>&Date_of_Entry=<date_of_entry *make sure to include hour minute>&Date_of_Birth=
<date_of_birth>&Outcome_Type=<outcome_type>&Outcome_Subtype=<animal_subtype>&Animal_Type=<animal_type>&Sex=<sex>&Age=<age>&Breed=<breed>
```
***DO NOT MAKE YOUR ANIMAL TYPE ANYTHING OTHER THAN CAT,DOG,BIRD,LIVESTOCK,OTHER IT WILL MESS UP THE ANALYSIS IF YOU DO***
Here is an example with output:
```bash
root@py-debug-deployment-5cc8cdd65f-c22z8:/# curl -X POST "10.244.10.88:5000/update_animal?Animal_ID=A643424&Name=Boomer&Date_of_Entry=5-5-2021&Date_of_Birth=5-5-2020&Outcome_Type=IDK&Outcome_Subtype=WOW&Animal_Type=Other&Sex=Female&Age=old&Breed=Whale&Color=Blue"
You have edited animal A643424
```
Here is an example with output checking to see that it is updated:
```bash
root@py-debug-deployment-5cc8cdd65f-c22z8:/# curl 10.244.10.88:5000/get_animal?Animal_ID=A643424[{"Animal_ID": "'A643424'", "Name": "'Boomer'", "Date_of_Entry": "'5-5-2021'", "Date_of_Birth": "'5-5-2020'", "Outcome_Type": "'IDK'", "Outcome_Subtype": "'WOW'", "Animal_Type": "'Other'", "Sex": "'Female'", "Age": "'old'", "Breed": "'Whale'", "Color": "'Blue'"}]
```

Next let's look at how to delete an animal. To delete an animal provide the Animal ID. There is a get method route that can give you the format of the curl.
Here is a general example route:
```bash
curl <flask_IP>:5000/delete_animal
```
Here is an example with output:
```bash
root@py-debug-deployment-5cc8cdd65f-c22z8:/# curl 10.244.10.88:5000/delete_animal
    Try a curl command like:
    curl -X DELETE localhost:5000/delete_animal?Animal_ID=A643424
```
Here is the general example route to actually delete the animal:
```bash
curl -X DELETE <flask_IP>:5000/delete_animal?Animal_ID=<animal_id>
```
Here is an example of that with output:
```
root@py-debug-deployment-5cc8cdd65f-c22z8:/# curl -X DELETE 10.244.10.88:5000/delete_animal?Animal_ID=A643424
You have deleted animal A643424
```

Lastly, let us look at how to do jobs. There is a get method route that can give you the format of the curl.
Here is the general example route:
```bash
curl <flask_IP>:5000/jobs
```
Here is the example of the get route with output:
```bash
root@py-debug-deployment-5cc8cdd65f-c22z8:/# curl 10.244.10.88:5000/jobs
    Try a curl command like:
    curl -X POST -H "content-type: application/json" -d '{"job_type": "dates", "start": "6/17/2019", "end": "6/17/2020"}' localhost:5000/jobs
```
Now to actually send a job. There are 2 job types, or 2 types of analysis. animal_type and dates. animal_type gives a bar graph showing the number of each type of animal in the entire dataset. dates gives you 
