#/usr/bin/python
# File:   affiliations/standardize/doNull.py
# Author: Michael Cummings, Assistant Museam Libarian, Systems and Information Technology 
#         Thomas J. Watson Libary, The Metropolitan Museam of Art
# Editor: Halima Rahman, Intern
# Gist:   nulls-out the affiliation, for example 
#         from a list where the affiliaton is = 'none'
#         the id values are from PgAdmin, these values
#         are recognized the the API
# Usage:  $python doNull.py
import json
import requests
import csv
import base64
from requests import Request, Session

# -------------------------------
# Set Up Info for Sierra API Host 
# -------------------------------

SIERRA_API_HOST = 'HOST HERE'      
SIERRA_API_KEY = 'API KEY HERE'   
SIERRA_API_KEY_SECRET = 'API SECRET HERE'                
AUTH_URI = '/iii/sierra-api/v5/token'
VALIDATE_URI = '/iii/sierra-api/v5/patrons/validate'
PATRONS_URI = '/iii/sierra-api/v5/patrons/'

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
# Open the file of pending updates and null out field d
# -------------------------------------------------------------
DONECOUNT=0
input_file = csv.DictReader(open("/home/Halima/projects/affiliations/standardize/todolist.txt"))
for row in input_file:
    DONECOUNT += 1
    PATRON_RECORD_ID  = str(row['PID'])
    payload = {
        "varFields":
            [ 
            { "fieldTag": "d", "content": "" },
            ]
        }

    # Add this patron's id to the end of the URL for endpoint
    patrons_url = SIERRA_API_HOST + PATRONS_URI + PATRON_RECORD_ID
    
    # UPDATE the patron record
    patrons_response = requests.put(patrons_url, headers = request_headers, data = json.dumps(payload))

    # log the result
    if patrons_response.status_code == 204:
        print("SUCCESSFULLY UPDATED "+PATRON_RECORD_ID+" "+str(DONECOUNT))
    else:
        print("****** ERROR ******* \n" + patrons_response_status_code) 
print('done. remove todolist.txt!')
