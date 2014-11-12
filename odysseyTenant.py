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

import requests

class odysseyTenant:
    AdminEmail = ''
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
            odysseyTenant.serverURL = 'ngp-qa-web'
            odysseyTenant.serverAdminPort = '86'
            odysseyTenant.serverAPIport = '85'
        if env.lower() == 'localhost':
            odysseyTenant.serverURL = 'localhost'
            odysseyTenant.serverAdminPort = '86'
            odysseyTenant.serverAPIport = '85'
        odysseyTenant.APItokenURL = 'http://' + odysseyTenant.serverURL + ':' + odysseyTenant.serverAPIport + '/api/token'
        odysseyTenant.AdminTokenURL = 'http://' + odysseyTenant.serverURL + ':' + odysseyTenant.serverAdminPort + '/administration/token'
        odysseyTenant.AdminTenantsURL = 'http://' + odysseyTenant.serverURL + ':' + odysseyTenant.serverAdminPort + '/administration/tenants'
        odysseyTenant.APIaccountsURL = 'http://' + odysseyTenant.serverURL + ':' + odysseyTenant.serverAPIport + '/api/accounts'
        odysseyTenant.APIagreementsURL = 'http://' + odysseyTenant.serverURL + ':' + odysseyTenant.serverAPIport + '/api/serviceAgreements'
        odysseyTenant.APIserviceofferingsURL = 'http://' + odysseyTenant.serverURL + ':' + odysseyTenant.serverAPIport + '/api/serviceofferings'
    pass

    def getAuthorizationToken(self, email):
        postHeaders = {}
        postPayload = "grant_type=password&username=" + email + "&password=letmein123&scope=marathon_odyssey"
        response = requests.post(odysseyTenant.APItokenURL, postPayload, headers=postHeaders)
        accessToken = str(response.json()["access_token"])
        fullAccessToken = "Bearer " + accessToken
        return(fullAccessToken);

##    def callAPIreturningJSON(url, headers, payload, logFileName):
##        s = ''
##        output = requests.post(url, payload, headers=headers)
##
##        if output.status_code == 401:
##
##
##        if output.status_code == 200:
##            s = output.json()
##            id = s["id"].encode("ascii")
##        else:
##        #log that the post fileinput
##            #sys.stdout.write(output.content)
##            id = output.content
##
##        #log the results
##        #log_output = url + "," + str(output.status_code) +  "," + str(output.elapsed) + "," payload + "," + id  + '\n'
##        log_output = url + "\t" + str(output.status_code) +  "\t" + str(output.elapsed) + "\t" + str(payload) + "\t" + id  + '\n'
##        logFile = open(logFileName, 'a')
##        #sys.stdout.write(output)
##
##        #output the line to the output file
##        try:
##            logFile.write(log_output)
##        except:
##            print("Failed to write to log file")
##        print ('Logging API post: ' + log_output)
##        return(s);


class odysseySchedule(odysseyTenant):

    pass

def main():
    timTenant = odysseyTenant()
    timTenant.setEnvironmentURLs("QA")
    print (timTenant.APIserviceofferingsURL)
    print (timTenant.getAuthorizationToken('tim@mds.mds'))
    pass

if __name__ == '__main__':
    main()


