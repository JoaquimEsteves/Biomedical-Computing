#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import argparse
import sqlite3 as lite
import sys
import utils
from utils import Logger
log = Logger(debug=settings.DEBUG)
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
		cur.execute('SELECT SQLITE_VERSION()')
		
		data = cur.fetchone()
		
		print "SQLite version: %s" % data                
		
	except lite.Error, e:
		
		print "Error %s:" % e.args[0]
		sys.exit(1)
		
	log.info("Connected to database correctly!...")
	
	###### MONTERS BELLOW
	'''
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
	try:
		while(True):
			# waits for client input:
			input_data = raw_input()
			# handle which command should run
			if input_data.startswith('list'):
				# list - chama o ECP com UDP as protocol. pede a lista de topicos
				log.debug("list - Requesting list of possible translations from TCS server.")
				_list(args)
			elif input_data.startswith('request'):
				# request - request translation for given language
				log.debug("request - Requesting translation for given arguments")
				_request(args, input_data)
			elif input_data == 'exit':
				# exit - exit user application
				log.debug("exit - Exiting user application.")
				break
			elif input_data == 'help':
				# help - show list of possible commands
				commands = map(lambda x: '\t> {}'.format(x), [
					'list: Requesting list of possible translations from TCS server.',
					'request: Requesting translation for given arguments.\n\t\t> request n t N W1 W2 ... WN\n\t\t> request n f filename',
					'exit: Exit current user application.',
				])
				log.info("""List of possible commands:\n{}""".format(
					"\n".join(commands)))
			else:
				# validate corner cases
				if input_data.strip() != '':
					log.warning("\"{}\" command does not exist.".format(input_data))
	except KeyboardInterrupt, e:
		# if CTRL+C is pressed, then go for last step
		log.info("\nCTRL+C - Exiting user application.")
		pass
		
		
		'''