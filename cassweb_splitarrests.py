#!/usr/bin/env python
# coding: utf-8
# author: Joachim Ganseman

### Split the OCR-ed Cassation arrests into separate arrests
# This currently works for arrests from the year 2000 onwards.
# Split done by regex, based on formatting as outputted from the xpdf tool
# 
# Still needs work to be more complete!

from os import listdir, path, remove, makedirs, getcwd
from os.path import join, exists
import math
import time
import unicodedata
import re


dataroot = getcwd()
dataset = "cassweb"
TXT_DIR = join(dataroot, dataset,"text-xpdf")
OUTPUT_DIR = join(dataroot, dataset,"text-xpdf-split")# to save the resulting model
if not exists(OUTPUT_DIR):
    print("Created directory ", OUTPUT_DIR)
    makedirs(OUTPUT_DIR)


# too many special characters in there, also because of OCR errors. Limit to plain ASCII
def unicodeToAscii(s):
    return ''.join(
        c for c in unicodedata.normalize('NFD', s)
        if unicodedata.category(c) != 'Mn' and ord(c) < 128
    )

# note: pattern must contain 1 subgroup, style (foo(bar)):
# as the number of matches is used to iterate through the document
def splitarrests(filelist, pattern, numberpattern):
    for myfile in filelist:
        with open(join(TXT_DIR,myfile), 'r') as f:
            filecontent = f.read()
            arrestssplitted = re.split(pattern, filecontent)     # split file into separate arrests
            for i, text in enumerate(arrestssplitted): 
                # print(text.replace('\n', '*')[:50])         # print output to get idea of the regex capturing groups

                # if line i matches the regex completely, skip i+1 (kamer), and add i+2
                if re.match(pattern, text):
                    currentarrest = text.strip()
                    currentarrest += arrestssplitted[i+2].strip().replace("\n\n", "\n")
                    # currentarrest = unicodeToAscii(currentarrest).replace('\x0c', '\n').replace('_', '-')    # leave this to reader

                    # get the arrest number
                    arrestnumber = re.match(numberpattern, text).group(1)
                    newfilename = myfile.replace(".txt", "-"+arrestnumber+".txt")
                    print("writing arrest " + arrestnumber + " to file " + newfilename)
                    with open(join(OUTPUT_DIR,newfilename), 'w') as f2:
                        f2.write(currentarrest)


# segment and preprocess the data
# for xpdf processed files: each new arrest is marked by e.g. "N° 7 \n x°" where x=1/2/3/V (kamernr / verenigd)


### PART 1 
# split the files from 2014_06 until 2015_05
# sort and only do a selection
text_list = sorted([file for file in listdir(TXT_DIR) if 'ac' in file])
print(text_list)

# they use the following pattern:
pattern = "(N[°or]\.?\s*\d{1,4}\n([123][°oe•]|[Vv]))" #"(N°\s*\d{1,3}\n[123V]°)"
numberpattern = "N[°or]\.?\s*(\d{1,4})"
# still misses a few, e.g. N° 132 from ac_2015_03.txt

splitarrests(text_list, pattern, numberpattern)


### PART 2
# split the rest of the files: 2012_01 only
# Encoded differently in pdf, hence decoded differently by xpdf?
text_list = sorted([file for file in listdir(TXT_DIR) if 'ac' in file])
text_list = text_list[0]
print(text_list)

# they use the following pattern:
pattern = "(N°\s*\d{1,4}\n(\d{1,2}.\d{1,2}.12))" # Number of arrest, with date on next line
numberpattern = "N°\s*(\d{1,4})"

splitarrests([text_list], pattern, numberpattern)


### PART 3
# split files of the form AC-2002-01 up to AC-2011-12

text_list = sorted([file for file in listdir(TXT_DIR) if 'AC' in file and 'Reg' not in file])
print(text_list)

# they use the following pattern:
pattern = "(N[°or]\.?\s*\d{1,4}\n([123][°oe•]|[Vv]))" #"(N°\s*\d{1,3}\n[123V]°)"
numberpattern = "N[°or]\.?\s*(\d{1,4})"

splitarrests(text_list, pattern, numberpattern)


### PART 4
# arrests from 2000-01 to 2001-10
# note that these do not follow naming by month

text_list = sorted([file for file in listdir(TXT_DIR) if ('2000' in file or '2001' in file) and not '11' in file])
print(text_list)

# they use the following pattern:
pattern = "(N[°or]\.?\s*\d{1,4}\n([123][°oe•]|[Vv]))" #"(N°\s*\d{1,3}\n[123V]°)"
numberpattern = "N[°or]\.?\s*(\d{1,4})"

splitarrests(text_list, pattern, numberpattern)


### END
# arrests from 1999 and before are published in 2-column format.
# while the OCR did a fairly good job in following the columns, it probably still fails too often to be useful here
# so stopping here for now


### POSTPROCESSING: delete erroneously splitted arrests (still 2 arrests in the same file)
# There are never more than 1000 arrests per year
maxArrestsPerYear = 1000
beginyear=2000
endyear=2015
removefile=True

for currentyear in range(beginyear, endyear+1):

    #select all files containing years within the range specified above
    text_list = [file for file in listdir(OUTPUT_DIR) if str(currentyear) in file]

    # files have a suffix that should be increasing by 1. If there is a gap, remove the previous file from the list 
    # as that file will contain multiple arrests (was not splitted properly)
    previousOK = -1
    for i in range(1,maxArrestsPerYear):
        filenamesuffix = "-" + str(i) + ".txt"
        if any(filenamesuffix in filename for filename in text_list):
            previousOK = i
        else:
            if previousOK > 0:
                # arrest not found? it's still part of the previous one: remove the previous file from consideration
                toremovesuffix = "-" + str(previousOK) + ".txt"
                previousfile = [s for s in text_list if toremovesuffix in s]   # note this is an array
                if previousfile and previousfile[0] in text_list:    # only remove if not already removed
                    text_list.remove(previousfile[0])
                    if removefile:
                        remove(join(OUTPUT_DIR, previousfile[0]))
                        print("Removed erroneously splitted arrest ", previousfile[0])
                    else:
                        print("Not considering possibly erroneously splitted arrest ", previousfile[0])

# now text_list only has clean arrests. 
