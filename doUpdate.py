#/usr/bin/python
# File:   affiliations/doUpdate.py
# Author: Michael Cummings, Assistant Museam Libarian, Systems and Information Technology 
#         Thomas J. Watson Libary, The Metropolitan Museam of Art
# Editor: Halima Rahman, Intern
# Gist:   for each line, updates the patron, creating a varfield d with
#         affiliation and nulling out the varfield p
# Usage:  $python doUpdate.py
import json
import requests
import base64
from requests import Request, Session

# -------------------------------
# Set Up Info for Sierra API Host 
# -------------------------------

SIERRA_API_HOST = 'HOST NAME HERE'      
SIERRA_API_KEY = 'API KEY HERE'   
SIERRA_API_KEY_SECRET = 'API SECRET HERE'                
AUTH_URI = '/iii/sierra-api/v5/token'
VALIDATE_URI = '/iii/sierra-api/v5/patrons/validate'
PATRONS_URI = '/iii/sierra-api/v5/patrons/'
logFile = '/home/ubuntu/projects/affiliations/logFile.txt'

# ----------------------------------------------
# Prepare URL, custom headers, and body for auth 
# ----------------------------------------------

# Create URL for auth endpoint
auth_url = SIERRA_API_HOST + AUTH_URI

# Base64 encode the API key and secret separated by a ':' (colon)
encoded_key = base64.b64encode(SIERRA_API_KEY + ':' + SIERRA_API_KEY_SECRET)

auth_headers = {'Accept': 'application/json', 'Authorization': 'Basic ' + encoded_key,'Content-Type': 'application/x-www-form-urlencoded'}

# Set grant type request for HTTP body
grant_type = 'client_credentials'  # Request a client credentials grant authorization

# Make the call to the Auth endpoint to get a bearer token
auth_response = requests.post(auth_url, headers = auth_headers, data = grant_type)

access_token = auth_response.json()['access_token']

# Create headers for making subsequent calls to the API
request_headers = {'Accept': 'application/json', 'Authorization': 'Bearer ' + access_token,'Content-Type': 'application/json'}


# -------------------------------------------------------------
# Open the file of pending updates 
# -------------------------------------------------------------
with open('/home/Halima/projects/affiliations/todolist.txt','r') as f:
        resultlist = json.load(f)
#
# -------------------------------------------------------------
# Parse the sql results; assign Python variables; construct
# the 'payload' JSON object
# -------------------------------------------------------------
for item in resultlist:
    PATRON_RECORD_ID=str(item[0])
    my_patron_name  =str(item[2])+", "+str(item[3])
    my_affiliation = str(item[4])
    # payload = { 
    #    "expirationDate": ""+str(yyyymmdd(item[3]))+"",
    #    "barcodes": [""+str(item[2])+""],
    #    "addresses": [ { "lines": [ " " ], "type": "h" } ]
    #    }
    payload = {
        "varFields":
            [ 
            { "fieldTag": "d", "content": ""+str(item[4])+"" },
            { "fieldTag": "p", "content": "" }
            ]
        }

    # Add this patron's id to the end of the URL for endpoint
    patrons_url = SIERRA_API_HOST + PATRONS_URI + PATRON_RECORD_ID
    
    # UPDATE the patron record
    patrons_response = requests.put(patrons_url, headers = request_headers, data = json.dumps(payload))

    # log the result
    with open(logFile, 'a') as l:
        l.write("PATRON ID:" + PATRON_RECORD_ID + "\n")
        l.write("PATRON NAME:" + my_patron_name + "\n")
        if patrons_response.status_code == 204:
            l.write("SUCCESSFULLY UPDATED \n")
        else:
            l.write("****** ERROR ******* \n" + patrons_response_status_code) 
    print(PATRON_RECORD_ID)
print('done. remove todolist.txt!')
