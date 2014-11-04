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

#this script makes the same get call over and over for load simulation


#function to call the API
def callAPI(url, payload, headers, multiplier):
    for iteration in range(0, multiplier):
        print("> " + url )
        r = requests.get(url, params = payload, headers=headers)
        print("< status_code=" + str(r.status_code))
        
    return;

def authorize():
    url_base = "http://ngp-qa-web:85/"
    api_call = "api/token"
    auth_url = url_base + api_call
    payload = "grant_type=password&username=tim@mds.mds&password=letmein123&scope=marathon_odyssey"
    headers = {}
    r = requests.post(auth_url, payload, headers=headers)
    id = str(r.json()["access_token"])
    full_token = "Bearer " + id
    print(full_token)
    return(full_token);                
    

# get the input filenames and test parameters from the config file
#fileArg = sys.argv[1]

#set the constants
mode = "cps" #mode can be cps or script
multiplier = 30
start_hour = "11"
#input the script url
url_base = "http://ngp-qa-web:85/"
api_call = "odyssey/accounts/details/Accounts%2f1"
url = url_base + api_call
params = {}
token = ""

tenant_num = 1
if mode == "cps":
    #run the selected calls per second
    cycles = 120000
    cps = 20
    for i in range(1,cycles):
        sys.stdout.write("-" + str(i))
        for j in range(0, 70):
            #line = lines[j]
            #print("line " + line[0])
            
            payload = {}
            headers = {"Authorization" : token}
                
    
            #print(payload['accountID'] + " " + headers['tenantID'])
            #sys.stdout.write('.')
            r = requests.get(url, params = payload, headers=headers)
            if r.status_code == 401:
                #reauthorize
                token = authorize()
            print(str(r.status_code))#sys.stdout.write(line[0])
            print(str(r.elapsed))
            time.sleep(.01)
        i = i + 1
                   
else:
    #load a timing script from field IIS logs
    
    # hardcode for now - the input filename for script_timer
    #fileArg = sys.argv[1]
    fileArg = 'c:/sites/u_0902_test.txt'

    # open the extract file for processing
    timerFile = open(fileArg, 'r')
     

    #outputFilename = "c:/sites/" + server + "_" + date + "_byAPIandMethod.txt"
    #outputFilename = fileArg + ".byIP.txt"

    #outputFile = open(outputFilename, 'w')
     


    #read the IIS logs to establish timing
    #set up a dictionary for the timing tuples

    script_timer = {}
    i = 1
    for line in timerFile:
       
        if line[11:13] == start_hour: #check if the line is a valid execution
        
        #extract the data fields by character position
            rowData = line.split()
            apiRaw = rowData[10]
            if "https://app.serviceceo.com/" in apiRaw:
                #apiRaw = apiRaw.replace("https://app.serviceceo.com/", "",1)
                #apiParts = apiRaw.split("?")
                #if len(apiParts) > 1:
                #    apiCall = apiParts[0]
                #else:
                dt_string = rowData[0] + " " + rowData[1]
                s_time = datetime.strptime(dt_string, "%Y-%m-%d %H:%M:%S")
                apiCall = rowData[4].lower()
                method = rowData[3] #pull the method request from the entry
                if apiCall[0] == "/":
                    apiCall = apiCall[1:]
                #query.append(method + ":" + apiCall)
                #time.sleep(1)
                #print(s_time)
                script_timer[i] = [s_time, method]
                i = i + 1

    #read the tenant_id file


    #calculate the intervals between timeslots
    i = 1
    cps = 1 #call per second


    script_timer_size = len(script_timer)
    #fix this to output the formated start time
    #print("start_hour=" + script_timer[1][3])
    for timeslot in range(1, script_timer_size):
        
        delta = script_timer[timeslot + 1][0] - script_timer[timeslot][0]
        #print(str(timeslot) + " " + str(script_timer[timeslot]))
        if delta.seconds == 0:
            callAPI(url, params, headers, multiplier)
            cps = cps + 1
            next 
        #else needs to know if a cps > 1 loop was just completed
        else:
            if cps > 1:
                print("Sent " + str(cps))
                cps = 1 #reset the cps flag
                callAPI(url, params, headers, multiplier)
                
            #if cps > 15:
            #    print("timeslot=" + str(timeslot) + " at " + str(script_timer[i].hour) + ":" + str(script_timer[i].minute) + ":" + str(script_timer[i].second) + " delta=" + str(delta.seconds) + " -- calls=" + str(cps) + '\n')
            print("Wait for " + str(delta.seconds) + " seconds")
            time.sleep(delta.seconds)
            callAPI(url, params, headers, multiplier)
        #print("timeslot=" + str(timeslot) + " at " + str(script_timer[i].minute) + ":" + str(script_timer[i].second) + " delta=" + str(delta.seconds) + " -- calls=" + str(cps) + '\n')
        i= i + 1


    #outputFilename = "c:/sites/test_raven_workorders.csv"
    #outputFile = open(outputFilename, 'w')
    #outputFilename = fileArg + ".byIP.txt"
    stop()
    #loop thru the script_timer to run the test
    for i in range(1, numberofloops):
        #construct the URL
        if i == 1:
            page = 1024
            url = url_base
            page = page + 1
            print("called " + url + '\n')
            response = urllib2.urlopen(url)
            print("response from " + url + '\n')
            output = response.read()
            outputFile.write(output)
            print("proceessed from " + url + '\n')
            response = ""
            
        else:
            url = url_base + "&start=" + str(page)
            page = page + 1024
            print("called " + url + '\n')
            response = urllib2.urlopen(url)
            print("response from " + url + '\n')
            output = response.read()
            outputFile.write(output)
            response = ""


    #outputFilename = fileArg + ".byIP.txt"


     




    #readlines from file until EOF
    #query = []
    #for line in inputFile:
       
    #   if line[0:4] == "2014": #check if the line is a valid execution
        #extract the data fields by character position
    #        rowData = line.split()
    #        query.append(rowData[5])
        

        #create the new line (tab separated) to output
        #output = '\t' + date + '\t' + platform + '\t' + server + rowData[4] '\n'
        #sys.stdout.write(output)
     
        #output the line to the output file
        #outputFile.write(output)
         
            

    #listWriter = csv.DictWriter(open(outputFilename, 'wb'), fieldnames=tally[tally.keys()[0]].keys(), delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL) 
                                
    #for row in tally:
        #print(row)
        #print(tally[row])
        #create the new line (tab separated) to output
    #    output = '\t' + date + '\t' + platform + '\t' + server + '\t' + row + '\t' + str(tally[row]) + '\n'
        #sys.stdout.write(output)
     
        #output the line to the output file
        


    #close the input and output files
    outputFile.close()
