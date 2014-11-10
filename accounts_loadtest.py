import sys
import re
import csv
import fileinput
import json
import csv
import time
from datetime import datetime
import requests
import StringIO
import os

#function to call the API
def callAPI_withload(url, payload, headers, multiplier):
    for iteration in range(0, multiplier):
        print("> " + url )
        #r = requests.get(url, payload, headers=headers)
        #print("< status_code=" + str(r.status_code))
        
    return;

def callAPI(url, headers, payload, logFileName):
    output = requests.post(url, payload, headers=headers)
    
    #print("< status_code=" + str(r.status_code))
    #output = url + "," + str(r.status_code) +  "," + str(r.elapsed) + "," + rowData[2] + "," + dbid  + '\

    #log the results
    if output.status_code == 200:
        s = output.json()
        id = s["id"].encode("ascii")
    else:
    #log that the post fileinput
        #sys.stdout.write(output.content)
        id = output.content

    #log the results
    #log_output = url + "," + str(output.status_code) +  "," + str(output.elapsed) + "," payload + "," + id  + '\n'
    log_output = url + "\t" + str(output.status_code) +  "\t" + str(output.elapsed) + "\t" + str(payload) + "\t" + id  + '\n'
    logFile = open(logFileName, 'a')
    #sys.stdout.write(output)

    #output the line to the output file
    logFile.write(log_output)
    return(output);

def authorize(email):
    url_base = "http://ngp-qa-web:85/"
    api_call = "api/token"
    auth_url = url_base + api_call
    payload = "grant_type=password&username=" + email + "&password=letmein123&scope=marathon_odyssey"
    headers = {}
    r = requests.post(auth_url, payload, headers=headers)
    #print(r.content)
    id = str(r.json()["access_token"])
    full_token = "Bearer " + id
    #print(full_token)
    return(full_token);

# get the input filenames and test parameters from the config file
#fileArg = sys.argv[1]

#set the constants
mode = "cps" #mode can be cps or script
multiplier = 10


url_base = "http://ngp-qa-web:85/"
api_call = "api/accounts"
url = url_base + api_call

params = {}


    
#get the tenant IDs from the log
admin_email = "bernetta.briggs@incorporation.org"
token = authorize(admin_email)
headers = {'content-type': 'application/json', 'Authorization' : token}

##        try:
##            output = callAPI(url, headers, payload, logFileName)
##        except:
##            print ('Something bad happened.')

#set up load parameters
delay = 30
cycles = 10
acctsPerCycle = 10
#read the tenant_file
apiPathName = "\\\\mds-fs01\\pitcrew\\api_testing"
accountPath = "Accounts"
file = "OneThousandAccountsNJNY.csv"
accountsFileName = os.path.join(apiPathName, accountPath, file)

#setup the log files
logPathName = "\\\\mds-fs01\\pitcrew\\api_testing\Logs"
i = datetime.now()
dt = i.strftime('%Y%m%d-%H%M%S')
logFileCalc = file + "_" + dt + ".tsv"
logFileName = os.path.join(logPathName, logFileCalc)

try:
    logFile = open(logFileName, 'a')   
except:
    print("Terminating Script: Can't open log file (" + logFileName + ")")
    sys.exit("Log file is already open")

csvFileReader = csv.DictReader(open(accountsFileName))
if mode == "cps":
    #run the selected calls per minute

    for i in range(0,cycles):
        for j in range(0,acctsPerCycle):
        
            sys.stdout.write("-" + str(i))
            #get the next line from the accountFile
            row = csvFileReader.next()
            
            #set up the post
            post_body_account = { \
                'address': { \
                    'lineOne': str(row["Address 1"]), \
                    'city': str(row["City"]), \
                    'state': str(row["State"]), \
                    'stateAbbreviation': str(row["State Abbreviation"]), \
                    'postalCode': str(row["Zip"]), \
                    'country': str(row["Country"]), \
                    'latitude': str(row["Latitude"]), \
                    'longitude': str(row["Longitude"])\
                    }, \
                'contact': { \
                    'name': str(row["Contact Name"]) \
                },
                'isNew': True, \
                'name': str(row["Company Name"])\
            }

            payload = json.dumps(post_body_account)

            print(payload)

            #increment the account loop
            j = j + 1
            
            #call the api
            output = callAPI(url, headers, payload, logFileName)
            print(str(output.status_code))
        #wait    
        time.sleep(delay)

        #reset inner loop
        j = 0
        #increment the cycle loop
        i = i + 1

    
        
                   

   
