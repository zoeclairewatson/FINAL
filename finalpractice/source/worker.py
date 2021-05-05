import jobs
from jobs import q, rd1, rd
import time
import redis
import matplotlib.pyplot as plt

@q.worker
def execute_job(jid):
    
    data = jobs.get_job_data(jid)

    job_type = jobs.get_job_type(jid)

    jobs.update_job_status(jid, 'in progress')
   
 
    #analysis: plot total number of outcomes for each day in date range

    #first job type: dates
    if (job_type == 'dates'):

        #format of how dates come in??????????? should be a string
        start = data['start']
        end = data['end']

        #set inital outcomes count
        animal_outcomes_of_day = 0

        #x values: list of dates
        x_values_to_plot = []

        #y values: list of integer numbers of outcomes per date
        y_values_to_plot = []

        start = datetime.datetime.strptime( start, '%m/%d/%Y')
        end = datetime.datetime.strptime( end, '%m/%d/%Y')

        #format to check for full day, rather than specific time??????????
        for key in rd1.keys():

            key_time_temp = key['Date_of_Entry'].decode(utf-8).replace("'","")
            key_time = datetime.datetime.strptime(key_time_temp, '%m/%d/%Y %H:%M')

            #check for keys in date range
            if (start <= key_time <= end):

                #set specific date
                x = key['Date_of_Entry']

                #check if date is alread in x_values_to_plot
                if x not in x_values_to_plot:

                    #if new date: add to list of x_values_to_plot
                    x_values_to_plot.append(x)

                    #check through db for each animal with matching Date_of_Entry
                    for i in range( rd1.dbsize() ):

                        #will there be an issue with b formatting? should we use [1:]?
                        if (x == rd1.hget(i, 'Date_of_Entry')):

                            #increment animal_outcomes_of_day count
                            animal_outcomes_of_day = animal_outcomes_of_day + 1

                    #finalize count for the day
                    y = animal_outcomes_of_day

                    #add total count to list of y_values_to_plot
                    y_values_to_plot.append(y)

                #reset animal_outcomes_of_day count before moving to next day
                animal_outcomes_of_day = 0

        #plot line graph
        plt.scatter(x_values_to_plot, y_values_to_plot)
        #plt.show()
        plt.savefig('/outcomes_by_date.png')

        with open('/outcomes_by_date.png', 'rb') as f:
            img = f.read()

        rd.hset(f'job.{jid}', 'result', img)
        #rd.hset(jobid, 'image', img)        


    #analysis: plot total # of outcomes by type of animal in date range
    if (job_type == 'animal_type'):
    
        animal_types = ['Bird', 'Cat', 'Dog', 'Livestock', 'Other']
        animal_counts = [0, 0, 0, 0, 0]

        for key in rd1.keys():

            this_animal_type = str(key['Animal_Type'])[1:]
            if this_animal_type == "'Bird'":
                animal_counts[0] += 1
            elif this_animal_type == "'Cat'":
                animal_counts[1] += 1
            elif this_animal_type == "'Dog'":
                animal_counts[2] += 1
            elif this_animal_type == "'Livestock'":
                animal_counts[3] += 1
            elif this_animal_type == "'Other'":
                animal_counts[4] += 1

        plt.clf()
        plt.bar(animal_types, animal_counts, color='green')
        plt.xlabel('Animal Type')
        plt.ylabel('Frequency')
        plt.title('Outcomes by Animal Type')
        #plt.show()
        plt.savefig('/outcomes_by_animal_type.png')
        with open('/outcomes_by_animal_type.png', 'rb') as f:
            img = f.read()

        rd.hset(f'job.{jid}', 'result', img)

             
    jobs.update_job_status(jid, 'complete')

execute_job()
