#!/usr/bin/python
# file:   addorderGOBIasJSON.py
# author: Michael Cummings, Assistant Museum Librarian, Systems and Information Technology 
#         Thomas J. Watson Libary, The Metropolitan Museam of Art
#         June, 2018
# Editor: Halima Rahman, Intern
# Gist:   Add a GOBI order in JSON format using Sierra API
# Usage:  $python addorderGOBIasJSON.py           
import json
import requests
import base64
from requests import Request, Session

# ------------------------------
# Set Up Info for Sierra API Host 
# ------------------------------

SIERRA_API_HOST = 'HOST HERE'      
SIERRA_API_KEY = 'API KEY HERE'   
SIERRA_API_KEY_SECRET = 'API SECRET HERE'                
AUTH_URI = '/iii/sierra-api/v5/token'
VALIDATE_URI = '/iii/sierra-api/v5/acquisitions/validate'
# the next one is for adding GOBI orders
ACQS_URI= '/iii/sierra-api/v5/acquisitions/orders/classic?'
logFile = '/home/halima/projects/acquisitions/logFile.txt'

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
request_headers = {'Accept': 'application/marc-in-json', 'Authorization': 'Bearer ' + access_token,'Content-Type': 'application/marc-in-json'}
PARAMS ="login=gobiybpapi&location=ucl&fund=wlib&vendor=quyan"
theurl = SIERRA_API_HOST + ACQS_URI + PARAMS
payload = {
"marc": {
      "leader": "00000nam a2200000u  4500",
      "controlfield": [
         {
            "@tag": "001",
            "#text": "99982943180"
         },
         {
            "@tag": "003",
            "#text": "NhCcYBP"
         },
         {
            "@tag": "005",
            "#text": "20191218110645.0"
         },
         {
            "@tag": "008",
            "#text": "191218t20192019xx ||||||||||||||   eng d"
         }
      ],
      "datafield": [
         {
            "@tag": "020",
            "@ind1": "",
            "@ind2": "",
            "subfield": [
               {
                  "@code": "a",
                  "#text": "9781682618998"
               },
               {
                  "@code": "c",
                  "#text": "18.99"
               }
            ]
         },
         {
            "@tag": "035",
            "@ind1": "",
            "@ind2": "",
            "subfield": {
               "@code": "a",
               "#text": "(OCoLC)1108442613"
            }
         },
         {
            "@tag": "100",
            "@ind1": "1",
            "@ind2": "",
            "subfield": {
               "@code": "a",
               "#text": "ABRAMS, HOWIE"
            }
         },
         {
            "@tag": "245",
            "@ind1": "1",
            "@ind2": "0",
            "subfield": {
               "@code": "a",
               "#text": "ABCS OF METALLICA."
            }
         },
         {
            "@tag": "260",
            "@ind1": "",
            "@ind2": "",
            "subfield": [
               {
                  "@code": "b",
                  "#text": "PERMUTED PLATINUM"
               },
               {
                  "@code": "c",
                  "#text": "2019"
               }
            ]
         }
      ]
   }
}
acquisitions_response= requests.get(theurl, headers = request_headers, json=payload)
#print (json.dumps(acquisitions_response.json(), indent =4))
print acquisitions_response.status_code
#print acquisitions_response.txt

