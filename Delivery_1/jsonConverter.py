#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import argparse
import sqlite3 as lite
import sys
# import utils
# from utils import Logger
# log = Logger(debug=settings.DEBUG)
from pprint import pprint

#!/usr/bin/python
# -*- coding: utf-8 -*-
con = None
#sdasd

# with open('data.json') as data_file:    
    # data = json.load(data_file)

# pprint(data)


if __name__ == "__main__":
	try:
		con = lite.connect('myDB.sqlt')
		
		cur = con.cursor()
		print "Showing off some of the items on our database! Hopefully it will be empty!\n"	
		cur.execute("SELECT * FROM Medication;")
		print cur.fetchall()    
		cur.execute("SELECT * FROM Product;")
		print cur.fetchall()            
		print "trying to insert!"
		cur.execute("INSERT INTO Medication VALUES ('123','ayy','manushiet','1','bugger','ayyy','sysshit');")
		con.commit();
		cur.execute("INSERT INTO Medication VALUES ('1234','ayy',None,'1','bugger','ayyy','sysshit');")
		con.commit();
		cur.execute("SELECT * FROM Medication;")
		print cur.fetchall()    
		print "Hopefully we can see that inserting values works, with that out of the way let's start analyzing some jsons!\n\n"
	except lite.Error, e:
		
		print "Error %s:" % e.args[0]
		sys.exit(1)
		
	print "Sucessfully connected to db!"
	
	
	###### MONTERS BELLOW
	"""
	# format of command is ./user [-n TCSname] [-p TCSport] so get those arguments and validate them
	parser = argparse.ArgumentParser()
	parser.add_argument('-n', dest='tcs_name', type=str, default=settings.DEFAULT_TCS_NAME,
						help='Translation Contact Server IP Address.')
	parser.add_argument('-p', dest='tcs_port', type=int, default=settings.DEFAULT_TCS_PORT,
						help='Translation Contact Server Port Address.')
	args = parser.parse_args()	# validate them
	# print information just to make sure
	log.debug("Using TCS Name = {}, TCS Port = {}.".format(args.tcs_name, args.tcs_port))
	log.info("Welcome :).")
	# forever & ever (util "exit")
	"""
	try:
		while(True):
			# waits for client input:
			print "Ok just write down the name of the json file you want to open up!"
			input_data = raw_input()
			with open(input_data) as data_file:    
				data = json.load(data_file)
				try:
					if data["resourceType"] != "Medication":
						print "This is not a medication!"
						break
					medID = data["id"]
					text = None
					manufacturer = None
					isBrand = None
					code = None
					display = None
					system = None
					if 'text' in data :
						text = data["text"]
					if 'manufacturer' in data:
						manufacturer = data['manufacturer']["reference"]
					if 'isBrand' in data:
						isBrand = data['isBrand']
					if 'code' not in data:	
						coding = data['code']['coding']
						code = coding['code']
						display = coding['display']
						system = coding['system']
					medicationInsert = "INSERT INTO Medication VALUES ('"+str(medID)+"'"
					medicationInsert +=	",'"+str(text)+"','"+str(manufacturer)+"','"+str(isBrand)+"','"+str(code)+"','"+str(display)+"','"+str(system)+"');"
					cur.execute(medicationInsert)
					con.commit();	
				except Exception, e:
					print "Error %s:" % e.args[0]
					break
				
				pprint(data)
	except KeyboardInterrupt, e:
		# if CTRL+C is pressed, then go for last step
		print "\nCTRL+C - Exiting user application."
		pass
		
		