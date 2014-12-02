import sys
#import re
import csv
import fileinput
import json
import time
#from datetime import datetime
import requests
#import StringIO

#creates the RavenDB indices for the API

#function to call the API
def callAPI(url, payload, headers, multiplier):
    for iteration in range(0, multiplier):
        print("> " + url )
        r = requests.put(url, params = payload, headers=headers)
        print("< status_code=" + str(r.status_code))
        
    return;


#input the script url
dbServer = "http://ngp-qa-db:8080/"

#set up the api call for the end of the URL string
api_call = "indexes/accounts"

#input the path to the file that contains the list of tenant ids
databaseFileName = "c:/sites/databases.csv"


#set up the data for the post body that defines the creation of the Map (ie. the index)
post_data = """{Map: 'from a in docs.accounts
select new 
{
AccountId = a.Id,
Name = a.Name,
Number = a.Number,
City = a.Address.City,
StateAbbreviateion = a.Address.StateAbbreviation,
State = a.Address.State
}' 
}"""



databaseFile = open(databaseFileName, 'rb')


#read the lines from the file and iterate over each line (i.e. dbid) to make the PUT request to create the index
for dbid in databaseFile.xreadlines():
   
    dbid=dbid.strip('\n')
    dbid=dbid.strip('\r')
    #from the compete URL for the current dbid
    url = dbServer + "databases/" + dbid + "/" + api_call
    print(url)

    #set up the request header and body
    
    headers = {'content-type': 'application/json'}
    #payload = post_data            
    params=json.dumps(post_data)
    
    #make the call to the API       
    r = requests.put(url, post_data, headers=headers)
    
    print(r.status_code)
    time.sleep(5)
        
                   
#close the input and output files
databaseFile.close()
