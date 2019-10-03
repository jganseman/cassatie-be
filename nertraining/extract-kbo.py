#!/usr/bin/python3

# extract a training dataset for NER training, using regular expressions
# Entity: KBO/BCE number
# run as: python3 extract-kbo.py >> trainingdata-kbo.txt
# output: on the command line (pipe to file to save)
# Author: Joachim Ganseman

import os
import re

encoding = "utf-8"
entityname = "KBO"

# define and compile regex to extract
p = re.compile(u'\d{4}\.\d{3}\.\d{3}')

# iterate over all files 
directory = "../cassweb/text-xpdf-split/"
files = [i for i in os.listdir(directory) if i.endswith("txt")]

# function taking a regex match and printing it out to use for spaCy training
# format: (u"Uber blew through $1 million a week", {"entities": [(0, 4, "ORG")]}),
def printfortrainingdata(mymatch):
	
	# create match tuple
	matchdef = ( str(mymatch.start()) , str(mymatch.end()), entityname )
	
	# put it into an entity json array
	myent = {'entities': [ matchdef ]}	
	
	# combine with source string into a tuple
	# do not strip() the string here, as that will screw up matched start and end positions
	mytuple = (mymatch.string, myent)  
	
	# print to command line
	print(mytuple, ',', sep='')

	# todo UTF encoding seems OK in Python3 (not Python2), but u"" signifier is not printed.
	# for the moment, considering that harmless

for f in files:
	#print("Processing file", f)
	with open(directory+f, "r") as currentfile:
		for line in currentfile:
			mymatch = p.search(line.strip())		# use search to match anywhere in the string
			if mymatch:
				printfortrainingdata(mymatch)



	

