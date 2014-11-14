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

class odysseyTenantGenerator:
    sourceFilePath = '//mds-fs01/pitcrew/api_testing/'
    def validateTenantsImportFile(self, csvFileName):
        tenantSourceFile = self.sourceFilePath + 'tenants/' + csvFileName

        if os.path.exists(tenantSourceFile) == False:
            print('Source file does not exist - quitting')
            sys.exit()
        else:
            print('Source File Found')

        csvFileValidator = csv.DictReader(open(tenantSourceFile))

        for row in csvFileValidator:
            print('Validating source file...')
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
                accountswithAgreements = str(row["AccountswithAgreements"])
            except:
                print('Source file incomplete, check all rows against format of template.csv')
                sys.exit()

            if os.path.exists(self.sourceFilePath + 'companyhours/' + companyHoursFile) == True:
                print('Company hours file exists for: ' + companyName)
            else:
                print('Company hours file does not exist for: ' + companyName)
                print('Qutting script')
                sys.exit()


            if os.path.exists(self.sourceFilePath + 'holidays/' + companyHolidaysFile) == True:
                print('Company holidays file exists for: ' + companyName)
            else:
                print('Company holidays file does not exist for: ' + companyName)
                print('Qutting script')
                sys.exit()

            if os.path.exists(self.sourceFilePath + 'territories/' + companyTerritory) == True:
                print('Company territory file exists for: ' + companyName)
            else:
                print('Company territory file does not exist for: ' + companyName)
                print('Qutting script')
                sys.exit()

            if os.path.exists(self.sourceFilePath + 'employees/' + employeesList) == True:
                print('Company employee file exists for: ' + companyName)
            else:
                print('Company employee file does not exist for: ' + companyName)
                print('Qutting script')
                sys.exit()

            if os.path.exists(self.sourceFilePath + 'services/' + servicesList) == True:
                print('Company services file exists for: ' + companyName)
            else:
                print('Company services file does not exist for: ' + companyName)
                print('Qutting script')
                sys.exit()

            if os.path.exists(self.sourceFilePath + 'teams/' + teamsList) == True:
                print('Company teams file exists for: ' + companyName)
            else:
                print('Company teams file does not exist for: ' + companyName)
                print('Qutting script')
                sys.exit()

            if accountsList == 'None':
                print('No accounts-only file to import, step will be skipped')
            else:
                if os.path.exists(self.sourceFilePath + 'accounts/' + accountsList) == True:
                    print('Company accounts file exists for: ' + companyName)
                else:
                    print('Company accounts file does not exist for: ' + companyName)
                    print('Qutting script')
                    sys.exit()

            if accountswithAgreements == 'None':
                print('No accounts with agreements file to import, step will be skipped')
            else:
                if os.path.exists(self.sourceFilePath + 'accounts/' + accountswithAgreements) == True:
                    print('Company accounts with agreements file exists for: ' + companyName)
                else:
                    print('Company accounts with agreements file does not exist for: ' + companyName)
                    print('Qutting script')
                    sys.exit()
            print('Import file is valid')


class odysseyAdmin:
    Username = 'admin@marathondata.com'
    Password = 'letmein123'
    logFilePathAdmin = "//mds-fs01/pitcrew/api_testing/Logs/Administration/"

    def setAdminEnvironmentURLs(self, env):
        if env.lower() == 'qa':
            self.serverURL = 'ngp-qa-web'
            self.serverAdminPort = '86'
            self.serverAPIport = '85'
        if env.lower() == 'localhost':
            self.serverURL = 'localhost'
            self.serverAdminPort = '86'
            self.serverAPIport = '85'
        self.adminTokenURL = 'http://' + self.serverURL + ':' + self.serverAdminPort + '/administration/token'
        self.adminTenantsURL = 'http://' + self.serverURL + ':' + self.serverAdminPort + '/administration/tenants'
        self.adminSchedulingLicensingURL = 'http://' + self.serverURL + ':' + self.serverAdminPort + '/administration/schedulinglicensing/'

    def createTenant(self, tenantAdminName, CompanyName, tenantAdminEmail, LicenseCount, wordOrderNSeedumber, invoiceNumberSeed):
        headers = {'content-type': 'application/json', 'Authorization' : (odysseyAdmin.getAdminAuthorizationToken(self, self.Username))}
        logFileName = self.createAdminLogFileName()

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

        tenantPayload = json.dumps(post_body_tenant)
        jsonResponseFromTenant = odysseyAdmin.callAdminAPIreturningJSON(self, self.adminTenantsURL, headers, tenantPayload, logFileName)

        post_body_scheduling = { \
            'id': '00000000-0000-0000-0000-000000000000', \
            'voloAPIKey': 'ODYS-SEYO-DYSS-EYOD', \
            'schedulingType': 1
            }

        schedulingPayload = json.dumps(post_body_scheduling)
        schedulingLicensingFullURL = self.adminSchedulingLicensingURL + str(jsonResponseFromTenant['id'])
        jsonResponseFromSchedulingConfig = odysseyAdmin.callAdminAPIreturningJSON(self, schedulingLicensingFullURL, headers, schedulingPayload, logFileName)

    def createAdminLogFileName(self):
        i = datetime.datetime.now()
        dt = i.strftime('%Y%m%d-%H%M%S')
        logFileCalc = 'Administration' + "_" + dt + ".tsv"
        fullLogFileName = odysseyAdmin.logFilePathAdmin + logFileCalc

        return fullLogFileName

    def getAdminAuthorizationToken(self, email):
        postHeaders = {}
        postPayload = "grant_type=password&username=" + email + "&password=letmein123&scope=marathon_admin"
        response = requests.post(self.adminTokenURL, postPayload, headers=postHeaders)
        accessToken = str(response.json()["access_token"])
        fullAccessToken = "Bearer " + accessToken

        return(fullAccessToken);

    def callAdminAPIreturningJSON(self, url, headers, payload, logFileName):
        jsonResponse = ''

        output = requests.post(url, payload, headers=headers)

        if output.status_code == 401:
            return (401)
        if output.status_code == 200:
            jsonResponse = output.json()
            id = jsonResponse["id"].encode("ascii")
        else:
            id = output.content

        log_output = url + "\t" + str(output.status_code) +  "\t" + str(output.elapsed) + "\t" + str(payload) + "\t" + id  + '\n'
        try:
            logFile = open(logFileName, 'a')
        except:
            print("Failed to open to log file")
        try:
            logFile.write(log_output)
        except:
            print("Failed to write to log file")
        print ('Logging API post: ' + log_output)

        return(jsonResponse);

class odysseyTenant:
    AdminEmail = ''
    emailDomain = ''
    CompanyName = ''
    LicenseCount = 0
    TenantName = ''
    StartingWorkNumber = 0
    StartingInvoiceNumber = 0
    SchedulingType = 1         # 0 = Manual, 1 = Automatic
    tenantID = ''

    logFilePath = "//mds-fs01/pitcrew/api_testing/Logs/"
    sourceFilePath = "//mds-fs01/pitcrew/api_testing/"

    def setEnvironmentURLs(self, env):
        if env.lower() == 'qa':
            self.serverURL = 'ngp-qa-web'
            self.serverAdminPort = '86'
            self.serverAPIport = '85'
            self.dbServer = 'ngp-qa-db'
        if env.lower() == 'localhost':
            self.serverURL = 'localhost'
            self.serverAdminPort = '86'
            self.serverAPIport = '85'
            self.dbServer = 'localhost'
        self.apiTokenURL = 'http://' + self.serverURL + ':' + self.serverAPIport + '/api/token'
        self.adminTokenURL = 'http://' + self.serverURL + ':' + self.serverAdminPort + '/administration/token'
        self.adminTenantsURL = 'http://' + self.serverURL + ':' + self.serverAdminPort + '/administration/tenants'
        self.apiAccountsURL = 'http://' + self.serverURL + ':' + self.serverAPIport + '/api/accounts'
        self.apiAgreementsURL = 'http://' + self.serverURL + ':' + self.serverAPIport + '/api/serviceAgreements'
        self.apiServiceOfferingsURL = 'http://' + self.serverURL + ':' + self.serverAPIport + '/api/serviceofferings'
        self.apiServiceHoursURL = 'http://' + self.serverURL + ':' + self.serverAPIport + '/api/serviceHours'
        self.apiCompanyHolidsaysURL = 'http://' + self.serverURL + ':' + self.serverAPIport + '/api/companyHolidays'
        self.apiServiceTerritoriesURL = 'http://' + self.serverURL + ':' + self.serverAPIport + '/api/serviceTerritories'
        self.adminUsersURL = 'http://' + self.serverURL + ':' + self.serverAdminPort + '/administration/users'
        self.adminTenantAdministratorsURL = 'http://' + self.serverURL + ':' + self.serverAdminPort + '/administration/tenantadministrator'
        self.apiTechniciansURL = 'http://' + self.serverURL + ':' + self.serverAPIport + '/api/technicians'
        self.apiTeamsURL = 'http://' + self.serverURL + ':' + self.serverAPIport + '/api/teams'
    pass

    def setAdminAndTenantID(self, email):
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

    def createLogFileName(self, functionCalling):
        i = datetime.datetime.now()
        dt = i.strftime('%Y%m%d-%H%M%S')
        logFolderName = self.AdminEmail
        logFolderName = logFolderName.replace('@', '_')
        logFolderName = logFolderName.replace('-', '_')
        logFolderName = logFolderName.replace('.', '_')
        if os.path.exists(odysseyTenant.logFilePath + logFolderName) == False:
            os.mkdir(odysseyTenant.logFilePath + logFolderName)
        logFileCalc = functionCalling + "_" + dt + ".tsv"
        fullLogFileName = odysseyTenant.logFilePath + logFolderName + '/' + logFileCalc

        return fullLogFileName

    def getAuthorizationToken(self, email):
        postHeaders = {}
        postPayload = "grant_type=password&username=" + email + "&password=letmein123&scope=marathon_odyssey"
        response = requests.post(self.apiTokenURL, postPayload, headers=postHeaders)
        try:
            accessToken = str(response.json()["access_token"])
            fullAccessToken = "Bearer " + accessToken
        except:
            fullAccessToken = ''
        return(fullAccessToken);

    def callAPIreturningJSON(self, url, headers, payload, logFileName):
        jsonResponse = ''

        output = requests.post(url, payload, headers=headers)

        if output.status_code == 401:
            return (401)
        if output.status_code == 200:
            jsonResponse = output.json()
            id = jsonResponse["id"].encode("ascii")
        else:
            id = output.content

        log_output = url + "\t" + str(output.status_code) +  "\t" + str(output.elapsed) + "\t" + str(payload) + "\t" + id  + '\n'
        try:
            logFile = open(logFileName, 'a')
        except:
            print("Failed to open to log file")
        try:
            logFile.write(log_output)
        except:
            print("Failed to write to log file")
        print ('Logging API post: ' + log_output)

        return(jsonResponse);

    def setCompanyHours(self, companyHoursInJSON):
        headers = {'content-type': 'application/json', 'Authorization' : (odysseyTenant.getAuthorizationToken(self, self.AdminEmail))}
        logFileName = self.createLogFileName('setCompanyHours')
        companyHoursSourceFile = self.sourceFilePath + 'CompanyHours/' + companyHoursInJSON
        jsonCompanyHours = open(companyHoursSourceFile, 'rb')
        payloadCompanyHours = jsonCompanyHours.read()

        jsonResponseFromCompanySchedule = odysseyTenant.callAPIreturningJSON(self, self.apiServiceHoursURL, headers, payloadCompanyHours, logFileName)
    pass


    def setCompanyHolidays(self, companyHolidsaysInJSON):
        headers = {'content-type': 'application/json', 'Authorization' : (odysseyTenant.getAuthorizationToken(self, self.AdminEmail))}
        logFileName = self.createLogFileName('setHolidays')
        holidaysSourceFile = self.sourceFilePath + 'Holidays/' + companyHolidsaysInJSON
        jsonHolidays = open(holidaysSourceFile, 'rb')
        payloadHolidays = jsonHolidays.read()

        jsonResponseFromCompanyHolidays = odysseyTenant.callAPIreturningJSON(self, self.apiCompanyHolidsaysURL, headers, payloadHolidays, logFileName)
    pass


    def setCompanyTerritory(self, companyTerritoryInJSON):
            headers = {'content-type': 'application/json', 'Authorization' : (odysseyTenant.getAuthorizationToken(self, self.AdminEmail))}
            logFileName = self.createLogFileName('setTerritory')
            territorySourceFile = self.sourceFilePath + 'Territories/' + companyTerritoryInJSON
            jsonTerritory = open(territorySourceFile, 'rb')
            payloadTerritory = jsonTerritory.read()

            jsonResponseFromCompanyHolidaysd = odysseyTenant.callAPIreturningJSON(self, self.apiServiceTerritoriesURL, headers, payloadTerritory, logFileName)
    pass

    def populateServicesFromCSV(self, csvFile):
            headers = {'content-type': 'application/json', 'Authorization' : (odysseyTenant.getAuthorizationToken(self, self.AdminEmail))}
            logFileName = self.createLogFileName('CreateServices')
            serviceSourceFile = self.sourceFilePath + 'Services/' + csvFile
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

                jsonResponseFromService = odysseyTenant.callAPIreturningJSON(self, self.apiServiceOfferingsURL, headers, servicePayload, logFileName)

                if jsonResponseFromService == 401:
                    headers = {'content-type': 'application/json', 'Authorization' : (odysseyTenant.getAuthorizationToken(self, self.AdminEmail))}
                    jsonResponseFromService = odysseyTenant.callAPIreturningJSON(self, self.apiServiceOfferingsURL, headers, servicePayload, logFileName)
    pass

    def populateEmployeesFromCSV(self, csvFile):
        employeeSourceFile = self.sourceFilePath + 'Employees/' + csvFile
        csvFileReader = csv.DictReader(open(employeeSourceFile))
        headers = {'content-type': 'application/json', 'Authorization' : (odysseyTenant.getAuthorizationToken(self, self.AdminEmail))}
        logFileName = self.createLogFileName('CreateEmployees')

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
            jsonResponseFromEmployee = odysseyTenant.callAPIreturningJSON(self, self.adminUsersURL, headers, userPayload, logFileName)

            if str(row["Role"]) == 'Administrator':
                post_body_admin = {'userID': str(jsonResponseFromEmployee['id'])}

                adminPayload = json.dumps(post_body_admin)
                jsonResponseFromAdmin = odysseyTenant.callAPIreturningJSON(self, self.adminTenantAdministratorsURL, headers, adminPayload, logFileName)

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
                jsonResponseFromTechnician = odysseyTenant.callAPIreturningJSON(self, self.apiTechniciansURL, headers, technicianPayload, logFileName)
    pass

    def populateTeamsFromCSV(self, csvFile):
        teamSourceFile = self.sourceFilePath + 'Teams/' + csvFile
        csvFileReader = csv.DictReader(open(teamSourceFile))
        headers = {'content-type': 'application/json', 'Authorization' : (odysseyTenant.getAuthorizationToken(self, self.AdminEmail))}
        logFileName = self.createLogFileName('CreateTeams')

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
            jsonResponseFromTeam = odysseyTenant.callAPIreturningJSON(self, self.apiTeamsURL, headers, teamPayload, logFileName)
        pass

class odysseyAccounts(odysseyTenant):
    def populateAccountsWithAgreementsFromCSV(self, csvFile, agreementsPerDay, delayBetweenAccountCreationinSeconds, AssertAgreements):
        accountSourceFile = self.sourceFilePath + 'Accounts/' + csvFile
        csvFileReader = csv.DictReader(open(accountSourceFile))
        today_date = datetime.date.today()
        initialCommitmentWindowStart = datetime.datetime.now()
        initialCommitmentWindowEnd = datetime.datetime.now()
        initialCommitmentWindowStart_iso = ''
        initialCommitmentWindowEnd_iso = ''
        countOfAgreements = 0
        headers = {'content-type': 'application/json', 'Authorization' : (odysseyTenant.getAuthorizationToken(self, self.AdminEmail))}
        logFileName = self.createLogFileName('CreateAccountsWithAgreements')

        requestServices = requests.get(self.apiServiceOfferingsURL, headers=headers)
        services = requestServices.json()

        print self.AdminEmail

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
            jsonResponseFromAccount = odysseyTenant.callAPIreturningJSON(self, self.apiAccountsURL, headers, accountPayload, logFileName)

            if jsonResponseFromAccount == 401:
                headers = {'content-type': 'application/json', 'Authorization' : (odysseyTenant.getAuthorizationToken(self, self.AdminEmail))}
                jsonResponseFromAccount = odysseyTenant.callAPIreturningJSON(self, self.apiAccountsURL, headers, accountPayload, logFileName)

            initialCommitmentWindowStart_iso = initialCommitmentWindowStart.strftime("%Y-%m-%dT00:15:00")
            initialCommitmentWindowEnd_iso = initialCommitmentWindowEnd.strftime("%Y-%m-%dT23:45:00")

            todayDateFormatted = today_date.strftime("%Y-%m-%d")

            post_body_agreement = {
                "accountId" : str(jsonResponseFromAccount['id']), \
                    "billingAddress" : { 'city': str(row["City"]), \
                          "country" : str(row["Country"]), \
                          "id" : str(jsonResponseFromAccount['address']['id']),\
                          'latitude': str(row["Latitude"]), \
                          'lineOne': str(row["Address 1"]), \
                          "lineTwo" : "",\
                          'longitude': str(row["Longitude"]),\
                          'postalCode': str(row["Zip"]), \
                          'state': str(row["State"]), \
                    'stateAbbreviation': str(row["State Abbreviation"]) \
                        },\
                  "contact" : { "email" : "",\
                      "id" : str(jsonResponseFromAccount['contact']['id']),\
                      "name" : str(jsonResponseFromAccount['contact']['name']),\
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
                      "id" : str(jsonResponseFromAccount['address']['id']), \
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
            jsonResponseFromAgreement = odysseyTenant.callAPIreturningJSON(self, self.apiAgreementsURL, headers, agreementPayload, logFileName)

            if jsonResponseFromAgreement == 401:
                headers = {'content-type': 'application/json', 'Authorization' : (odysseyTenant.getAuthorizationToken(self, self.AdminEmail))}
                jsonResponseFromAgreement = odysseyTenant.callAPIreturningJSON(self, self.apiAccountsURL, headers, accountPayload, logFileName)

            countOfAgreements += 1

            if countOfAgreements >= agreementsPerDay:
                print ("Advancing Day")
                countOfAgreements = 0
                initialCommitmentWindowStart = initialCommitmentWindowStart + datetime.timedelta(days=1)
                initialCommitmentWindowEnd = initialCommitmentWindowEnd + datetime.timedelta(days=1)
            time.sleep(delayBetweenAccountCreationinSeconds)

            if AssertAgreements == True:
                self.logAgreementAssertion(self.tenantID, str(jsonResponseFromAccount['id']), str(row["Company Name"]), str(initialCommitmentWindowStart.strftime("%Y-%m-%d")), self.dbServer, self.serverURL)

            print ('Count Of Agreements: ' + str(countOfAgreements) + '\n')
    pass

    def populateAccountsFromCSV(self, csvFile):
            accountSourceFile = self.sourceFilePath + 'Accounts/' + csvFile
            csvFileReader = csv.DictReader(open(accountSourceFile))
            headers = {'content-type': 'application/json', 'Authorization' : (odysseyTenant.getAuthorizationToken(self, self.AdminEmail))}
            logFileName = self.createLogFileName('CreateAccounts')

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

                jsonResponseFromAccount = odysseyTenant.callAPIreturningJSON(self, self.apiAccountsURL, headers, accountPayload, logFileName)

                if jsonResponseFromAccount == 401:
                    headers = {'content-type': 'application/json', 'Authorization' : (odysseyTenant.getAuthorizationToken(self, self.AdminEmail))}
                    jsonResponseFromAccount = odysseyTenant.callAPIreturningJSON(self, self.apiAccountsURL, headers, accountPayload, logFileName)
    pass

    def logAgreementAssertion(self, tenant, accountId, accountName, serviceDate, dbServer, apiServer):
        assertionLogFilePath = self.sourceFilePath + 'Assertions/Agreements_' + str(datetime.datetime.now().strftime("%Y%m%d")) + '.csv'
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
        print ('Logging assertion: ' + log_output)


def main():
##    timGenerator = odysseyTenantGenerator()
##    timGenerator.validateTenantsImportFile('tim.csv')
##    timAdmin = odysseyAdmin()
##    timAdmin.setAdminEnvironmentURLs('QA')
##    timAdmin.createTenant('StayinFront Inc', 'StayinFront Inc', 'tbuck@sif4.sif', 5, 1000, 1000)
    timAccounts = odysseyAccounts()
    timAccounts.setEnvironmentURLs("QA")
    while len(str(timAccounts.getAuthorizationToken('tbuck@sif4.sif'))) <= 100:
        print ('Unable to authenticate user, waiting 5 seconds')
        time.sleep(5)
    timAccounts.setAdminAndTenantID('tbuck@sif4.sif')
##    timAccounts.emailDomain = '@sif4.sif'
##    timAccounts.setCompanyHours('hours_EST_9-5_S-S_60minBreak.json')
##    timAccounts.setCompanyHolidays('holidays_Static_Holidays.json')
##    timAccounts.setCompanyTerritory('territories_NJ_Only.json')
##    timAccounts.populateEmployeesFromCSV('template.csv')
##    timAccounts.populateServicesFromCSV('services_Basic-One_Of_Each.csv')
##    timAccounts.populateTeamsFromCSV('teams_A-Team.csv')
    timAccounts.populateAccountsWithAgreementsFromCSV('KearnyJerseyCity.csv', 10, 1, True)
    pass

if __name__ == '__main__':
    main()


