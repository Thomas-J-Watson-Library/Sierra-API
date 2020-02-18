#!/usr/bin/python
# File:   get-affphone.py
# Author: Michael Cummings, Assistant Museam Libarian, Systems and Information Technology 
#         Thomas J. Watson Libary, The Metropolitan Museam of Art
# Editor: Halima Rahman, Intern
# Gist:   This query finds the visitor records with phones that don't have
#         numbers, thus indicating the affiliation is in the wrong field.
#         The patron type must be 5 or 6        
# Usage:  $python get-affphone.py 
#
import psycopg2
import psycopg2.extras
import json
try:
    connect_str = "dbname='iii' user='USER HERE host='HOST HERE' " + \
                  "password='PASSWORD HERE' port='1032'"
    # use our connection values to establish a connection
    conn = psycopg2.connect(connect_str)
    conn.set_client_encoding('UTF8')
    cursor = conn.cursor()
    cursor.execute("""SELECT DISTINCT
    v.id as system_id,
    '.p' || v.record_num || 'a' as patron_rec_id,
    UPPER(first_name) as first_name, 
    UPPER(last_name) as last_name, 
    x.phone_number
    FROM
    sierra_view.patron_view v
    JOIN sierra_view.patron_record_fullname n   
        ON v.id = n.patron_record_id
    JOIN sierra_view.patron_record_phone x
        ON v.id=x.patron_record_id
    JOIN sierra_view.record_metadata m   
        ON v.id = m.id
    LEFT JOIN sierra_view.varfield_view f 
        ON v.id = f.record_id
    WHERE
    x.patron_record_phone_type_id=2
    AND
    v.ptype_code in ('5','6')
    AND m.record_type_code='p'
    AND phone_number > ''
        and phone_number NOT LIKE '%0%'
        and phone_number NOT LIKE '%1%'
        and phone_number NOT LIKE '%2%'
        and phone_number NOT LIKE '%3%'
        and phone_number NOT LIKE '%4%'
        and phone_number NOT LIKE '%5%'
        and phone_number NOT LIKE '%6%'
        and phone_number NOT LIKE '%7%'
        and phone_number NOT LIKE '%8%'
        and phone_number NOT LIKE '%9%'
        and phone_number NOT LIKE '%-%'
        and phone_number != ''
    order by x.phone_number
    limit 500""")
    rows = cursor.fetchall()
    with open('todolist.txt','a') as f:
        f.write(json.dumps(rows))
except Exception as e:
    print("ERROR")
    print(e)

print ('EDIT todolist.txt, remove backslashes from affiation and names.')
print ('After editing, run python doUpdate.py')
