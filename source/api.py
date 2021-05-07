import json
from flask import Flask, request, send_file
from hotqueue import HotQueue
import redis
import jobs
from jobs import rd, rd1, q
import os
import uuid
import datetime

app = Flask(__name__)

@app.route('/helloWorld',methods=['GET'])
def hello_world():
    return "Hello World!"

@app.route('/load',methods=['GET'])
def load():
    load_data()
    return "You have loaded the data set from the json file!"
    #return str(rd1.hgetall(1))
def load_data():
    with open("/app/animal_center_data_file.json","r") as json_file:
        animal_data = json.load(json_file)
 
    i = 0
    for animal in animal_data:
        animal_id = animal['Animal ID']
        name = animal['Name']
        date_of_entry = animal['DateTime'] 
        date_of_birth = animal['Date of Birth'] 
        outcome_type = animal['Outcome Type']
        outcome_subtype = animal['Outcome Subtype']
        animal_type = animal["Animal Type"]
        sex = animal['Sex upon Outcome']
        age = animal['Age upon Outcome']
        breed = animal['Breed']
        color = animal['Color']
        
        rd1.hmset(i,{'Animal_ID': animal_id,'Name':name,'Date_of_Entry':date_of_entry,'Date_of_Birth': date_of_birth, 'Outcome_Type': outcome_type,'Outcome_Subtype': outcome_subtype,'Animal_Type': animal_type, 'Sex':sex, 'Age':age, 'Breed': breed, 'Color':color})
        i = i+1
        

def get_data():
    animal_data = []
   
    for i in range(rd1.dbsize()-1):
        animal = {}
        animal['Animal_ID'] = str(rd1.hget(i,'Animal_ID'))[1:]
        animal['Name'] = str(rd1.hget(i,'Name'))[1:]
        animal['Date_of_Entry'] = str(rd1.hget(i,'Date_of_Entry'))[1:] 
        animal['Date_of_Birth'] = str(rd1.hget(i,'Date_of_Birth'))[1:] 
        animal['Outcome_Type'] = str(rd1.hget(i,'Outcome_Type'))[1:]
        animal['Outcome_Subtype'] = str(rd1.hget(i,'Outcome_Subtype'))[1:]
        animal['Animal_Type'] = str(rd1.hget(i,'Animal_Type'))[1:]
        animal['Sex'] = str(rd1.hget(i,'Sex'))[1:]
        animal['Age'] = str(rd1.hget(i,'Age'))[1:]
        animal['Breed'] = str(rd1.hget(i,'Breed'))[1:]
        animal['Color'] = str(rd1.hget(i,'Color'))[1:]
        
        animal_data.append(animal) 
    
    return animal_data

# READ route
@app.route('/get_animal',methods=['GET'])
def get_id_animal():
    animalid = str(request.args.get('Animal_ID'))
    test = get_data()
    return json.dumps([x for x in test if x['Animal_ID'] == "'"+animalid+"'"])

# CREATE route
@app.route('/add_animal', methods=['GET', 'POST'])
def add_animal():
    if request.method == 'POST':
        animal_dict = request.get_json(force=True)
        rd1.hset( rd1.dbsize(), animal_dict )
        return "Added new animal with ID = "+animal_dict['Animal_ID']

    else:
        return """

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

"""
   
# UPDATE route
@app.route('/update_animal', methods=['GET', 'POST'])
def update_animal():
    if request.method == 'POST':
        #get Animal_ID, the only required query parameter
        animalid = str(request.args.get('Animal_ID'))
        #raise exception if user does not provide Animal_ID
        if not animalid:
            raise Exception('Animal_ID must be one of the query parameters')
        #iterate over all keys in raw data db
        for key in rd1.keys():
            #return "checking for animal id match"
            #find animal that matches the Animal_ID parameter
            if str(rd1.hget(key, 'Animal_ID'))[1:] == "'"+animalid+"'":
                #return "found animal match"                
                #iterate over all field:value pairs passed in the query string
                for field, value in request.args.items():
                    
                    #skip the Animal_ID field
                    if field == 'Animal_ID':
                        pass
                    #update the database for any other field that is passed in the query 
                    else:
                        rd1.hset(key, field, value)
                return "You have edited animal "+animalid
        else:
            return "cannot find animal"

    else:
        return """

    Try a curl command like:

    curl -X POST "localhost:5000/update_animal?Animal_ID='A643424'&Animal_Type='Dog'"


"""

# DELETE route
@app.route('/delete_animal', methods=['GET', 'DELETE'])
def delete_animal():
    if request.method == 'DELETE':
        animalid = request.args.get('Animal_ID')
        test = get_data()
        animal = [x for x in test if x['Animal_ID'] == "'"+animalid+"'"]
        rd1.delete(test.index(animal[0]))
        return "You have deleted animal "+animalid

    else:
        return """

    Try a curl command like:

    curl -X DELETE localhost:5000/delete_animal?Animal_ID='A643424'

"""


@app.route('/jobs', methods=['GET', 'POST'])
def jobs_api():
    if request.method == 'POST':
        try:
            job = request.get_json(force=True)
        except Exception as e:
            return True, json.dumps({'status': "Error", 'message': 'Invalid JSON: {}.'.format(e)})
        return json.dumps(jobs.add_job(job['job_type'],job['start'], job['end']))

    else:
        return """

    Try a curl command like:

    curl -X POST -H "content-type: application/json" -d '{"job_type": "dates", "start": "6/17/2019", "end": "6/17/2020"}' localhost:5000/jobs

"""

@app.route('/download/<jobid>', methods=['GET'])
def download(jobid):
    path = f'/app/{jobid}.png'
    with open(path, 'wb') as f:
        f.write(rd.hget(jobid, 'result'))
    return send_file(path, mimetype='image/png', as_attachment=True)

#curl localhost:5000/download/<jobid> >outcome.png

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
