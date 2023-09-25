#!/usr/bin/python
# File:   cloistershold.py
# Author: Michael Cummings, Assistant Museum Libarian, Systems and Information Technology 
#         Thomas J. Watson Libary, The Metropolitan Museam of Art 
# Editor: Halima Rahman, Intern
# Gist:   New holds are any found where the hold id is greater than the
#         value stored in the logfile, last_hold_processed.txt
#         If newholds were found the highest hold id number is
#         stored in the log.
#         If newholds.txt contains anything after this script runs,
#         the file can be emailed 
# Usage:  $python cloistershold.py > newholds.txt
import psycopg2
import pprint

def main():
    # -------------------------------------------------
    # assign the starting hold id. get it from the log
    # -------------------------------------------------
    pf = open("/home/Halima/projects/cloisters/last_hold_processed.txt","r")
    PREVIOUS_HOLDID= str(pf.read())
    MAX_HOLD=""

    # ------------------------------------------
    # prepare the connection. standard psycopg2
    # ------------------------------------------
    conn_string = "host='HOST NAME HERE' port=1032 dbname='iii' user='USER NAME HERE' password='PASSWORD HERE' sslmode='require'"
    # print "Connecting to database\n	->%s" % (conn_string)
 
    conn = psycopg2.connect(conn_string)
    conn.set_client_encoding('UTF8')
    cursor = conn.cursor()
  
    # ------------------------------------------------
	# execute the SQL query. backslash continues lines
    # ------------------------------------------------
    cursor.execute("SELECT h.id, f.last_name, f.first_name, id2reckey(f.patron_record_id), \
    TO_CHAR(placed_gmt,'YYYY-MM-DD') AS request_date, \
    TO_CHAR(placed_gmt,'HH24:MI') AS request_time, \
    UPPER(p.call_number_norm), \
    p.barcode, id2reckey(b.bib_record_id), LEFT(best_title,40), LEFT(best_author,40)\
    FROM \
    sierra_view.patron_record_fullname f, \
    sierra_view.hold h,\
    sierra_view.item_view i, \
    sierra_view.bib_record_item_record_link k,\
    sierra_view.bib_record_property b,\
    sierra_view.item_record_property p\
    WHERE \
    h.id > "+PREVIOUS_HOLDID+" and \
    h.record_id=i.id and \
    i.location_code = 'off' and \
    h.patron_record_id=f.patron_record_id and \
    i.id=k.item_record_id and \
    b.bib_record_id=k.bib_record_id and\
    p.item_record_id=i.id\
    order by h.id")

    records = cursor.fetchall()

    # tests
    # print number of records
    # print len(records)
	# print out the records using pretty print
    # pprint.pprint(records)
    
    # -----------------------------------------
    # print out customized list of the records 
    # specify the destination file on the
    # command line when this script is called
    # -----------------------------------------
    for record in records:
        MAX_HOLD = str(record[0])
        print ""
        print "PATID: "+record[3]+"  LAST : "+record[1]+"  FIRST: "+record[2]
        print "RDATE: "+record[4]+"  RTIME: "+record[5]
        print "CALL#: "+str(record[6])
        print "BARCD: "+record[7]
        print "TITLE: "+record[9]
        print "AUTH : "+record[10]
        print "BIBID: "+record[8]
        print "HOLD#: "+str(record[0])
    conn.close

    # ---------------------------------------
    # record new maximum hold id in the log 
    # ---------------------------------------
    if MAX_HOLD > PREVIOUS_HOLDID:
        f = open("/home/Halima/projects/cloisters/last_hold_processed.txt","w")
        f.write(MAX_HOLD)
        f.close()

if __name__ == "__main__":
    main()
