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
import math
from collections import Counter

class ngp:
    

    def createTenant(self, name): 
        self.name=name 


        #Initialize the argument we passed with the object 

    def stateTenant(self):
        self.name=name 
         

    def createOneAccount(self, tenant, acctData):
        print(tenantID)
        print(acctData)
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

        accountPayload = json.dumps(post_body_account)

        output = callAPIreturningJSON(AccountsURL, headers, accountPayload, logFileName)


class raven():

    def __init__(self, url_base, dbid):
       
        
        self.server = url_base
        self.dbid = dbid
        try:
            requests.get(url_base)
        except:
            print("Network Error reaching " + url_base)
            sys.exit("Network Error reaching " + url_base)
        
        response = requests.get(url_base)
        if response.status_code > 204:
            print("Network Error reaching " + url_base + " Status Code = " + str(response.status_code))
            sys.exit("Error reaching " + url_base + " Status Code = " + str(response.status_code))

    def getCollections(self):
        apiCall = "/indexes/Raven/DocumentsbyEntityName"
        url = self.server + "/databases/" + self.dbid + apiCall
        startNum = 0
        pageSize = 100
        indexSize = pageSize - 1
        

        params = {"fetch" : "Raven-Entity-Name", "start" : startNum, "pageSize": pageSize}
        
        #get the first page of metadata
        response = requests.get(url, params = params)
        metadata = response.json()
        self.totalResults = metadata["TotalResults"]
        ##print("got the first page")
        ##print(str(self.totalResults))
        linesInPage = len(metadata['Results'])
        
       

        #process the first response
        i=0
        getCounter=1
        k=0
        collectionArray = []

        #check if the linesInPage are less than total results
        if self.totalResults > pageSize:
            lastLine = pageSize
             #calculate the number of other gets needed
            numberOfOtherGets = int(math.ceil(float(self.totalResults)/float(pageSize)))
        else:
            lastLine = linesInPage
            numberOfOtherGets = 0
            
        for i in range(0, lastLine):
            #print(str(metadata['Results'][i]['@metadata']['Raven-Entity-Name']))
            #print(str(i))
            
            collectionArray.append(str(metadata['Results'][i]['@metadata']['Raven-Entity-Name']))
            i+=1
        ##print("gettting " + str(lastLine) + " lines")
        
        
       

        #if the number of docs is more than the pageSize
        if numberOfOtherGets > 0 :
        
            for getCounter in range(1, numberOfOtherGets):
                startNum = startNum + pageSize
                params = {"fetch" : "Raven-Entity-Name", "start" : startNum, "pageSize": pageSize}
                ##print("next get:" + str(getCounter))
                i = 0
                #get the subsequent page of metadata
                response = requests.get(url, params = params)
                metadata = response.json()
                linesInPage = len(metadata['Results'])

                if linesInPage < pageSize:
                    lastLine = linesInPage
                    ##print("gettting " + str(lastLine) + " lines")
                else:
                    ##print("gettting " + str(lastLine) + " lines")
                    lastLine = pageSize
                    
                for i in range(0, lastLine):
                    collectionArray.append(str(metadata['Results'][i]['@metadata']['Raven-Entity-Name']))
                    i+=1
                metadata = ""
                getCounter+=1



        self.collections=Counter()
        for collection in collectionArray:
            self.collections[collection] += 1

        self.collectionNames = self.collections.keys()
   
    
        
    def getSchema(self, drillDown=0):
        self.getCollections()

        api_call = "databases"
        params = {"pageSize" : "1"}

        getMetadata = 0 #by default, don't extract metadata fields

        self.l1_properties = {}
        
        for doc in self.collectionNames:
            url = self.server + "/" + api_call + "/" + self.dbid + "/indexes/dynamic/" + doc
            r = requests.get(url, params = params)
            s = r.json()
            
            
            #this extracts the 1st level JSON property names from the document
            
            l1_fields = s['Results'][0].keys()

            if drillDown == 0:
                self.l1_properties[doc] = l1_fields
            else:
            #loop thru the level 1 fields to check for container fields
                for l1_field in l1_fields:
                    #recurse level1
                    if type(s['Results'][0][l1_field])==type({}): #if the field is a parent
                        #get the keys for the child members at level2
                        l2_fields = s['Results'][0][l1_field].keys()

                        #check each field in level 2
                        for l2_field in l2_fields:
                            if type(s['Results'][0][l1_field][l2_field])==type({}): #if the field is a parent
                            #get the keys for the child members at level

                                l3_fields = s['Results'][0][l1_field][l2_field].keys()
                                for l3_field in l3_fields:
                                    if type(s['Results'][0][l1_field][l2_field][l3_field])==type({}): #if the field is a parent
                                        l4_fields = s['Results'][0][l1_field][l2_field][l3_field].keys()
                                        for l4_field in l4_fields:
                                            print(doc + "," + l1_field + "," + l2_field + "," + l3_field + "," + l4_field) #level4 print
                                    else:
                                        print(doc + "," + l1_field + "," + l2_field + "," + l3_field) #level3 print

                            else:
                                if getMetadata == 1:
                                    print(doc + "," + l1_field + "," + l2_field ) #level2 print
                                else:
                                
                                    if l1_field <> "@metadata":
                                        print(doc + "," + l1_field + "," + l2_field) #level2 print
                        
                    else: #no children below level 1
                        if getMetadata == 1:
                            print(doc + "," + l1_field) #leve1 print
                        else:
                            if l1_field <> "@metadata":
                                
                                print(doc + "," + l1_field) #leve1 printoneNames = self.collectionNames[1]

        
    def queryIndex(self, indexName, params):
        apiCall = "/indexes/" + indexName
        url = self.server + "/databases/" + self.dbid + apiCall
        
        

        #params = {"fetch" : "Raven-Entity-Name", "start" : startNum, "pageSize": pageSize}
        
        #get the first page of metadata
        response = requests.get(url, params = params)
        self.results = response.json()
        #self.totalResults = metadata["TotalResults"]
        ##print("got the first page")
        ##print(str(self.totalResults))
        #linesInPage = len(metadata['Results'])
        

    def createIndex(self, indexName, map):
        apiCall = "/indexes/" + indexName
        url = self.server + "/databases/" + self.dbid + apiCall
        response = requests.put(url, map)
        self.statusCode = response.status_code
        self.results = response.json()
        
        
