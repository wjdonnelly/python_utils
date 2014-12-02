import sys
#import re
import csv
import fileinput
import json
import time
from datetime import datetime
import requests
#import StringIO
import os

#creates tenants in the QA environment

#function to post to the API and log the call and responses
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
    dbServer = "http://ngp-qa-web:85/"
    api_call = "api/token"
    auth_url = dbServer + api_call
    payload = "grant_type=password&username=" + email + "&password=letmein123&scope=marathon_odyssey"
    headers = {}
    r = requests.post(auth_url, payload, headers=headers)
    #print(r.content)
    id = str(r.json()["access_token"])
    full_token = "Bearer " + id
    #print(full_token)
    return(full_token);

def admin_authorize(email):
    dbServer = "http://ngp-qa-web:86/"
    api_call = "administration/token"
    auth_url = dbServer + api_call
    payload = "grant_type=password&username=" + email + "&password=letmein123&scope=marathon_admin"
    headers = {}
    r = requests.post(auth_url, payload, headers=headers)
    if r.status_code == 200:
        id = str(r.json()["access_token"])
        full_token = "Bearer " + id
    else:
        full_token = ""
    #print(full_token)
    return(full_token);

def useJSONFile(url, headers, file, logFileName):
    #open the file
    try:
        apiPathName = "\\\\mds-fs01\\pitcrew\\api_testing"
        jsonFileName = os.path.join(apiPathName, file)
        jsonFile = open(jsonFileName, 'rb')
    except:
        print("Terminating Script: Could not open json file (" + jsonFileName + ").")
        sys.exit("Terminating Script: Could not open script file (" + jsonFileName + ").")
        
    #read the json body
    payload = jsonFile.read()
        
    #call the api
    output = callAPI(url, headers, payload, logFileName)
    jsonFile.close()

    #log the output
    
    return(output);


##def useCSVfile(
##
def createServices(url, headers, file, logFileName):
    #open the file
    apiPathName = "\\\\mds-fs01\\pitcrew\\api_testing"
    csvFileName = os.path.join(apiPathName, file)
    try:
       
        csvFile = csv.DictReader(open(csvFileName))
        print(csvFileName)
        #csvFile = open(csvFileName, 'rb')
    except:
        print("Terminating Script: Could not open csv file (" + csvFileName + ").")
        sys.exit("Terminating Script: Could not open csv(" + csvFileName + ").")

    #csvFileReader = csv.DictReader(open(csvFileName))

    for row in csvFile:

        intFrequency = 0

        if str(row["Frequency"]) == 'One Time':
            intFrequency = 0
        if str(row["Frequency"]) == 'Weekly':
            intFrequency = 1
        if str(row["Frequency"]) == 'Monthly':
            intFrequency = 2
        if str(row["Frequency"]) == 'Quarterly':
            intFrequency = 3

        post_body = { \
            'Name': str(row["Name"]), \
            'Duration': int(row["Duration (Minutes)"]) * 60000, \
            'Frequency': intFrequency ,\
            'Price': int(row["Price"]),\
            }
        output = callAPI(url, headers, post_body, logFileName)
        #return guid
        
    return(output);
        
def createEmployees(url, headers, file, emailDomain, dbid, logFileName):
    #open the file
    apiCall = ":86/administration/users"
    url = url + apiCall
    apiPathName = "\\\\mds-fs01\\pitcrew\\api_testing"
    csvFileName = os.path.join(apiPathName, file)
    try:
       
        csvFile = csv.DictReader(open(csvFileName))
        print(csvFileName)
        #csvFile = open(csvFileName, 'rb')
    except:
        print("Terminating Script: Could not open csv file (" + csvFileName + ").")
        sys.exit("Terminating Script: Could not open csv(" + csvFileName + ").")

    for row in csvFile:
        userIDfromResponse = ''
        post_body_admin = ''
        post_body_technician = ''

        post_body_user = { \
        'email': str(row["First Name"]) + str(row["Last Name"]) + emailDomain, \
        'name': str(row["First Name"]) + ' ' + str(row["Last Name"]), \
        'password': str(row["Password"]), \
        'tenantId': dbid}

        # Do a post here to create the user
        userIDfromResponse = callAPI(url, headers, post_body_user, logFileName)
        
        # Grab the userID and set userIDfromResponse
        # Make some logging

##        if str(row["Role"]) == 'Administrator':
##            post_body_admin = {'userID': userIDfromResponse}
##
##        # Do a post here to create the admin
##        # Make some logging
##
##        if str(row["Role"]) == 'Technician':
##            post_body_technician = { \
##            'callsign': str(row["Callsign"]), \
##            'endingAddress': \
##                {'lineOne': str(row["EndingAddress.LineOne"]), \
##                'city': str(row["EndingAddress.City"]), \
##                'state': str(row["EndingAddress.State"]), \
##                'stateAbbreviation': str(row["EndingAddress.StateAbbreviation"]), \
##                'postalCode': str(row["EndingAddress.postalCode"]), \
##                'country': str(row["EndingAddress.Country"]), \
##                'latitude': float(row["EndingAddress.Latitude"]), \
##                'longitude': float(row["EndingAddress.Longitude"]),\
##                },\
##            'startingAddress': \
##                {'lineOne': str(row["StartingAddress.LineOne"]), \
##                'city': str(row["StartingAddress.City"]), \
##                'state': str(row["StartingAddress.State"]), \
##                'stateAbbreviation': str(row["StartingAddress.StateAbbreviation"]), \
##                'postalCode': str(row["StartingAddress.postalCode"]), \
##                'country': str(row["StartingAddress.Country"]), \
##                'latitude': float(row["StartingAddress.Latitude"]), \
##                'longitude': float(row["StartingAddress.Longitude"]),\
##                },\
##            'userID': userIDfromResponse}
    return(output);


def createTeams(url, headers, file, logFileName):
    #open the file
    apiPathName = "\\\\mds-fs01\\pitcrew\\api_testing"
    csvFileName = os.path.join(apiPathName, file)
    try:
       
        csvFile = csv.DictReader(open(csvFileName))
        print(csvFileName)
        #csvFile = open(csvFileName, 'rb')
    except:
        print("Terminating Script: Could not open csv file (" + csvFileName + ").")
        sys.exit("Terminating Script: Could not open csv(" + csvFileName + ").")

    for row in csvFile:

        post_body = { \
            'callsign': str(row["CallSign"]), \
            'isNew': str(True), \
            'name': str(row["Team Name"]),\
            'technicians': [] , \
            'endingAddress': \
                {'lineOne': str(row["EndingAddress.LineOne"]), \
                'city': str(row["EndingAddress.City"]), \
                'state': str(row["EndingAddress.State"]), \
                'stateAbbreviation': str(row["EndingAddress.StateAbbreviation"]), \
                'postalCode': str(row["EndingAddress.postalCode"]), \
                'country': str(row["EndingAddress.Country"]), \
                'latitude': float(row["EndingAddress.Latitude"]), \
                'longitude': float(row["EndingAddress.Longitude"]),\
                },\
            'startingAddress': \
                {'lineOne': str(row["StartingAddress.LineOne"]), \
                'city': str(row["StartingAddress.City"]), \
                'state': str(row["StartingAddress.State"]), \
                'stateAbbreviation': str(row["StartingAddress.StateAbbreviation"]), \
                'postalCode': str(row["StartingAddress.postalCode"]), \
                'country': str(row["StartingAddress.Country"]), \
                'latitude': float(row["StartingAddress.Latitude"]), \
                'longitude': float(row["StartingAddress.Longitude"])}, \
            }
        output = callAPI(url, headers, post_body, logFileName)
    return(output);

def useRaw(url, headers, payload, logFileName):
   #output = callAPI(url, headers, payload,logFileName)
    output = requests.post(url, payload, headers=headers)
    #print("< status_code=" + str(r.status_code))
    #output = url + "," + str(r.status_code) +  "," + str(r.elapsed) + "," + rowData[2] + "," + dbid  + '\n'
    #callAPI(url, headers, payload, logFileName)

    #log the results
    if output.status_code == 200:
        s = output.json()
        id = s["id"].encode("ascii")
    else:
    #log that the post fileinput
         id = output.content
   
    #log the results
    #log_output = url + "," + str(output.status_code) +  "," + str(output.elapsed) + "," payload + "," + id  + '\n'
    log_output = url + "\t" + str(output.status_code) +  "\t" + str(output.elapsed) + "\t" + str(payload) + "\t" + id  + '\n'
    logFile = open(logFileName, 'a')   
    #sys.stdout.write(output)
 
    #output the line to the output file
    logFile.write(log_output)
    return(output);

#read the tenant_file
apiPathName = "\\\\mds-fs01\\pitcrew\\api_testing"
tenantPath = "Tenants"
file = "tim.csv"
tenantFileName = os.path.join(apiPathName, tenantPath, file)
#tenantFileName = "c:/sites/make_10_tenants.csv"
try:
    tenant_array = csv.DictReader(open(tenantFileName, 'rb'), delimiter=',', quotechar='"')
except:
    print("Terminating Script: Could not open script file (" + tenantFileName + ").")
    sys.exit("Terminating Script: Could not open script file (" + tenantFileName + ").")

#set up the pass/fail variable
success = 1

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
    
        

#get admin auth token

admin_token = admin_authorize("admin@marathondata.com")
if admin_token == "":
    print("Failed to get admin token")
    sys.exit("Failed to get admin token")

print(admin_token)
#set up base_url
dbServer = "http://ngp-qa-web"




for tenant in tenant_array:



    #Step 1 - create the tenant
    post_body = { 'active': 'true', 'companyName': tenant['companyName'], 'emailAddress': tenant['emailAddress'], \
                  'invoiceNumberSeed' : tenant['invoiceNumberSeed'], 'isNew': 'true', 'licenses': tenant['licenses'], \
                   'name': tenant['name'], 'type': 0, 'workOrderNumberSeed' : tenant['workOrderNumberSeed']}

    

    #set up the url
    api_call = ":86/administration/tenants"
    url = dbServer + api_call

    #set up the request header and body
    
    headers = {'content-type': 'application/json', 'Authorization' : admin_token}
              
    payload=json.dumps(post_body)

    output = useRaw(url, headers, payload, logFileName)
    #output = requests.post(url, payload, headers=headers) 
    print(output.content)
    

    if output.status_code == 200:
        s = output.json()
        dbid = s["id"].encode("ascii")
        time.sleep(60)
        
        
    elif output.status_code == 409:
        #get the dbid if the database exists already
        dbid = "1234" #need this to create employees
        id = output.content
    else:
        #log that the tenant did not create
        success = 0
        id = output.content
        break
    #log the results
    #output = dbServer + "," + str(output.status_code) +  "," + str(output.elapsed) + "," + tenant['Tenant_Admin_Email'] + "," + dbid  + '\n'
    #sys.stdout.write(output)
 
    #output the line to the output file
    #print(output)
    #logFile.write(output)

    #get token for this tenant
    token = authorize(tenant['emailAddress'])
    print(token)
    headers = {'content-type': 'application/json', 'Authorization' : token}

   

   #set up the service hours
    api_call = ":85/api/serviceHours"
    url = dbServer + api_call
    #output = useJSONFile(url, headers, "hours_9-5MF_NoBreaks_EST.json")
    output = useJSONFile(url, headers, "Hours\\" + tenant['Hours'], logFileName)
    if output.status_code > 204:
        print(output.content)
        success = 0

    #set up the Territories
    api_call = ":85/api/serviceTerritories"
    url = dbServer + api_call
    output = useJSONFile(url, headers, "Territories\\" + tenant['Territories'], logFileName)
    if output.status_code > 204:
        print(output.content)
        success = 0
        
     #set up the services
    api_call = ":85/api/serviceOfferings"
    url = dbServer + api_call
    output = createServices(url, headers, "Services\\" + tenant['Services'], logFileName)
    if output.status_code > 204:
        print(output.content)
        success = 0

     #set up the holidays
    api_call = ":85/api/companyHolidays"
    url = dbServer + api_call
    output = useJSONFile(url, headers, "Holidays\\" + tenant['Holidays'], logFileName)
    if output.status_code > 204:
        print(output.content)
        success = 0

  #set up the teams
    api_call = ":85/api/teams"
    url = dbServer + api_call
    output = createTeams(url, headers, "Teams\\" + tenant['Teams'], logFileName)
    if output.status_code > 204:
        print(output.content)
        success = 0

    #set up the employees
    api_call = ""
    url = dbServer + api_call
    
    output = createEmployees(url, headers,  "Employees\\" + tenant['Employees'], tenant["Email_Domain"], dbid, logFileName)
    if output.status_code > 204:
        print(output.content)
        success = 0


if success == 1:
    print("everything worked")
else:
    print("POST errors: please check the log file (" + logFileName + ")")

    
#close the input and output files

logFile.close()
