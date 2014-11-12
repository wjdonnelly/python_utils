import sys
import re
import csv
import fileinput
from collections import Counter
import urllib
import urllib2
import json
import csv



# get the input filename from the command line
#fileArg = sys.argv[1]

#set the constants
#input the url
url_base = "http://raven2:8080/databases/pp1-b448e853-f94a-4e30-8c11-a71d670a4707/streams/query/allWorkOrders?format=excel&pagesize=1024"

outputFilename = "c:/sites/test_raven_workorders.csv"
outputFile = open(outputFilename, 'w')
#outputFilename = fileArg + ".byIP.txt"

#set the number of loops
numberofloops = 304

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
