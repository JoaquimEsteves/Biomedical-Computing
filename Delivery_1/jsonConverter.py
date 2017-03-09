#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import argparse
import sqlite3 as lite
import sys
import base64
# import utils
# from utils import Logger
# log = Logger(debug=settings.DEBUG)
from pprint import pprint

con = None

def parseMedication(cur,con,data):
	if data["resourceType"] != "Medication":
		print "This is not a medication!"
		return
	medID =  "'"+str(data["id"])+"'"
	text = 'NULL'
	encodedText = 'NULL'
	manufacturer = 'NULL'
	isBrand = 'NULL'
	code = 'NULL'
	display = 'NULL'
	system = 'NULL'
	if 'text' in data :
		#ALWAYS ENCODE PLAIN TEXT WHEN DEALING WITH JSONS
		#JSONS ARE REALLY BLOODY FINNICKY
		text = str(data["text"])
		encodedText = "'"+str(base64.b64encode(text))+"'"
	if 'manufacturer' in data:
		manufacturer = "'"+str(data['manufacturer']["reference"])+"'"
	if 'isBrand' in data:
		isBrand = "'"+str(data['isBrand'])+"'"
	if 'code' in data:
		#For some SILLY REASON, code also apparently can have text!
		if 'text' in data['code']:
			text = base64.b64decode(encodedText) + "Coding Text: " + str(data['code']['text'])
			encodedText = "'"+str(base64.b64encode(text))+"'"
		# coding = "'"+str(data['code']['coding'])+"'"
		if 'coding' in data['code']:
			code = "'["
			display = "'["
			system = "'["
			max_items = len(data['code']['coding'])
			i = 0
			while i < max_items:
				code += str(data['code']['coding'][i]['code'])+","
				display += str(data['code']['coding'][i]['display'])+","
				system += str(data['code']['coding'][i]['system'])+","
				i += 1
			code += "]'"
			display += "]'"
			system += "]'"
	medicationInsert = "INSERT INTO Medication VALUES ("+medID+""
	medicationInsert +=	","+encodedText+","+manufacturer+","+isBrand+","+code+","+display+","+system+");"
	
	cur.execute(medicationInsert)
	con.commit();	
	cur.execute("SELECT * FROM Medication;")
	print "\n\n\n\nPrinting out the complete list of Medications!"
	print cur.fetchall()
	return medID

def parseProduct(cur,con,data,medID):
	text = 'NULL'
	code = 'NULL'
	display = 'NULL'
	system = 'NULL'
	if 'form' in data["product"]:
		if 'code' in data["product"]["form"]:
			#For some SILLY REASON, code also apparently can have text!
			if 'text' in data["product"]["form"]['code']:
				text = base64.b64decode(encodedText) + "Coding Text: " + str(data['code']['text'])
				encodedText = "'"+str(base64.b64encode(text))+"'"
			# coding = "'"+str(data['code']['coding'])+"'"
			if 'coding' in data['code']:
				code = "'["
				display = "'["
				system = "'["
				max_items = len(data['code']['coding'])
				i = 0
				while i < max_items:
					code += str(data['code']['coding'][i]['code'])+","
					display += str(data['code']['coding'][i]['display'])+","
					system += str(data['code']['coding'][i]['system'])+","
					i += 1
				code += "]'"
				display += "]'"
				system += "]'"	
	return
def parsePackage(cur,con,data,medID):
	return
	
if __name__ == "__main__":
	con = lite.connect('myDB.sqlt')
	
	cur = con.cursor()
	print "Showing off some of the items on our database! Hopefully it will be empty!\n"	
	cur.execute("SELECT * FROM Medication;")
	print cur.fetchall()    
	cur.execute("SELECT * FROM Product;")
	print cur.fetchall()            
	# print "trying to insert!"
	# cur.execute("INSERT INTO Medication VALUES ('123','ayy','manushiet','1','bugger','ayyy','sysshit');")
	# con.commit();
	# cur.execute("INSERT INTO Medication VALUES ('1234','ayy','NULL','1','bugger','ayyy','sysshit');")
	# con.commit();
	# cur.execute("SELECT * FROM Medication;")
	# print cur.fetchall()    
	# print "Hopefully we can see that inserting values works, with that out of the way let's start analyzing some jsons!\n\n"
		
	print "Sucessfully connected to db!"
	
	try:
		while(True):
			# waits for client input:
			print "Ok just write down the name of the json file you want to open up!\n\n\n"
			input_data = raw_input()
			with open(input_data) as data_file:    
				data = json.loads(data_file)
				try:
					medID = parseMedication(cur,con,data)
					if 'product' in data:
						parseProduct(cur,con,data, medID)
					if 'package' in data:
						parsePackage(cur,con,data,medID)
					
				except ValueError:
					print "Error %s:" % e.args[0]
					break
				
				# pprint(data)
	except KeyboardInterrupt, e:
		# if CTRL+C is pressed, then go for last step
		print "\nCTRL+C - Exiting user application."
		pass
		
		