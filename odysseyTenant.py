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

class odysseyTenant:
    AdminEmail = 'tim13@mds.mds'
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
        if env.lower() == 'localhost':
            self.serverURL = 'localhost'
            self.serverAdminPort = '86'
            self.serverAPIport = '85'
        self.apiTokenURL = 'http://' + self.serverURL + ':' + self.serverAPIport + '/api/token'
        self.adminTokenURL = 'http://' + self.serverURL + ':' + self.serverAdminPort + '/administration/token'
        self.adminTenantsURL = 'http://' + self.serverURL + ':' + self.serverAdminPort + '/administration/tenants'
        self.apiAccountsURL = 'http://' + self.serverURL + ':' + self.serverAPIport + '/api/accounts'
        self.apiAgreementsURL = 'http://' + self.serverURL + ':' + self.serverAPIport + '/api/serviceAgreements'
        self.apiServiceofferingsURL = 'http://' + self.serverURL + ':' + self.serverAPIport + '/api/serviceofferings'
    pass

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
        accessToken = str(response.json()["access_token"])
        fullAccessToken = "Bearer " + accessToken

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


class odysseyAccounts(odysseyTenant):
    def populateAccountsWithAgreementsFromCSV(self, csvFilePath, agreementsPerDay, delayBetweenAccountCreationinSeconds):
        csvFileReader = csv.DictReader(open(csvFilePath))
        today_date = datetime.date.today()
        initialCommitmentWindowStart = datetime.datetime.now()
        initialCommitmentWindowEnd = datetime.datetime.now()
        initialCommitmentWindowStart_iso = ''
        initialCommitmentWindowEnd_iso = ''
        countOfAgreements = 0
        headers = {'content-type': 'application/json', 'Authorization' : (odysseyTenant.getAuthorizationToken(self, self.AdminEmail))}
        logFileName = self.createLogFileName('CreateAccountsWithAgreements')

        requestServices = requests.get(self.apiServiceofferingsURL, headers=headers)
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

            print ('Count Of Agreements: ' + str(countOfAgreements) + '\n')

    pass

    def populateAccountsFromCSV(self, csvFilePath):
            csvFileReader = csv.DictReader(open(csvFilePath))
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




def main():
    timAccounts = odysseyAccounts()
    timAccounts.setEnvironmentURLs("QA")
    timAccounts.AdminEmail = 'tim12@mds.mds'
    #timAccounts.populateAccountsFromCSV('//mds-fs01/pitcrew/api_testing/Accounts/B_Accounts.csv')
    #timAccounts.callAPIreturningJSON('url', 'payload', 'Blah')
    #timAccounts.createLogFileName('BLAH')
    pass

if __name__ == '__main__':
    main()


