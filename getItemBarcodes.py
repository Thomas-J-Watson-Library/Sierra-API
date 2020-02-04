#!/usr/bin/python
#	File:   getItemBarcodes.py 
#	Author:	Michael Cummings, Assistant Museum Librarian, Systems and Information Technology
#			Thomas J. Watson Library, The Metropolitan Museum of Art
#			June, 2018
#   Editor: Halima Rahman, Intern
#   Gist:   Script passes a JSON query for hold requests placed on items in location offsite where
#         hold creation date equals today. Item location is sierra item field 79; location
#         offsite is code 'off'. Item hold creation date is item field 8003.
#         This script saves results to a file; there are subsequent steps in seperate scripts
#         which retrieve the barcode for the selected item and send them to caiasoft via their API.
#	Usage:	python getItemBarcodes.py fully-qualified-name-of-file-with-JSON-items  AM|PM
#           Run this script just before midnight to pick up all requests for the same day.
import json
import requests
import base64
import sys
from requests import Request, Session
from datetime import date

#--------------------------------------------
# function to pull id off hyperlink
#--------------------------------------------
def pluckId( str ):
	# Split the hyperlink string using the delimiter '/'
    parts = str.split('/')
    id_part = parts[7]
    str = id_part.replace('"}','')
    return(str);

#--------------------------------------------
# Read config file
#--------------------------------------------

from ConfigParser import SafeConfigParser
parser = SafeConfigParser()
parser.read('/home/helper/local_config.cfg')

SIERRA_API_HOST = parser.get('sierra', 'SIERRA_API_HOST')
SIERRA_API_KEY = parser.get('sierra', 'SIERRA_API_KEY')
SIERRA_API_KEY_SECRET = parser.get('sierra', 'SIERRA_API_KEY_SECRET')

AUTH_URI = '/iii/sierra-api/v5/token'
VALIDATE_URI = '/iii/sierra-api/v5/items/validate'
ITEMS_URI = '/iii/sierra-api/v5/items/'

hold_date = str(date.today())

# Cron requires full paths 
morningFile 	= parser.get('filepaths', 'MORNING_REQUESTS_FILE')+hold_date+".txt"
eveningFile 	= parser.get('filepaths', 'EVENING_REQUESTS_FILE')+hold_date+".txt"
circlogFile     = parser.get('filepaths', 'CIRC_LOG_FILE')+hold_date+".txt"
itemid = ''

#-----------------------------------------------
# Prepare URL, custom headers, and body for auth 
#-----------------------------------------------

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

# Create URL for items endpoint
items_url = SIERRA_API_HOST + ITEMS_URI

#------------------------------------------------
# Read the JSON file containing Sierra item links
#------------------------------------------------

with open(sys.argv[1]) as f:
    link_file_contents = json.load(f)

for hyperlink in link_file_contents['entries']:

	#-------------------------------------
	# Reduce hyperlink to the itemid alone
	#-------------------------------------
    itemid = pluckId(hyperlink['link'])

	#--------------------------------------------------
	# Pass the itemid to the API call to get a barcode
	#--------------------------------------------------

    payload = {'id': itemid, 'fields': 'barcode,fixedFields'}
    items_response = requests.get(items_url, headers = request_headers, params = payload)
	
	#--------------------------------------------------
	# Convert the API's JSON response to Python 
	#--------------------------------------------------
	
    responseStr = (json.dumps(items_response.json(), indent =2))
    responseData= json.loads(responseStr)
	#-------------------------------------------------------------------
	# For the AM request, retrieve and save ALL request barcodes
	#-------------------------------------------------------------------
    if sys.argv[2] == "AM":
        with open(morningFile,'a') as f:
            for holdrequest in responseData['entries']:
				# APPEND TO STRING OF BARCODES
                f.write(holdrequest['barcode'] + "\n")
    else:
		#-------------------------------------------------------------------
		# For the PM request, retrieve and save unmatched request barcodes
		# from the AM processing file. Since there may not have been any
        # requests in the AM, test test for IOError and if caught, use a
        # dummy value for comparisons.
		#-------------------------------------------------------------------
		
        try:
            with open(morningFile,'r') as m:
                AMbarcodes = m.read()
        except IOError:
                AMbarcodes = '00000007000000'
        for holdrequest in responseData['entries']:
            if holdrequest['barcode'] not in AMbarcodes:
                with open(eveningFile,'a') as f:
				# print ("Found new barcode. Saving in PM group: "+holdrequest['barcode'])
                    f.write(holdrequest['barcode'] + "\n")

        ## -- end of PM section --##
    #with open(circlogFile,'a') as c:
        #c.write(holdrequest['barcode']+" "+holdrequest['fixedFields']['76']['value']+"\n")

print("Done ")
