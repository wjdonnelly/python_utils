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
import re

#from accounts_loadtest import url

class odyssey():
    def __init__(self, env):


    #read the config file and set the config variables

        self.filePath = '//mds-fs01/pitcrew/api_testing/'
        self.logFilePath = '//mds-fs01/pitcrew/api_testing/logs/'
        self.appServerName = 'ngp-qa-web'
        self.voloAPIKey = 'ODYS-SEYO-DYSS-EYOD'
        self.scriptFile = "eap_boston_3.csv" #hard code

        self.dbServerName = 'ngp-qa-db'
        self.dbServerPort = '8080'
        self.dbServerURL = "http://" + self.dbServerName + ":" + self.dbServerPort
        self.appServerAdminPort = '86'
        self.appServerAPIPort = '85'


        self.logFilePathAdmin = self.filePath + "Logs/Administration/"
        self.sysAdminPassword = 'letmein123'
        self.sysAdminEmail = 'admin@marathondata.com'

        #hard code
        self.sysAdminTokenURL = 'http://' + self.appServerName + ":" + self.appServerAdminPort + '/administration/token'
        self.tenantAdminTokenURL = 'http://' + self.appServerName + ":" + self.appServerAPIPort + '/api/token'
        self.tenantAdminPassword = "letmein123"
        self.adminSchedulingLicensingURL = 'http://' + self.appServerName + ":" + self.appServerAdminPort + '/administration/schedulinglicensing/'
        self.consoleVerbose = 1


        self.headers = {'content-type': 'application/json', 'Authorization' : "blankToken"}
        self.creatingTenants = True
        self.tenantUserName = ""

        #define API endpoints
        self.createTenantsAPI = '/administration/tenants'
        self.apiAccountsAPI = '/api/accounts'
        self.apiAgreementsAPI = '/api/serviceAgreements'
        self.apiServiceOfferingsAPI = '/api/serviceofferings'
        self.apiServiceHoursAPI = '/api/serviceHours'
        self.apiCompanyHolidsaysAPI = '/api/companyHolidays'
        self.apiServiceTerritoriesAPI = '/api/serviceTerritories'
        self.adminUsersAPI =  '/administration/users'
        self.adminTenantAdministratorsAPI = '/administration/tenantadministrator'
        self.apiTechniciansAPI = '/api/technicians'
        self.apiTeamsAPI = '/api/teams'

        self.createTenantsURL = 'http://' + self.appServerName + ':' + self.appServerAdminPort + '/administration/tenants'
        self.apiAccountsURL = 'http://' + self.appServerName + ':' + self.appServerAPIPort + '/api/accounts'
        self.apiAgreementsURL = 'http://' + self.appServerName + ':' + self.appServerAPIPort + '/api/serviceAgreements'
        self.apiServiceOfferingsURL = 'http://' + self.appServerName + ':' + self.appServerAPIPort + '/api/serviceofferings'
        self.apiServiceHoursURL = 'http://' + self.appServerName + ':' + self.appServerAPIPort + '/api/serviceHours'
        self.apiCompanyHolidsaysURL = 'http://' + self.appServerName + ':' + self.appServerAPIPort + '/api/companyHolidays'
        self.apiServiceTerritoriesURL = 'http://' + self.appServerName + ':' + self.appServerAPIPort + '/api/serviceTerritories'
        self.adminUsersURL = 'http://' + self.appServerName + ':' + self.appServerAdminPort + '/administration/users'
        self.adminTenantAdministratorsURL = 'http://' + self.appServerName + ':' + self.appServerAdminPort + '/administration/tenantadministrator'
        self.apiTechniciansURL = 'http://' + self.appServerName + ':' + self.appServerAPIPort + '/api/technicians'
        self.apiTeamsURL = 'http://' + self.appServerName + ':' + self.appServerAPIPort + '/api/teams'
        self.apiDuplicateEmailURL = 'http://' + self.appServerName + ':' + self.appServerAPIPort + '/api/duplicateemployees?email='

    #def __connect__(self):

        try:
            requests.get("http://" + self.appServerName)
        except:
            print("Network Error reaching " + self.appServerName)
            sys.exit("Network Error reaching " + self.appServerName)

        response = requests.get("http://" + self.appServerName)
        if response.status_code > 204:
            print("Network Error reaching " + self.appServerName + " Status Code = " + str(response.status_code))
            sys.exit("Error reaching " + self.appServerName + " Status Code = " + str(response.status_code))



    def validate(self):
        tenantSourceFile = self.filePath + 'tenants/' + self.scriptFile

        if os.path.exists(tenantSourceFile) == False:
            print('Source file (' + tenantSourceFile +  ' not found - quitting')
            sys.exit()
        else:
            print('Opening main test script file: ' + tenantSourceFile)

        self.scriptDict = []
        with open(tenantSourceFile, mode='r') as infile:
            dictReader = csv.DictReader(infile)
            for row in dictReader:
                self.scriptDict.append(row)



#        csvFileValidator = csv.DictReader(open(tenantSourceFile))

        for row in self.scriptDict:
            print('Validating source file...')
            print row["companyName"]
            try:
                companyName = str(row["companyName"])
                adminName = str(row["name"])
                adminEmail = str(row["emailAddress"])
                licenses = int(row["licenses"])
                workOrderNumberSeed = int(row["workOrderNumberSeed"])
                invoiceNumberSeed = int(row["invoiceNumberSeed"])
                emailDomain = str(row["Email_Domain"])

                companyHoursFile = str(row["Hours"])
                companyHolidaysFile = str(row["Holidays"])
                companyTerritory = str(row["Territories"])
                employeesList = str(row["Employees"])
                servicesList = str(row["Services"])
                teamsList = str(row["Teams"])
                accountsList = str(row["Accounts"])
                #accountswithAgreements = str(row["AccountswithAgreements"])
                agreementsPerDay = int(row["AgreementsPerDay"])
                agreementsDelay = int(row["AgreementDelayinSeconds"])
            except:
                print('Source file incomplete, check all rows against format of template.csv')
                sys.exit()

            if os.path.isfile(self.filePath + 'companyhours/' + companyHoursFile) == True:
                print('Processing company hours from: ' + companyHoursFile)
            else:
                print('Using default file! Company hours file (' + self.filePath + companyHoursFile + ') not found.')
                print('')
                sys.exit()




            if os.path.isfile(self.filePath + 'holidays/' + companyHolidaysFile) == True:
                print('Processing company holidays from: ' + companyHolidaysFile)
            else:
                print('Using default file! Company holidays file (' + self.filePath + companyHolidaysFile + ') not found.')
                companyHolidaysFile = "_default"
                sys.exit()

            if os.path.isfile(self.filePath + 'territories/' + companyTerritory) == True:
                print('Processing territories file from: ' + companyTerritory)
            else:
                print('Using default file! Company territories file (' + self.filePath + companyTerritory + ') not found.')
                print('Quitting script')
                sys.exit()

            if os.path.isfile(self.filePath + 'employees/' + employeesList) == True:
                print('Processing employees from: ' + employeesList)
            else:
                print('Using default file! Company employees file (' + self.filePath + employeesList + ') not found.')


            if os.path.isfile(self.filePath + 'services/' + servicesList) == True:
                print('Processing services from: '  + servicesList)
            else:
                print('Using default file! Company services file (' + self.filePath + servicesList + ') not found.')


            if os.path.isfile(self.filePath + 'teams/' + teamsList) == True:
                print('Processing teams from: '  + teamsList)
            else:
                print('Using default file! Company teams file (' + self.filePath + teamsList + ') not found.')


            if accountsList == 'None' or accountsList == '':
                print('No accounts-only file to import, step will be skipped')
            else:
                if os.path.isfile(self.filePath + 'accounts/' + accountsList) == True:
                    print('Processing accounts list from: '  + accountsList)
                else:
                    print('Accounts file (' + self.filePath + accountsList + ') not found.')


            if agreementsPerDay == '0':
                print('No accounts with agreements file to import, step will be skipped')
            else:
                print("Accounts will be created with " + str(agreementsPerDay) + " agreements per day.")
#                 if os.path.exists(self.filePath + 'accounts/' + accountswithAgreements) == True:
#                     print('Company accounts with agreements file exists for: ' + companyName)
#                 else:
#                     print('Company accounts with agreements file does not exist for: ' + companyName)
#                     print('Quitting script')
#                     sys.exit()
            print('Import file is valid')

    def createOneTenant(self):
        pass

    def createTenants(self, createAll = True, finish = True, createAccounts = True, overWrite = True):
        #createAll will create all tenants in the input file - False will create 1 tenant
        #finish will set up holidays, hours, etc - False will not
        #createAccounts will create the accounts in the csv - False will not
        #overWrite will overWrite existing tenants - False will create a new tenant admin email to create a new tenant

        tenantSourceFile = self.filePath + 'tenants/' + self.scriptFile

        if os.path.exists(tenantSourceFile) == False:
            print('Source file does not exist - quitting')
            sys.exit()
        else:
            print('Source File Found')

        csvFileReader = csv.DictReader(open(tenantSourceFile))
        i = 0
        for row in csvFileReader:
            i = i+1
            self.creatingTenants = True
            companyName = str(row["companyName"])
            tenantAdminName = str(row["name"])
            tenantAdminEmail = str(row["emailAddress"])
            licenses = int(row["licenses"])
            workOrderNumberSeed = int(row["workOrderNumberSeed"])
            invoiceNumberSeed = int(row["invoiceNumberSeed"])
            self.emailDomain = str(row["Email_Domain"])
            companyHoursFile = str(row["Hours"])
            companyHolidaysFile = str(row["Holidays"])
            companyTerritory = str(row["Territories"])
            employeesList = str(row["Employees"])
            servicesList = str(row["Services"])
            teamsList = str(row["Teams"])
            accountsList = str(row["Accounts"])
            #accountswithAgreements = str(row["AccountswithAgreements"])
            agreementsPerDay = int(row["AgreementsPerDay"])
            agreementsDelay = int(row["AgreementDelayinSeconds"])

            #__odysseyAdminSession__ = __odysseyAdmin__()
            #__odysseyAdminSession__.setAdminEnvironmentURLs('QA')
            tenant = self.createTenant(tenantAdminName, companyName, tenantAdminEmail, 5, 1000, 1000)

            #__finishTenant__ = odysseyAccounts()
           # __finishTenant__.setEnvironmentURLs("QA")
#             while len(str(__getToken__(self.tenantAdminURL, tenantAdminEmail, self.tenantAdminPassword))) <= 100:
#                 print ('Unable to authenticate user, waiting 5 seconds...')
            time.sleep(5)

            # Allow this to be none
            self.creatingTenants = False
            if finish:
                self.setCompanyHours(companyHoursFile)
                self.setCompanyHolidays(companyHolidaysFile)        # Allow this to be none
                self.setCompanyTerritory(companyTerritory)
                #self.populateEmployees(employeesList)
                self.populateServices(servicesList)
                self.populateTeams(teamsList)

            if createAccounts:
                if accountsList == 'None' or accountsList == '':
                    print ('No accounts-only file to import, step will be skipped')
                else:
                    if self.consoleVerbose >= 1: print("Adding accounts from " + accountsList)
                    self.__createAccounts__(accountsList)
#             if agreementsPerDay == '25':
#                 print ('No accounts with agreements file to import, step will be skipped')
#             else:
#                 self.createAgreements('KearnyJerseyCity.csv', agreementsPerDay, agreementsDelay, True)
#
#             #finish tenant creation
#             #setAdminAndTenantID(tenantAdminEmail)
            #emailDomain = emailDomain


            if i==1 and createAll == False:
                break




#class __odysseyAdminSession__():
#     Username = self.adminUserName
#     Password = 'letmein123'
#     logFilePathAdmin = "//mds-fs01/pitcrew/api_testing/Logs/Administration/"

#     def __setAdminEnvironment__(self, env):
#         if env.lower() == 'qa':
#             self.appServerName = 'ngp-qa-web'
#             self.appServerAdminPort = '86'
#             self.appServerAPIPort = '85'
#         if env.lower() == 'localhost':
#             self.appServerName = 'localhost'
#             self.appServerAdminPort = '86'
#             self.appServerAPIPort = '85'
#         self.adminTokenURL = 'http://' + self.appServerName + ':' + self.appServerAdminPort + '/administration/token'
#         self.adminTenantsURL = 'http://' + self.appServerName + ':' + self.appServerAdminPort + '/administration/tenants'
#         self.adminSchedulingLicensingURL = 'http://' + self.appServerName + ':' + self.appServerAdminPort + '/administration/schedulinglicensing/'

    def createTenant(self, tenantAdminName, CompanyName, tenantAdminEmail, LicenseCount, wordOrderNSeedumber, invoiceNumberSeed):
        logFileName = self.__createAdminLogFileName__()

        post_body_tenant = { \
            'name': tenantAdminName, \
            'companyName': CompanyName, \
            'emailAddress': tenantAdminEmail, \
            'licenses': LicenseCount, \
            'type': 0, \
            'active': True, \
            'isNew': True, \
            'workOrderNumberSeed': wordOrderNSeedumber, \
            'invoiceNumberSeed': invoiceNumberSeed, \
            }


        self.tenantAdminEmail = tenantAdminEmail
        createTenantsURL = 'http://' + self.appServerName + ':' + self.appServerAdminPort + '/administration/tenants'
        tenantPayload = json.dumps(post_body_tenant)
        tenantResults = {}
        tenantResults = self.__postAPI__(self.createTenantsURL, tenantPayload, logFileName)



        if tenantResults["statusCode"] == 200:

            pass

        elif tenantResults["statusCode"] == 409:
            self.getDBID()
            if self.consoleVerbose >= 1: print("Tenant already exists with tenantID: " + self.tenantID)

        else:
            print("Error: " + tenantResults["content"])
            return()


        post_body_scheduling = { \
        'id': '00000000-0000-0000-0000-000000000000', \
        'voloAPIKey': self.voloAPIKey, \
        'schedulingType': 1 }

        schedulingPayload = json.dumps(post_body_scheduling)
        schedulingLicensingFullURL = self.adminSchedulingLicensingURL + str(tenantResults["id"])
        SchedulingConfigResults = self.__postAPI__(schedulingLicensingFullURL, schedulingPayload, logFileName)

    def __createAdminLogFileName__(self):
        i = datetime.datetime.now()
        dt = i.strftime('%Y%m%d-%H%M%S')
        logFileCalc = 'Administration' + "_" + dt + ".tsv"
        fullLogFileName = self.logFilePathAdmin + logFileCalc

        return fullLogFileName




    def __postAPI__(self, url, payload, logFileName):

        results = {}
        output = requests.post(url, payload, headers=self.headers)
        (str(output.status_code))
        if output.status_code == 401 or output.status_code == 500:
            if self.consoleVerbose >= 1: print("Got a " + str(output.status_code) + " from " + url)
            token = self.__getToken__()
            if self.consoleVerbose >= 1: print("got a new token: " + token)
            self.headers = {'content-type': 'application/json', 'Authorization' : token}
            output = requests.post(url, payload, headers=self.headers)

        if output.status_code == 200:
            jsonResponse = output.json()
            results["id"] = jsonResponse["id"].encode("ascii")
        else:
            results["id"] = ""

        results["content"] = output.content
        results["statusCode"] = output.status_code

        log_output = url + "\t" + str(output.status_code) +  "\t" + str(output.elapsed) + "\t" + str(payload) + "\t" + results["id"]  + '\n'
        try:
            logFile = open(logFileName, 'a')
        except:
            print("Failed to open to log file")
        try:
            logFile.write(log_output)
        except:
            print("Failed to write to log file")
        if self.consoleVerbose >= 2: print('Logging API post: ' + log_output)

        return(results);

    def __getAPI__(self, url, params):

        results = {}
        output = requests.get(url, params=params, headers=self.headers)
        if output.status_code == 401 or output.status_code == 500:
            if self.consoleVerbose >= 1: print("Got a " + str(output.status_code) + " from " + url)
            token = self.__getToken__()
            if self.consoleVerbose >= 1: print("got a new token: " + token)
            self.headers = {'content-type': 'application/json', 'Authorization' : token}
            output = requests.get(url, params=params, headers=self.headers)
            #print(str(output.status_code))

        if output.status_code == 200:
            jsonResponse = output.json()
            try:
                results["id"] = jsonResponse["id"].encode("ascii")
            except:
                results["id"] = ""

        results["content"] = output.content
        results["statusCode"] = output.status_code
        return(results)

    def getAccounts(self):

        results = {}
        params = ''
        output = requests.get(self.apiAccountsURL , params=params, headers=self.headers)
        print(str(output.status_code))
        if output.status_code == 401 or output.status_code == 500:
            if self.consoleVerbose >=1: print("Got a " + str(output.status_code) + " from " + self.apiAccountsURL)
            token = self.__getToken__()
            if self.consoleVerbose >= 1: print("got a new token: " + token)
            self.headers = {'content-type': 'application/json', 'Authorization' : token}
            output = requests.get(self.apiAccountsURL, params=params, headers=self.headers)
            print(str(output.status_code))

        if output.status_code == 200:
            jsonResponse = output.json()
            self.accountList =  jsonResponse
        else:
            self.accountList =  ""




    def __setAdminAndTenantID__(self, email):
        postHeaders = {}
        postPayload = "grant_type=password&username=" + email + "&password=letmein123&scope=marathon_odyssey"
        response = requests.post(self.apiTokenURL, postPayload, headers=postHeaders)
        try:
            self.tenantID = response.json()['tenantId']
            self.AdminEmail = email
            result = 'Success'
        except:
            result = 'Failure'
        return(result);

    def __createLogFileName__(self, functionCalling):
        i = datetime.datetime.now()
        dt = i.strftime('%Y%m%d-%H%M%S')
        logFolderName = self.tenantAdminEmail
        logFolderName = logFolderName.replace('@', '_')
        logFolderName = logFolderName.replace('-', '_')
        logFolderName = logFolderName.replace('.', '_')
        if os.path.exists(self.logFilePath + logFolderName) == False:
            os.mkdir(self.logFilePath + logFolderName)
        logFileCalc = functionCalling + "_" + dt + ".tsv"
        fullLogFileName = self.logFilePath + logFolderName + '/' + logFileCalc

        return fullLogFileName;

    def __getToken__(self):
        if self.creatingTenants:
            userName = self.sysAdminEmail
            authURL = self.sysAdminTokenURL
            scope = "&scope=marathon_admin"
            password = self.sysAdminPassword
        else:
            userName = self.tenantAdminEmail
            authURL = self.tenantAdminTokenURL
            scope = "&scope=marathon_odyssey"
            password = self.tenantAdminPassword

        postPayload = "grant_type=password&username=" + userName + "&password=" + password + scope

        response = requests.post(authURL, postPayload, headers=self.headers)
        try:
            accessToken = str(response.json()["access_token"])
            fullAccessToken = "Bearer " + accessToken
        except:
            fullAccessToken = ''
        return(fullAccessToken);
    pass



    def setCompanyHours(self, companyHoursInJSON):
        if self.consoleVerbose >= 1: print("Setup the Hours")
        if self.consoleVerbose >= 1: print("Creating Tenants is" + str(self.creatingTenants))
        logFileName = self.__createLogFileName__('setCompanyHours')
        companyHoursSourceFile = self.filePath + 'CompanyHours/' + companyHoursInJSON
        jsonCompanyHours = open(companyHoursSourceFile, 'rb')
        payloadCompanyHours = jsonCompanyHours.read()

        companyHoursResults = self.__postAPI__(self.apiServiceHoursURL, payloadCompanyHours, logFileName);



    def setCompanyHolidays(self, companyHolidsaysInJSON):
        if self.consoleVerbose >= 1: print("Setup the Holidays")
        logFileName = self.__createLogFileName__('setHolidays')
        holidaysSourceFile = self.filePath + 'Holidays/' + companyHolidsaysInJSON
        jsonHolidays = open(holidaysSourceFile, 'rb')
        payloadHolidays = jsonHolidays.read()

        companyHolidaysResults = self.__postAPI__(self.apiCompanyHolidsaysURL, payloadHolidays, logFileName);



    def setCompanyTerritory(self, companyTerritoryInJSON):
        if self.consoleVerbose >= 1: print("Setup the Territory")
        logFileName = self.__createLogFileName__('setTerritory')
        territorySourceFile = self.filePath + 'Territories/' + companyTerritoryInJSON
        jsonTerritory = open(territorySourceFile, 'rb')
        payloadTerritory = jsonTerritory.read()

        companyTerritoryResults = self.__postAPI__(self.apiServiceTerritoriesURL, payloadTerritory, logFileName);

    def populateServices(self, csvFile):
        if self.consoleVerbose >= 1: print("Setup the Services")
        logFileName = self.__createLogFileName__('CreateServices')
        serviceSourceFile = self.filePath + 'Services/' + csvFile
        csvFileReader = csv.DictReader(open(serviceSourceFile))

        for row in csvFileReader:
            intFrequency = 0

            if str(row["Frequency"]) == 'One Time':
                intFrequency = 0
            if str(row["Frequency"]) == 'Weekly':
                intFrequency = 1
            if str(row["Frequency"]) == 'Monthly':
                intFrequency = 2
            if str(row["Frequency"]) == 'Quarterly':
                intFrequency = 3

            post_body_service = { \
                'Name': str(row["Name"]), \
                'Duration': int(row["Duration (Minutes)"]) * 60000, \
                'Frequency': intFrequency ,\
                'Price': int(row["Price"]),\
                }


            servicePayload = json.dumps(post_body_service)

            serviceResults = self.__postAPI__(self.apiServiceOfferingsURL, servicePayload, logFileName);




    def populateEmployees(self, csvFile):
        if self.consoleVerbose >= 1: print("Setup the Employees")
        employeeSourceFile = self.filePath + 'Employees/' + csvFile
        csvFileReader = csv.DictReader(open(employeeSourceFile))
        logFileName = self.__createLogFileName__('CreateEmployees')

        for row in csvFileReader:
            userIDfromResponse = ''
            post_body_admin = ''
            post_body_technician = ''

            post_body_user = { \
            'email': str(row["First Name"]) + str(row["Last Name"]) + self.emailDomain, \
            'name': str(row["First Name"]) + ' ' + str(row["Last Name"]), \
            'password': str(row["Password"]), \
            'tenantId': self.tenantID}

            userPayload = json.dumps(post_body_user)
            jsonResponseFromEmployee = self.__postAPI__(self.adminUsersURL, userPayload, logFileName)

            if str(row["Role"]) == 'Administrator':
                post_body_admin = {'userID': str(jsonResponseFromEmployee['id'])}

                adminPayload = json.dumps(post_body_admin)
                jsonResponseFromAdmin = self._callAPI_(self.adminTenantAdministratorsURL, adminPayload, logFileName)

            if str(row["Role"]) == 'Technician':
                post_body_technician = { \
                'callsign': str(row["CallSign"]), \
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
                    'longitude': float(row["StartingAddress.Longitude"]),\
                    },\
                'userID': str(jsonResponseFromEmployee['id'])}

                technicianPayload = json.dumps(post_body_technician)
                jsonResponseFromTechnician = self.__postAPI__(self.apiTechniciansURL, technicianPayload, logFileName);
    pass

    def populateTeams(self, csvFile):
        teamSourceFile = self.filePath + 'Teams/' + csvFile
        csvFileReader = csv.DictReader(open(teamSourceFile))
        logFileName = self.__createLogFileName__('CreateTeams')

        for row in csvFileReader:
            post_body_team = { \
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

            teamPayload = json.dumps(post_body_team)
            teamResults = self.__postAPI__(self.apiTeamsURL, teamPayload, logFileName);
        pass

#class createAccounts(odyssey):
    def createAccountsWithAgreements(self, csvFile, agreementsPerDay, delayBetweenAccountCreationinSeconds, AssertAgreements):
        accountSourceFile = self.filePath + 'Accounts/' + csvFile
        csvFileReader = csv.DictReader(open(accountSourceFile))
        today_date = datetime.date.today()
        initialCommitmentWindowStart = datetime.datetime.now()
        initialCommitmentWindowEnd = datetime.datetime.now()
        initialCommitmentWindowStart_iso = ''
        initialCommitmentWindowEnd_iso = ''
        countOfAgreements = 0
        logFileName = self.__createLogFileName__('CreateAccountsWithAgreements')

        requestServices = requests.get(self.apiServiceOfferingsURL, headers=self.headers)
        services = requestServices.json()


        for row in csvFileReader:
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
            accountResults = self.__postAPI__(self.apiAccountsURL, accountPayload, logFileName)

            initialCommitmentWindowStart_iso = initialCommitmentWindowStart.strftime("%Y-%m-%dT00:15:00")
            initialCommitmentWindowEnd_iso = initialCommitmentWindowEnd.strftime("%Y-%m-%dT23:45:00")

            todayDateFormatted = today_date.strftime("%Y-%m-%d")

            post_body_agreement = {
                "accountId" : str(accountResults['id']), \
                    "billingAddress" : { 'city': str(row["City"]), \
                          "country" : str(row["Country"]), \
                          "id" : str(accountResults['address']['id']),\
                          'latitude': str(row["Latitude"]), \
                          'lineOne': str(row["Address 1"]), \
                          "lineTwo" : "",\
                          'longitude': str(row["Longitude"]),\
                          'postalCode': str(row["Zip"]), \
                          'state': str(row["State"]), \
                    'stateAbbreviation': str(row["State Abbreviation"]) \
                        },\
                  "contact" : { "email" : "",\
                      "id" : str(accountResults['contact']['id']),\
                      "name" : str(accountResults['contact']['name']),\
                      "phone" : ""\
                    },\
                  "effectiveDate" : todayDateFormatted,\
                  "initialCommitmentTech" : "technicians/1",\
                  "initialCommitmentWindowEnd" : initialCommitmentWindowEnd_iso,\
                  "initialCommitmentWindowStart" : initialCommitmentWindowStart_iso,\
                  "invoiceSchedule" : 0,\
                  "issue" : "",\
                  "name" : str(row["Company Name"]),\
                  "preferredEndTime" : "23:59:59",\
                  "preferredStartTime" : "00:00:00",\
                  "serviceAddress" : { 'city': str(row["City"]), \
                      "country" : str(row["Country"]), \
                      "id" : str(accountResults['address']['id']), \
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

            agreementPayload = json.dumps(post_body_agreement)
            agreementResults = self.__postAPI__(self.apiAgreementsURL, agreementPayload, logFileName)


            countOfAgreements += 1

            if countOfAgreements >= agreementsPerDay:
                print ("Advancing Day")
                countOfAgreements = 0
                initialCommitmentWindowStart = initialCommitmentWindowStart + datetime.timedelta(days=1)
                initialCommitmentWindowEnd = initialCommitmentWindowEnd + datetime.timedelta(days=1)
            time.sleep(delayBetweenAccountCreationinSeconds)

            if AssertAgreements == True:
                self.logAgreementAssertion(self.tenantID, str(accountResults['id']), str(row["Company Name"]), str(initialCommitmentWindowStart.strftime("%Y-%m-%d")), self.dbServer, self.appServerName)

            if self.consoleVerbose >= 1: print('Count Of Agreements: ' + str(countOfAgreements) + '\n')
    pass

    def createAgreements(self, csvFile, agreementsPerDay , delayBetweenAccountCreationinSeconds, AssertAgreements):
            #accountSourceFile = self.filePath + 'Accounts/' + csvFile
            #csvFileReader = csv.DictReader(open(accountSourceFile))
            today_date = datetime.date.today()
            initialCommitmentWindowStart = datetime.datetime.now()
            initialCommitmentWindowEnd = datetime.datetime.now()
            initialCommitmentWindowStart_iso = ''
            initialCommitmentWindowEnd_iso = ''
            countOfAgreements = 0
            logFileName = self.__createLogFileName__('CreateAccountsWithAgreements')

            requestServices = requests.get(self.apiServiceOfferingsURL, headers=self.headers)
            services = requestServices.json()

            #get accounts list from the api
            accounts = self.getAccounts()
            #from account in accounts
                #get accountID
                #get addressID
                #get contactID
                #get contact Name

            for account in accounts:
        #             post_body_account = { \
        #                 'address': { \
        #                     'lineOne': str(row["Address 1"]), \
        #                     'city': str(row["City"]), \
        #                     'state': str(row["State"]), \
        #                     'stateAbbreviation': str(row["State Abbreviation"]), \
        #                     'postalCode': str(row["Zip"]), \
        #                     'country': str(row["Country"]), \
        #                     'latitude': str(row["Latitude"]), \
        #                     'longitude': str(row["Longitude"])\
        #                     }, \
        #                 'contact': { \
        #                     'name': str(row["Contact Name"]) \
        #                 },
        #                 'isNew': True, \
        #                 'name': str(row["Company Name"])\
        #             }
        #
        #             accountPayload = json.dumps(post_body_account)
        #             accountResults = self.__postAPI__(self.apiAccountsURL, accountPayload, logFileName)

                initialCommitmentWindowStart_iso = initialCommitmentWindowStart.strftime("%Y-%m-%dT00:15:00")
                initialCommitmentWindowEnd_iso = initialCommitmentWindowEnd.strftime("%Y-%m-%dT23:45:00")

                todayDateFormatted = today_date.strftime("%Y-%m-%d")

                post_body_agreement = {
                    "accountId" : str(accountResults['id']), \
                        "billingAddress" : { 'city': str(row["City"]), \
                              "country" : str(row["Country"]), \
                              "id" : str(accountResults['address']['id']),\
                              'latitude': str(row["Latitude"]), \
                              'lineOne': str(row["Address 1"]), \
                              "lineTwo" : "",\
                              'longitude': str(row["Longitude"]),\
                              'postalCode': str(row["Zip"]), \
                              'state': str(row["State"]), \
                        'stateAbbreviation': str(row["State Abbreviation"]) \
                            },\
                      "contact" : { "email" : "",\
                          "id" : str(accountResults['contact']['id']),\
                          "name" : str(accountResults['contact']['name']),\
                          "phone" : ""\
                        },\
                      "effectiveDate" : todayDateFormatted,\
                      "initialCommitmentTech" : "technicians/1",\
                      "initialCommitmentWindowEnd" : initialCommitmentWindowEnd_iso,\
                      "initialCommitmentWindowStart" : initialCommitmentWindowStart_iso,\
                      "invoiceSchedule" : 0,\
                      "issue" : "",\
                      "name" : str(row["Company Name"]),\
                      "preferredEndTime" : "23:59:59",\
                      "preferredStartTime" : "00:00:00",\
                      "serviceAddress" : { 'city': str(row["City"]), \
                          "country" : str(row["Country"]), \
                          "id" : str(accountResults['address']['id']), \
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

                agreementPayload = json.dumps(post_body_agreement)
                agreementResults = self.__postAPI__(self.apiAgreementsURL, agreementPayload, logFileName)


                countOfAgreements += 1

                if countOfAgreements >= agreementsPerDay:
                    print ("Advancing Day")
                    countOfAgreements = 0
                    initialCommitmentWindowStart = initialCommitmentWindowStart + datetime.timedelta(days=1)
                    initialCommitmentWindowEnd = initialCommitmentWindowEnd + datetime.timedelta(days=1)
                time.sleep(delayBetweenAccountCreationinSeconds)

                if AssertAgreements == True:
                    self.logAgreementAssertion(self.tenantID, str(accountResults['id']), str(row["Company Name"]), str(initialCommitmentWindowStart.strftime("%Y-%m-%d")), self.dbServer, self.appServerName)

                if self.consoleVerbose  >= 1: print('Count Of Agreements: ' + str(countOfAgreements) + '\n')


    def __createAccounts__(self, csvFile):
        accountSourceFile = self.filePath + 'Accounts/' + csvFile
        csvFileReader = csv.DictReader(open(accountSourceFile))
        logFileName = self.__createLogFileName__('CreateAccounts')

        for row in csvFileReader:
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

            accountResults = self.__postAPI__(self.apiAccountsURL, accountPayload, logFileName)


    pass

    def logAgreementAssertion(self, tenant, accountId, accountName, serviceDate, dbServer, apiServer):
        assertionLogFilePath = self.filePath + 'Assertions/Agreements_' + str(datetime.datetime.now().strftime("%Y%m%d")) + '.csv'
        log_output = tenant + ',' + accountId + ',' + accountName + ',' + serviceDate + ',' + dbServer + ','+ apiServer + '\n'
        if os.path.exists(assertionLogFilePath) == False:
            assertionLogFile = open(assertionLogFilePath, 'a')
            assertionLogFile.write('Tenant,AccountID,AccountName,ServiceDate,DatabaseServer,apiServer\n')
            assertionLogFile.close()
        try:
            assertionLogFile = open(assertionLogFilePath, 'a')
        except:
            print("Failed to open to assertion log file")
        try:
            assertionLogFile.write(log_output)
        except:
            print("Failed to write to assertion log file")
        if self.consoleVerbose >= 2: print('Logging assertion: ' + log_output)


# def main():
#     newTenantGenerator = odysseyTenantGenerator()
#     newTenantGenerator.validateTenantsImportFile('tim.csv')
#     newTenantGenerator.importTenantsFromCSV('tim.csv')
#     pass
#
# if __name__ == '__main__':
#     main()

    def getDBID(self):


        response = requests.get(self.dbServerURL)
        if response.status_code > 204:
            print("Network Error reaching " + self.dbServerURL + " Status Code = " + str(response.status_code))
            sys.exit("Error reaching " + self.dbServerURL + " Status Code = " + str(response.status_code))

        #get dbid
        apiCall = "/databases/SystemAdministration/indexes/Auto/IdentityUsers/ByUserName"
        url = self.dbServerURL + apiCall
        params = "query=UserName:" + self.tenantAdminEmail
        response = requests.get(url, params = params)
        self.results = response.json()
        self.tenantID = str(self.results["Results"][0]["Claims"][0]["ClaimValue"])

    def processHarFile(self):

        #set creating tenants to false

        #get the list of files in filepath
        listofFiles = os.listdir(self.filePath)

        for fname in listofFiles:
            pathParts = os.path.splitext(fname)
            ext = pathParts[1]
            rep_file = pathParts[0]
            if ext == '.har':


                # open the extract file for p:rocessing
                #inputFile = open(self.filePath + fname, 'r')
                har = json.loads(open(self.filePath + fname).read())
                outputFilename = self.filePath + fname + "_results.txt" #add date code to this file
                outputFile = open(outputFilename, 'w')
                #sys.stdout.write(fname + '\n')
                for i in range(len(har["log"]["entries"])):
                    if har["log"]["entries"][i]["request"]["method"] == "GET":
                        line = har["log"]["entries"][i]["request"]["url"]
                        if "http://" + self.appServerName + ":" + self.appServerAPIPort in line:
                        #check if the line is a valid execution
                            #line = line.split()[1]
                            line = line.strip('\"')
                            apiCall = line.strip('\,\"')
                            print(apiCall)
                            params = {}
                            results = self.__getAPI__(apiCall, params)
                            print(results["statusCode"])
                            print(re.sub('.{8}-.{4}-.{4}-.{4}-.{12}', "0000-0000-0000", results["content"]))


                        #write the results to the file

                        # = line + '\n'
                        #outputFile.write(output)
                #sys.stdout.write(fname)



                #close the input and output files
                inputFile.close()
                outputFile.close()



    def getOdysseyAdminAuthToken(self, email, password):
        postHeaders = {}
        postPayload = "grant_type=password&username=" + email + "&password=" + password + "&scope=marathon_admin"
        response = requests.post(self.sysAdminTokenURL, postPayload, headers=postHeaders)
        try:
            accessToken = str(response.json()["access_token"])
        except:
            accessToken = ""
        fullAccessToken = "Bearer " + accessToken

        return(fullAccessToken);


##        headers = {'content-type': 'application/json', 'Authorization' : (odysseyTenant.getAuthorizationToken(self, self.AdminEmail))}
##            logFileName = self.createLogFileName('CreateAccountsWithAgreements')
##
##            initialCommitmentWindowStart = initialCommitmentWindowStart + datetime.timedelta(days=1)
##            initialCommitmentWindowEnd = initialCommitmentWindowEnd + datetime.timedelta(days=1)
##
##            requestServices = requests.get(self.apiServiceOfferingsURL, headers=headers)


    def checkForEmailInSystem(self, email):
        isDuplicated = True
        #adminToken = getOdysseyAdminAuthToken(self.sysAdminEmail, self.sysAdminPassword)

        try:
            ravenDBResult = str(self.results["Results"][0]["UserName"]).lower()
        except:
            ravenDBResult = False

        if ravenDBResult == email.lower():
            print ('A user with the email ' + email + ' already exists in the Odyssey system. \n')
            isDuplicated = True
        else:
            print('Email address is unique')
            isDuplicated = False
        return isDuplicated

