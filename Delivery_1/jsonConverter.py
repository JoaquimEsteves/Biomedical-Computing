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
		cur.execute("SELECT * FROM Medication;")
		
		print cur.fetchall()            
		
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
			input_data = raw_input()
	except KeyboardInterrupt, e:
		# if CTRL+C is pressed, then go for last step
		print "\nCTRL+C - Exiting user application."
		pass
		
		