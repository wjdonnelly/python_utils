import sys
import re
import csv
import fileinput
from collections import Counter
import json
import csv
import requests




# gets a list of database IDs from a RavenDB server


#input the url
server = "ngp-qa-db"
port = "8080"
url_base = "http://" + server + ":" + port + "/" 
api_call = "databases"
url = url_base + api_call 
params = {"pageSize" : "1024"}

#set the output file for the test data
outputFilename = "c:/sites/databases_" + server + ".csv"
outputFile = open(outputFilename, 'wb')

r = requests.get(url, params = params)
dbids = r.json() #converts the database list to an array


#look up an account_id for each tenant
i=1
for dbid in dbids:

    if dbid.startswith("Marathon") or dbid.startswith("Fake") or dbid.startswith("Odyssey") or dbid.startswith("Maponics") or dbid.startswith("System") or dbid.startswith("NGP"):
        next
    else:
        print(dbid)
    
        outputFile.write(dbid + '\n')



#close the input and output files
outputFile.close()
