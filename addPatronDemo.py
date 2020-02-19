# Filename: addPatronDemo.py
# Author:   Michael Cummings, Assistant Museum Librarian, Systems and Information Technology
#		    Thomas J. Watson Library, The Metropolitan Museam of Art
#           June, 2018
# Editor:   Halima Rahman, Intern
# Gist:     add a Sierra.patron
# Usage:    $python addPatronDemo.py
import json
import requests
import base64
from requests import Request, Session

############# Set Up Info for Sierra API Host #############

# SIERRA_API_HOST = 'https://sandbox.iii.com:443' # Hostname for Sierra sandbox API
SIERRA_API_HOST = 'enter hostname for Met Sierra' 
SIERRA_API_KEY = 'enter API key for host' 
SIERRA_API_KEY_SECRET = 'API secret for host'

############# Set URIs for Sierra API endpoints 					#############

AUTH_URI = '/iii/sierra-api/v5/token'
VALIDATE_URI = '/iii/sierra-api/v5/patrons/validate'
PATRONS_URI = '/iii/sierra-api/v5/patrons'

############# Prepare URL, custom headers, and body for auth 				#############
# Create URL for auth endpoint
auth_url = SIERRA_API_HOST + AUTH_URI
# Base64 encode the API key and secret separated by a ':' (colon)
encoded_key = base64.b64encode(SIERRA_API_KEY + ':' + SIERRA_API_KEY_SECRET)
auth_headers = {'Accept': 'application/json', 'Authorization': 'Basic ' + encoded_key,'Content-Type':'application/x-www-form-urlencoded'}
# Set grant type request for HTTP body
grant_type = 'client_credentials' # Request a client credentials grant authorization
#
print '********** CALLING POST', auth_url
# Make the call to the Auth endpoint to get a bearer token
auth_response = requests.post(auth_url, headers = auth_headers, data = grant_type)
print '********** RESPONSE ', auth_url
print ' '
print 'RESPONSE CODE: ', auth_response.status_code 
print "HEADERS: " + str(auth_response.headers)
print ' '
print "RESPONSE BODY: " + str(auth_response.text)
print ' '
access_token = auth_response.json()['access_token']
print ("access_token: " + access_token)
print ' '
# Create headers for making subsequent calls to the API
request_headers = {'Accept': 'application/json', 'Authorization': 'Bearer ' + access_token,'ContentType':'application/json'}
# Create URL for API endpoint
patrons_url = SIERRA_API_HOST + PATRONS_URI

############# Create Patron JSON object 						#############
############# Replace with action to iterate through a set of records or use parameters #############

payload = {
 "names": [
 "Bee, Busy"
 ],
 "barcodes": [
 "7777777"
 ],
 "expirationDate": "2018-07-21",
 "emails": [
 "busy.bee@metmuseum.org"
 ],
 "patronType": 2,
 "patronCodes": {
 "pcode1": "h",
 "pcode2": "z",
 "pcode3": 30
 },
 "addresses": [
 {
 "lines": [
 "99 North Field Park",
 "Hudson Valley, NY 10101"
 ],
 "type": "h"
 }
 ]
}

print ' '
print (json.dumps(payload, indent =4))

############# Send the Patron info to the server					#############
print '********** CALL ', patrons_url
patrons_response = requests.post(patrons_url, headers=request_headers, json=payload)
print '********** RESPONSE ', patrons_url
print "RESPONSE CODE: ", patrons_response.status_code # Print to stdout
print ' '
print "RESPONSE BODY : ", patrons_response.text # Print to stdout

#### print (json.dumps(patrons_response.json(), indent =4))



