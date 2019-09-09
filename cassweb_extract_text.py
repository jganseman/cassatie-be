#!/usr/bin/env python
# coding: utf-8
# author: Joachim Ganseman

### Extract text from pdfs downloaded from cassation website
# To use xpdf (pdftotext), first run "sudo apt install poppler-utils"
# To use PyPDF, first run "conda install -c conda-forge pypdf2"
# To use pdf2txt, first run "conda install -c conda-forge pdfminer.six"

### Default to xpdf (pdftotext). Other sections commented in the code --> uncomment them to activate

### Tesseract installation notes:
# 1. run "sudo apt-get install tesseract-ocr libtesseract-dev" OR "sudo snap install --channel=edge tesseract"
#    OR finer: "sudo apt-get install tesseract-ocr-nld tesseract-ocr-fra tesseract-ocr-deu tesseract-ocr-script-latn libtesseract-dev"
# 2. find the most recent version of pytesseract on https://anaconda.org/search?q=pytesseract 
# 3. run e.g. "conda install -c phygbu pytesseract"



from os import listdir, rename, system, makedirs, getcwd
from os.path import isfile, join, exists, getsize
from subprocess import Popen, PIPE, TimeoutExpired
import shutil
import re
import multiprocessing

#import numpy as np
#import pandas as pd
#import PyPDF2
#from PIL import Image, ImageSequence
#import pytesseract


dataroot = getcwd()
dataset = "cassweb"
PDF_DIR = join(dataroot, dataset)
filepath = PDF_DIR
pdf_list = [file for file in listdir(filepath) if ".pdf" in file]      # if "2014" in file]  
pdf_list = list(filter(None, pdf_list))              # remove any empty results
print(len(pdf_list), pdf_list)


### OPTION 1 : use PyPDF. Uncomment this section to activate

# # Reworked version of the earlier single-process PyPDF2 OCR routine
# # note: processing a single PDF can easily take 30 seconds
# # Now IMPROVED(tm) for parallel processing in python --> 10 times faster

# # Set directory for results of this function
# RESULT_DIR = join(dataroot, dataset, "text-pypdf2")
# if not exists(RESULT_DIR):
    # print("Created directory ", RESULT_DIR)
    # makedirs(RESULT_DIR)

# # First, define a function to run on a single file
# def text_from_pdf_parallel(mypdf):
    # print("Extracting text from file ", mypdf)
    # fullfilename = join(filepath,mypdf)
    
    # fileObj = open(fullfilename, 'rb')
    # PDFreader = PyPDF2.PdfFileReader(fileObj)
    # text = ''
    # for page in PDFreader.pages:    # eventually constrain [0:3]
        # text += '\n' + page.extractText()
    # fileObj.close()
    
    # if text == None:
        # pass
    # else:
        # mytxt = mypdf[:-3] + 'txt'
        # #mode = 'a' if exists(join(filepath,txt)) else 'w'
        # mode = 'w'
        # with open(join(RESULT_DIR,mytxt), mode) as f:
            # f.write(text)

# # Then, do the actual processing on all files
# pool = multiprocessing.Pool(20)
# pool.map(text_from_pdf_parallel, pdf_list)


### OPTION 2 (DEFAULT) : use pdftotext command line tool (Xpdf / poppler)
# --> these results are already much better
# and: takes only about 2 seconds/file

# command line options: http://www.xpdfreader.com/pdftotext-man.html  
# (-layout could be interesting)

RESULT_DIR_2 = join(dataroot, dataset, "text-xpdf")
if not exists(RESULT_DIR_2):
    print("Created directory ", RESULT_DIR_2)
    makedirs(RESULT_DIR_2)

# NEW: Also parallelized. Define function:
def use_xpdf_parallel(mypdf):
    print("Running xpdf text convertor on ", mypdf)
    mycommand = "pdftotext " + join(PDF_DIR,mypdf) + " " + join(RESULT_DIR_2, mypdf[:-3]+"txt")
    system(mycommand)    

# Then, do the actual processing on all files
# pdf_list was already defined
pool = multiprocessing.Pool(20)
pool.map(use_xpdf_parallel, pdf_list)

# note: uses an external process that might hang? If so, interrupt kernel and retry


### OPTION 3: pdf2txt (pdfminer.six) Uncomment this section to activate.
# note: easily takes 2 minutes per file!
# --> these results are maybe best (text order is better preserved)
# --> however, the hyphenation is not resolved, as it is in xpdf


# RESULT_DIR_3 = join(dataroot, dataset, "text-pdf2txt")
# if not exists(RESULT_DIR_3):
    # print("Created directory ", RESULT_DIR_3)
    # makedirs(RESULT_DIR_3)

# # also parallelized. First, define function
# def use_pdfminer_parallel(mypdf):
    # print("Running pdfminer pdf2txt.py text convertor on ", mypdf)
    # mycommand = "pdf2txt.py -o " + join(RESULT_DIR_3, mypdf[:-3]+"txt") + " " + join(PDF_DIR,mypdf)
    # system(mycommand)    

# # Then, do the actual processing on all files
# # pdf_list was already defined
# pool = multiprocessing.Pool(20)
# pool.map(use_pdfminer_parallel, pdf_list)
