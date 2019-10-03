#!/usr/bin/python3

# extract a training dataset for NER training, using regular expressions
# Entity: KBO/BCE number
# run as: python3 extract-kbo.py >> trainingdata-kbo.txt
# output: on the command line (pipe to file to save)
# Author: Joachim Ganseman

import os
import re

# printing functionality put in separate file
from printfortrainingdata import printmatch

encoding = "utf-8"
entityname = "KBO"

# define and compile regex to extract
p = re.compile(u'\d{4}\.\d{3}\.\d{3}')

# iterate over all files 
directory = "../cassweb/text-xpdf-split/"
files = [i for i in os.listdir(directory) if i.endswith("txt")]

for f in files:
	#print("Processing file", f)
	with open(directory+f, "r") as currentfile:
		for line in currentfile:
			mymatch = p.search(line.strip())		# use search to match anywhere in the string
			if mymatch:
				printmatch(mymatch, entityname)



	

