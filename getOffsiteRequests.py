#!/usr/bin/python
#	File:   getOffsiteRequests.py 
#   Author: Michael Cummings, Assistant Museum Librarian, Systems and Information Technology
#			Thomas J. Watson Library, The Metropolitan Museum of Art
#			June, 2018
#   Editor: Halima Rahman, Intern
#   Gist: Script passes a JSON query for hold requests placed on items in location offsite where
#         hold creation date equals today. Item location is sierra item field 79; location
#         offsite is code 'off'. Item hold creation date is item field 8003.
#         This script saves results to a file; there are subsequent steps in seperate scripts
#         which retrieve the barcode for the selected item and send them to caiasoft via their API.           
#	Usage:	$python getoffsiteRequests.py
#			Run this script just before midnight to pickup all requests for the same day.
import json
import requests
import base64
from requests import Request, Session
from datetime import date

hold_date = str(date.today())
	

#######################
##
## Read config file
##
#######################
from ConfigParser import SafeConfigParser
parser = SafeConfigParser()
parser.read('/home/helper/local_config.cfg')

SIERRA_API_HOST = parser.get('sierra', 'SIERRA_API_HOST')
SIERRA_API_KEY = parser.get('sierra', 'SIERRA_API_KEY')
SIERRA_API_KEY_SECRET = parser.get('sierra', 'SIERRA_API_KEY_SECRET')

ITEMS_JSON_PREFIX = parser.get('filepaths', 'ITEMS_JSON_PREFIX')

AUTH_URI = '/iii/sierra-api/v5/token'
VALIDATE_URI = '/iii/sierra-api/v5/items/validate'
ITEMS_URI = '/iii/sierra-api/v5/items/query?offset=0&limit=1000'

## Create URL for auth endpoint
auth_url = SIERRA_API_HOST + AUTH_URI

## Base64 encode the API key and secret separated by a ':' (colon)
encoded_key = base64.b64encode(SIERRA_API_KEY + ':' + SIERRA_API_KEY_SECRET)

auth_headers = {'Accept': 'application/json', 'Authorization': 'Basic ' + encoded_key,'Content-Type': 'application/x-www-form-urlencoded'}

## Set grant type request for HTTP body
grant_type = 'client_credentials'  

## Make the call to the Auth endpoint to get a bearer token
auth_response = requests.post(auth_url, headers = auth_headers, data = grant_type)
access_token = auth_response.json()['access_token']

## Create headers for making subsequent calls to the API
request_headers = {'Accept': 'application/json', 'Authorization': 'Bearer ' + access_token,'Content-Type': 'application/json'}

## Create URL for items endpoint
items_url = SIERRA_API_HOST + ITEMS_URI 

# 
# Create JSON query

payload = {
  "queries": [
    {
      "target": {
        "record": {
          "type": "item"
        },
        "id": 79
      },
      "expr": {
        "op": "equals",
        "operands": [
          "off  ",
          ""
        ]
      }
    },
    "and",
    {
      "target": {
        "record": {
          "type": "item"
        },
        "id": 8003
      },
      "expr": {
        "op": "equals",
        "operands": [
          hold_date,
          ""
        ]
      }
    }
  ]
}


#######################
##
## Submit the query
##
#######################

items_response = requests.post(items_url, headers=request_headers, json=payload)

# print '********** RESPONSE ',items_url 
# print "RESPONSE CODE: ", items_response.status_code # Print to stdout
# print ' '
# print "Total results: " + str(items_response.json()['total'])
# itemlist = items_response.text
itemlist = json.dumps(items_response.json(),indent=4)

## End part one. Save list of links to Sierra items in a file.
## Opening with w option erases preexisting data
#f = open('/home/halima/projects/clancy/items-'+hold_date, 'w')
f = open(ITEMS_JSON_PREFIX + hold_date, 'w')
f.write(itemlist)
f.close()
