#!/usr/bin/python
#  File:   sqlBuildDict.py
#  Author: Michael Cummings, Assistant Museum Librarian, Systems and Information Technology
#		   Thomas J. Watson Library, The Metropolitan Museam of Art
#          June, 2018
#  Editor: Halima Rahman, Intern
#  Gist:   execute an SQL query from a file against Sierra
#  Usage:  $python sqlBuildDict.py

import psycopg2
import psycopg2.extras
import json
from datetime import time
from datetime import date

thisday = date.today()
savedSQLresults = '/home/Halima/projects/fellows/todolist.txt'
logFile = '/home/Halima/projects/fellows/logFile.txt'

try:
    connect_str = "dbname='iii' user='USER NAME' host='HOST NAME' password='PASSWORD' port='1032'"
    # establish a connection
    conn = psycopg2.connect(connect_str)
    # create a psycopg2 cursor that can execute queries
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    # run a SELECT statement - 
    cursor.execute(open("/home/Halima/projects/fellows/findfellows.sql","r").read())
    rows = cursor.fetchall()
    
    #print (json.dumps(rows, indent =4)) 
    if cursor.rowcount != 0:
        with open(savedSQLresults,'a') as f:
             f.write(json.dumps(rows))
        
        with open(logFile,'a') as l:
            l.write(str(thisday) + "| sqlBuildDict saved " +
            str(cursor.rowcount) + " results \n")
    else:
        with open(logFile,'a') as l:
            l.write(str(thisday) + "| sqlBuildDict did not find results\n")

        print "no_results"

except Exception as e:
    print("ERROR")
    print(e)
