#! /usr/bin/python
# FILE:   get-patronid.py
# Author: Michael Cummings, Assistant Museum Librarian, Systems and Information Technology 
#         Thomas J. Watson Libary, The Metropolitan Museam of Art
#         June, 2018
# Editor: Halima Rahman, Intern
# Gist:   Finds information about a given patron by their patron id.
# USAGE:  $python get-patronid.py
#
import psycopg2
try:
    connect_str = "dbname='iii' user='USER NAME HERE' host='HOST HERE' " + \
                  "password='PASSWORD HERE' port='1032'"
    # use our connection values to establish a connection
    conn = psycopg2.connect(connect_str)
    conn.set_client_encoding('UTF8')
    # create a psycopg2 cursor that can execute queries
    cursor = conn.cursor()
    # run a SELECT statement - 
    #cursor.execute("""SELECT id,barcode from sierra_view.item_record_property where
    #barcode='30620011440244'""")

    cursor.execute("""SELECT DISTINCT
    v.id as system_id,
    -- searchable id, where a is a wildcard replacing the check digit
    '.p' || v.record_num || 'a' as patron_rec_id,
    'mid',
    UPPER(first_name) as first_name, 
    UPPER(last_name) as last_name, 
    'Visitor'as patron_type,
    'non-MMA'as department,
    r.name as role,
    q.name as institution,
    -- the next field is a placeholder for varfield 'd' content to be merged
    -- post query
    'EXTRA',
    CASE
        WHEN (addr2 ISNULL AND city ISNULL AND region ISNULL and postal_code ISNULL)
        THEN 'ADDRESS NEEDS UPDATE'
        WHEN (LENGTH(addr2) > 2 AND LENGTH(city)=2) THEN UPPER(addr2)
        WHEN (city = 'NY') THEN 'NEW YORK'
        WHEN (city ISNULL) THEN 'ADDRESS NEEDS CITY'
        ELSE 
        UPPER(city)
        END as city,
    CASE
        WHEN region > '' THEN regexp_replace(region, '\.', '', 'g') 
        WHEN (LENGTH(city)=2 AND addr2 >'') THEN UPPER(city)
        WHEN city = 'New York' THEN 'NY'
        ELSE
        UPPER(region)
    END AS region,
    CASE
    WHEN (country ISNULL) THEN 'United States'
        ELSE
        country
    END AS country,
    postal_code,
    -- calculate the status
    CASE
        WHEN expiration_date_gmt isnull THEN 'ACTIVE'
        WHEN expiration_date_gmt > NOW() THEN 'ACTIVE'
         ELSE
            'EXPIRED'
    END as status
    FROM
    sierra_view.patron_view v
    JOIN sierra_view.patron_record_fullname n   
        ON v.id = n.patron_record_id
    JOIN sierra_view.user_defined_pcode1_myuser q   
        ON v.pcode1 = q.code
    JOIN sierra_view.user_defined_pcode2_myuser r   
        ON v.pcode2 = r.code
    JOIN sierra_view.record_metadata m   
        ON v.id = m.id
    -- some records, might not have a patron address but need these fields to join tables
    LEFT JOIN sierra_view.patron_record_address a   
        ON v.id = a.patron_record_id
    --LEFT JOIN sierra_view.varfield_view f 
        --ON v.id = f.record_id
    WHERE
    v.id='481036482993'
    and
    v.ptype_code in ('5','6')
    -- next screens out bad visitor ptype that have museum values
    -- AND r.code not in ('z','v','m')
    -- AND f.field_content like '2099000%'
    -- and length(f.field_content)=14
    -- these two speed up varfield criteria, selecting the Museum ID field, assumes a
    -- Museum ID on the patron
    -- AND f.record_type_code='p' 
    -- AND f.varfield_type_code='u'
    -- metadata type for patron
    AND m.record_type_code='p'
    limit 30000""")
    rows = cursor.fetchall()
    print(rows) 
except Exception as e:
    print("ERROR")
    print(e)
