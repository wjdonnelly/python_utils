import sys
import re
import csv
import fileinput
import json
import csv
import time
import datetime
from datetime import datetime
import requests
import StringIO
import os
import dateutil.parser
import time

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
admin_email = "jannie.hensen@gravidamaurislimited.org"
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
#today's date
today_date = datetime.date.today()

#start now plus 30 min in ISO format
icws = datetime.datetime.now()


#interval = 30 minutes
interval = 1800

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

        try:
            output = callAPIreturningJSON(AccountsURL, headers, payload, logFileName)
        except:
            print ('Something bad happened psting to the accounts API.')

        requestServices = requests.get(ServicesURL, headers=headers)
        services = requestServices.json()

        #set up timing parameters

        icws = icws + datetime.timedelta(0,1800)
        icwe = icws + datetime.timedelta(0,9000)

        icws_iso = icws.strftime("%Y-%m-%dT%H:%M:%S")
        icwe_iso = icwe.strftime("%Y-%m-%dT%H:%M:%S")

    

    
        #print(time.strftime(nextDate,"%Y-%m-%dT%H%M%S"))
    
        
        post_body_agreement = {
            "accountId" : str(output['id']), \
                "billingAddress" : { 'city': str(row["City"]), \
                      "country" : str(row["Country"]), \
                      "id" : str(output['address']['id']),\
                      'latitude': str(row["Latitude"]), \
                      'lineOne': str(row["Address 1"]), \
                      "lineTwo" : "",\
                      'longitude': str(row["Longitude"]),\
                      'postalCode': str(row["Zip"]), \
                      'state': str(row["State"]), \
                'stateAbbreviation': str(row["State Abbreviation"]) \
                    },\
              "contact" : { "email" : "",\
                  "id" : str(output['contact']['id']),\
                  "name" : str(output['contact']['name']),\
                  "phone" : ""\
                },\
              "effectiveDate" : today_date,\
              "initialCommitmentTech" : "technicians/1",\
              "initialCommitmentWindowEnd" : icws_iso,\
              "initialCommitmentWindowStart" : icwe_iso,\
              "invoiceSchedule" : 0,\
              "issue" : "",\
              "name" : str(row["Company Name"]),\
              "preferredEndTime" : "23:59:59",\
              "preferredStartTime" : "00:00:00",\
              "serviceAddress" : { 'city': str(row["City"]), \
                  "country" : str(row["Country"]), \
                  "id" : str(output['address']['id']), \
                  "latitude" : str(row["Latitude"]), \
                  "lineOne" : str(row["Address 1"]), \
                  "lineTwo" : "",\
                  "longitude" : str(row["Longitude"]),\
                  "postalCode" : str(row["Zip"]), \
                  "state" : str(row["State"]), \
                  "stateAbbreviation" : str(row["State Abbreviation"]) \
                },\
              "services" : [ { "duration" : int(services [0]['duration']),\
                    "offeringId" : str(services [0]['id']),\
                    "price" : int(services [0]['price'])\
                  } ],\
              "zipTaxGeoData" : { "citySalesTax" : 0.045000001788139,\
                  "cityTaxCode" : "NE 8081",\
                  "cityUseTax" : 0.045000001788139,\
                  "countySalesTax" : 0,\
                  "countyTaxCode" : "",\
                  "countyUseTax" : 0,\
                  "districtSalesTax" : 0.003749999916181,\
                  "districtUseTax" : 0.003749999916181,\
                  "geoCity" : "NEW YORK",\
                  "geoCounty" : "NEW YORK",\
                  "geoPostalCode" : "10025",\
                  "geoState" : "NY",\
                  "stateSalesTax" : 0.039999999105930002,\
                  "stateUseTax" : 0.039999999105930002,\
                  "taxSales" : 0.088749997317791,\
                  "taxUse" : 0.088749997317791,\
                  "txbFreight" : "Y",\
                  "txbService" : "L"\
                }\
            }

        payload2 = json.dumps(post_body_agreement)

        print payload2
        print post_body_agreement

        try:
            output2 = callAPIreturningJSON(AgreementsURL, headers, payload2, logFileName)
        except:
            print ('Something bad happened psting to the agreements API.')




            payload = json.dumps(post_body_account)

            print(payload)

            #increment the account loop
            j = j + 1
            
            #call the api
            #output = callAPI(url, headers, payload, logFileName)
            #print(str(output.status_code))
            print(post_body)
        #wait    
        time.sleep(delay)

        #reset inner loop
        j = 0
        #increment the cycle loop
        i = i + 1

    
        
                   

   
