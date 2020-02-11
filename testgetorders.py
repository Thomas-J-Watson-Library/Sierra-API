#!/usr/bin/python
# File:   testgetorders.py
# Author: Michael Cummings, Assistant Museum Librarian, Systems and Information Technology 
#         Thomas J. Watson Libary, The Metropolitan Museam of Art
#         June, 2018
# Editor: Halima Rahman, Intern
# Gist:   This script simply tests your acquisitions endpoint. It returns a few orders.
# Usage:  $python testgetorders.py
#           
import json
import requests
import base64
from requests import Request, Session

# ------------------------------
# Set Up Info for Sierra API Host 

SIERRA_API_HOST = 'HOST HERE'      
SIERRA_API_KEY = 'API KEY HERE'   
SIERRA_API_KEY_SECRET = 'API SECRET HERE'                
AUTH_URI = '/iii/sierra-api/v5/token'
VALIDATE_URI = '/iii/sierra-api/v5/acquisitions/validate'
# the next one is for adding orders
ACQS_URI= '/iii/sierra-api/v5/acquisitions/orders'
# the next one is for querying orders
ORDERS_URI= '/iii/sierra-api/v5/orders'
logFile = '/home/ubuntu/projects/acquisitions/logFile.txt'

# ----------------------------------------------
# Prepare URL, custom headers, and body for auth 

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
theurl = SIERRA_API_HOST + ORDERS_URI

acquisitions_response= requests.get(theurl, headers = request_headers)
print (json.dumps(acquisitions_response.json(), indent =4))


