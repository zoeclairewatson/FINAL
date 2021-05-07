
## COE 332 FINAL PROJECT

* Keri Christian ( EID: )
* Zoe Watson ( EID: zcw268 )

# Project Overview

This project is a API using Kubernetes for a database that includes data from Austin animal centers. The data was put into a JSON file with the format as follows:
```
{
     "Animal ID": "A705283",
     "Name": "",
     "DateTime": "6/16/2015 9:00",
     "Date of Birth": "6/15/2014",
     "Outcome Type": "Transfer",
     "Outcome Subtype": "SCRP",
     "Animal Type": "Cat",
     "Sex upon Outcome": "Intact Male",
     "Age upon Outcome": "1 year",
     "Breed": "Domestic Shorthair Mix",
     "Color": "White"
   }
   ```
   It keeps track of animal outcomes, so whether an animal was adopted, transfered, returned to owner, euthanized, etc., when that outcome occurs, what age the animal is when the outcome occurs, what type of animal it is, it's sex upon outcome (male, female, neutered, spayed), and its breed and color. 

The API has CRUD (create, read, update, delete) routes so that the user can interact with the database. It also analyzes the data in two ways using a worker daemon that gets the jobs the user submits from a queue. The analysis is a bar graph showing how many of each animal type shows up in the database (cat,dog,bird,etc) and how many outcomes happen per day given a date range (intended to track productivity of the centers on a given date range)

