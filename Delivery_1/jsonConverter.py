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
	medID =  "'"+json.dumps(data["id"])+"'"
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
		text = json.dumps(data["text"])
		encodedText = "'"+str(base64.b64encode(text))+"'"
	if 'manufacturer' in data:
		manufacturer = "'"+json.dumps(data['manufacturer']["reference"])+"'"
	if 'isBrand' in data:
		isBrand = "'"+json.dumps(data['isBrand'])+"'"
	if 'code' in data:
		#For some SILLY REASON, code also apparently can have text!
		if 'text' in data['code']:
			text = base64.b64decode(encodedText) + "Coding Text: " + json.dumps(data['code']['text'])
			encodedText = "'"+str(base64.b64encode(text))+"'"
		# coding = "'"+str(data['code']['coding'])+"'"
		if 'coding' in data['code']:
			code = "'["
			display = "'["
			system = "'["
			max_items = len(data['code']['coding'])
			i = 0
			while i < max_items:
				code += json.dumps(data['code']['coding'][i]['code'])+","
				display += json.dumps(data['code']['coding'][i]['display'])+","
				system += json.dumps(data['code']['coding'][i]['system'])+","
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
	encodedText = 'NULL'
	code = 'NULL'
	display = 'NULL'
	system = 'NULL'
	if 'form' in data["product"]:
		if 'coding' in data["product"]["form"]:
			#For some SILLY REASON, code also apparently can have text!
			if 'text' in data["product"]["form"]:
				text = json.dumps(data["product"]["form"]['text'])
				encodedText = "'"+str(base64.b64encode(text))+"'"
			# coding = "'"+str(data['code']['coding'])+"'"
			if 'coding' in data["product"]["form"]:
				code = "'["
				display = "'["
				system = "'["
				max_items = len(data["product"]["form"]['coding'])
				i = 0
				while i < max_items:
					code += json.dumps(data["product"]["form"]['coding'][i]['code'])+","
					display += json.dumps(data["product"]["form"]['coding'][i]['display'])+","
					system += json.dumps(data["product"]["form"]['coding'][i]['system'])+","
					i += 1
				code += "]'"
				display += "]'"
				system += "]'"
	productInsert = "INSERT INTO Product VALUES ("+medID+","+encodedText+","+code+","+display+","+system+");"
	cur.execute(productInsert)
	con.commit();	
	cur.execute("SELECT * FROM Product;")
	print "\n\n\n\nPrinting out the complete list of Products!"
	print cur.fetchall()
	if 'ingredient' in data["product"]:
		parseIngredient(cur,con,data,medID)
	if 'batch' in data["product"]:
		parseBatch(cur,con,data,medID)
	return
	
def parseIngredient(cur,con,data,medID):
	itemDisplay = 'NULL'
	ammountType = 'NULL'
	ammountValue = 'NULL'
	ammountUnit = 'NULL'
	ammountSystem = 'NULL'
	ingredientInsert = ""
	if "item" in data["product"]["ingredient"][0]:
		max_items = len(data["product"]["ingredient"])
		i = 0
		while i < max_items:
			itemDisplay = json.dumps(data["product"]["ingredient"][i]["item"]["display"])
			if "amount" in data["product"]["ingredient"][i]:
				ammountType = "'numerator'"
				ammountValue ="'" + json.dumps(data["product"]["ingredient"][i]["amount"]["numerator"]["value"]) + "'"
				ammountSystem ="'" + json.dumps(data["product"]["ingredient"][i]["amount"]["numerator"]["system"]) + "'"
				ammountUnit ="'" +json.dumps(data["product"]["ingredient"][i]["amount"]["numerator"]["code"]) + "'"
				ingredientInsert = "INSERT INTO Ingredient VALUES ("+medID+","+itemDisplay+","+ammountType+","+ammountValue+","+ammountUnit+","+ammountSystem+");"
				cur.execute(ingredientInsert)
				con.commit();	
				ammountType = "'denominator'"
				ammountValue ="'" + json.dumps(data["product"]["ingredient"][i]["amount"]["denominator"]["value"]) + "'"
				ammountSystem ="'" + json.dumps(data["product"]["ingredient"][i]["amount"]["denominator"]["system"]) + "'"
				ammountUnit ="'" +json.dumps(data["product"]["ingredient"][i]["amount"]["denominator"]["code"]) + "'"
				ingredientInsert = "INSERT INTO Ingredient VALUES ("+medID+","+itemDisplay+","+ammountType+","+ammountValue+","+ammountUnit+","+ammountSystem+");"
				cur.execute(ingredientInsert)
				con.commit();
			i += 1
	cur.execute("SELECT * FROM Ingredient;")
	print "\n\n\n\nPrinting out the complete list of Ingredients!"
	print cur.fetchall()

def parseBatch(cur,con,data,medID):
	lotNumber = 'NULL'
	expirationDate = 'NULL'
	if 'lotNumber' in data["product"]["batch"][0]:
		lotNumber = "'" + json.dumps(data["product"]["batch"][0]["lotNumber"]) + "'"
	if 'expirationDate' in data["product"]["batch"][0]:
		expirationDate = "'" + json.dumps(data["product"]["batch"][0]["expirationDate"]) + "'"
	batchInsert = "INSERT INTO batch VALUES ("+medID+","+lotNumber+","+expirationDate+");"
	cur.execute(batchInsert)
	con.commit();
	cur.execute("SELECT * FROM Batch;")
	print "\n\n\n\nPrinting out the complete list of Batches!!"
	print cur.fetchall()

def parsePackage(cur,con,data,medID):
	text = 'NULL'
	encodedText = 'NULL'
	code = 'NULL'
	display = 'NULL'
	system = 'NULL'
	
	if 'container' in data["package"]:
		#For some SILLY REASON, code also apparently can have text!
		if 'text' in data["package"]["container"]:
			text = "Coding Text: " + json.dumps(data["package"]["container"]["coding"]['text'])
			encodedText = "'"+str(base64.b64encode(text))+"'"
		# coding = "'"+str(data['code']['coding'])+"'"
		if 'coding' in data["package"]["container"]:
			code = "'["
			display = "'["
			system = "'["
			max_items = len(data["package"]["container"]['coding'])
			i = 0
			while i < max_items:
				code += json.dumps(data["package"]["container"]['coding'][i]['code'])+","
				display += json.dumps(data["package"]["container"]['coding'][i]['display'])+","
				system += json.dumps(data["package"]["container"]['coding'][i]['system'])+","
				i += 1
			code += "]'"
			display += "]'"
			system += "]'"
	packageInsert= "INSERT INTO MedPackage VALUES ("+medID+","+text+","+code+","+display+","+system+");"
	cur.execute(packageInsert)
	con.commit();
	cur.execute("SELECT * FROM MedPackage;")
	print "\n\n\n\nPrinting out the complete list of Packages!!"
	print cur.fetchall()
	if 'content' in data["package"]:
		parsePackageContent(cur,con,data,medID)
	return

def parsePackageContent(cur,con,data,medID):
#
	itemDisplay = 'NULL'
	ammountValue = 'NULL'
	ammountSystem = 'NULL'
	ammountUnit = 'NULL'
	if "item" in data["package"]["content"][0]:
		max_items = len(data["package"]["content"])
		i = 0
		while i < max_items:
			itemDisplay = json.dumps(data["package"]["content"][i]["item"]["reference"])
			if "amount" in data["package"]["content"][i]:
				# ammountType = "'numerator'"
				ammountValue ="'" + json.dumps(data["package"]["content"][i]["amount"]["value"]) + "'"
				ammountSystem ="'" + json.dumps(data["package"]["content"][i]["amount"]["system"]) + "'"
				ammountUnit ="'" +json.dumps(data["package"]["content"][i]["amount"]["code"]) + "'"
				contentInsert = "INSERT INTO PackageContent ("+medID+","+itemDisplay+","+ammountValue+","+ammountUnit+","+ammountSystem+");"
				cur.execute(ingredientInsert)
				con.commit();	
			i += 1
		cur.execute("SELECT * FROM PackageContent;")
		print "\n\n\n\nPrinting out the complete list of contents!"
		print cur.fetchall()
#MONSTERS ABOVE



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
				data = json.load(data_file)
				dataTest = json.dumps(data)
				# print "DATA TEEEEEEEEEST\n\n\n\n\n\n"
				# print dataTest
				# print "DATATATAATATATA"
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
		
		