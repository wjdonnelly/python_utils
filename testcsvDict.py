#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      tdembowski
#
# Created:     12/11/2014
# Copyright:   (c) tdembowski 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import csv
import os
import sys
import json
import requests
import time
import datetime
import dateutil.parser
import math
from collections import Counter
from bdb import Breakpoint

#from accounts_loadtest import url

#class odyssey():
#    def __init__(self, env):
        
       
#read the config file and set the config variables

filePath = '//mds-fs01/pitcrew/api_testing/'




 
 #define API endpoints

#     #def __connect__(self):
#         
#         try:
#             requests.get("http://" + self.appServerName)
#         except:
#             print("Network Error reaching " + self.appServerName)
#             sys.exit("Network Error reaching " + self.appServerName)
#             
#         response = requests.get("http://" + self.appServerName)
#         if response.status_code > 204:
#             print("Network Error reaching " + self.appServerName + " Status Code = " + str(response.status_code))
#             sys.exit("Error reaching " + self.appServerName + " Status Code = " + str(response.status_code))
# 
# 
# 
#     def validate(self):
tenantSourceFile = filePath + 'tenants/' + "eap_boston_3.csv"

if os.path.exists(tenantSourceFile) == False:
    print('Source file (' + tenantSourceFile +  ' not found - quitting')
    sys.exit()
else:
    print('Opening main test script file: ' + tenantSourceFile)

with open(tenantSourceFile, mode='r') as infile:
    reader = csv.reader(infile)
    scriptDict = {rows[0]:rows[1] for rows in reader}

stop()    
#        csvFileValidator = csv.DictReader(open(tenantSourceFile))

       