#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      tdembowski
#
# Created:     10/11/2014
# Copyright:   (c) tdembowski 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import csv
import sys
import json
import requests
import time
import datetime
import dateutil.parser

accountImportFile = "C:/Users/tdembowski/Desktop/API Testing/Accounts/KearnyJerseyCity.csv"
url_base = "http://ngp-qa-web"
logFileName = 'C:/Users/tdembowski/Desktop/API Testing/Logs/Test.txt'

def main(argv):

    email = sys.argv[1]
    token = authorize(email)
    headers = {'content-type': 'application/json', 'Authorization' : token}
    AccountsURL = 'http://ngp-qa-web:85/api/accounts'
    AgreementsURL = 'http://ngp-qa-web:85/api/serviceAgreements'
    ServicesURL = 'http://ngp-qa-web:85/api/serviceofferings'


    createAccountsAndAgreementsfromCSV(accountImportFile, AccountsURL, AgreementsURL, ServicesURL, headers, logFileName)

    pass


def createAccountsAndAgreementsfromCSV(csvFilePath, AccountsURL, AgreementsURL, ServicesURL, headers, logFileName):
    csvFileReader = csv.DictReader(open(csvFilePath))
    today_date = datetime.date.today()
    initialCommitmentWindowStart = datetime.datetime.now()
    initialCommitmentWindowEnd = datetime.datetime.now()
    initialCommitmentWindowStart_iso = ''
    initialCommitmentWindowEnd_iso = ''

    requestServices = requests.get(ServicesURL, headers=headers)
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

        try:
            output = callAPIreturningJSON(AccountsURL, headers, accountPayload, logFileName)
            print output
        except:
            print ('Something bad happened psting to the accounts API.')

        initialCommitmentWindowStart = initialCommitmentWindowStart + datetime.timedelta(0,1800)
        initialCommitmentWindowEnd = initialCommitmentWindowStart + datetime.timedelta(0,9000)

        initialCommitmentWindowStart_iso = initialCommitmentWindowStart.strftime("%Y-%m-%dT%H:%M:%S")
        initialCommitmentWindowEnd_iso = initialCommitmentWindowEnd.strftime("%Y-%m-%dT%H:%M:%S")

        todayDateFormatted = today_date.strftime("%Y-%m-%d")

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

        agreementPayload = json.dumps(post_body_agreement)

        try:
            output2 = callAPIreturningJSON(AgreementsURL, headers, agreementPayload, logFileName)
            print output2
        except:
            print ('Something bad happened psting to the agreements API.')

        initialCommitmentWindowStart = initialCommitmentWindowStart + datetime.timedelta(0,3600)

        time.sleep(30)


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

def callAPIreturningJSON(url, headers, payload, logFileName):
    output = requests.post(url, payload, headers=headers)
    s = ''
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
    return(s);

if __name__ == "__main__":
    main(sys.argv)

