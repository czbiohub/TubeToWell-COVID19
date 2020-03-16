#!/usr/bin/env python3

import argparse
import csv
import time 


class TubeToWell:
	def __init__(self):

		# at startup ask for the user name and well barcode
		self.timestr = time.strftime("%Y%m%d-%H%M%S")
		self.parser = argparse.ArgumentParser()
		self.parser.add_argument('-n', '--name',  help="input user name", required=True)
		self.parser.add_argument('-b', '--barcode',  help="barcode number",  required=True)
		self.args = self.parser.parse_args()
		print("user: " + self.args.name)
		print("deep well barcode: " + self.args.barcode) #this should check if it's a valid plate barcode
		print("date: " + self.timestr)
		self.metadata = [['date', self.timestr], ['name', self.args.name], ['deep well barcode', self.args.barcode]]

		# make a list of the well row characters
		self.well_rows = [chr(x) for x in range(ord('A'), ord('H') + 1)] # move to state machine
		# make a list of well names in column wise order 
		self.well_names = []
		for letter in self.well_rows:
			for i in range(1,13):
				self.well_names.append(letter+str(i))
		self.well_names_iterator = iter(self.well_names)

		# make a dictionary with the tube locations as the key and the barcodes as the value
		self.tube_locations = {}
		for w in self.well_names:
			self.tube_locations[w] = None

		# the csv filename will be unique from scan time - confirm with Rafael how to decide filename
		with open(self.timestr+'.csv', 'a', newline='') as csvFile:
			writer = csv.writer(csvFile)
			writer.writerows(self.metadata)

		self.scanned_tubes = []

	def checkBarcode(self, check_input):
		print('barcode:' + check_input)
		
		# the user can only end the protocol by scanning the well plate again, however they cannot end the protocol if there were no tubes scanned
		# while check_input != self.args.barcode or not self.scanned_tubes:
			# find a way to make sure inputs came from barcode
		# check if the barcode was already scanned
		if check_input == self.args.barcode:
			print('this is the plate barcode')
			return False
		elif check_input in self.scanned_tubes:
			print('this tube was already scanned')
			return False
			# light up corresponding well
		# write to csv if it is a new barcode
		else: 
			with open(self.timestr+'.csv', 'a', newline='') as csvFile:
				row = [[check_input]]
				writer = csv.writer(csvFile)
				writer.writerows(row)
				self.scanned_tubes.append(check_input)
				self.tube_locations[next(self.well_names_iterator)] = check_input
			return True

