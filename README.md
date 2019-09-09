# cassatie-be
Dutch language NLP dataset for legaltech applications


## Introduction

LegalTech is a booming field, a very text intensive one too. The text is often complicated and drawn out (nobody reads court filings for some light bedtime reading), 
which makes that existing language models, largely built on accessible text from Wikipedia or social media, don't really capture the peculiarities of "legalese".
Large databases of "real-life" legal documents are rare, not in the least because of obvious privacy issues, and especially in languages other than English.

In the context of doing some experiments with Named Entity Recognition on Dutch language legal texts in Belgium, I found a dataset published by the Cassation court of Belgium,
which the scripts in this repository scrape and preprocess into a set of 9786 text files of individual decisions by that court. Could be useful as (part of a) 
training set for a Dutch language model tailored to legal applications.


## The dataset

Can be downloaded as zip file in the main folder of this repository: ```cassatie-be.zip``` 


## Requirements

To build the dataset yourself, you need Python and Firefox installed. 
These scripts were developed on an Ubuntu 18.04 Linux machine, it's not guaranteed to work on other platforms (but feel free to contribute!) 

These scripts rely on a few dependencies for scraping. If you use Conda for your Python environment, first run:
``` conda install selenium ``` 
and ``` conda install -c conda-forge geckodriver ```
If you don't use conda, check the websites of these projects for appropriate installation instructions.

For text extraction out of PDF-files, the project relies on the command-line tool ```pdftotext```.
To use it, run ```sudo apt install poppler-utils```.

A PyPDF alternative is available in the code, to use that, run ```conda install -c conda-forge pypdf2``` and uncomment the appropriate section in ```cassweb_extract_text.py```.
A pdf2txt alternative is also available, to use that, run ```conda install -c conda-forge pdfminer.six``` and uncomment the appropriate section in ```cassweb_extract_text.py```.



## Running the project

1. Clone this repository
2. Navigate to its main directory using the terminal
3. Run ```python3 cassweb_download.py``` --> Firefox will launch and download a bunch of pdf files into a subfolder named ```cassweb```.
4. Run ```python3 cassweb_extract_text.py``` --> Will extract all text from these files into a subfolder ```cassweb/text-xpdf```.
5. Run ```python3 cassweb_splitarrests.py``` --> Will split those files into individual arrests into a subfolder ```cassweb/text-xpdf-split```.


## Known limits

The data only consists of Dutch-language verdicts from the Belgian cassation court, which is limited in its scope: it only judges whether a trial followed the correct procedures.
It never judges about the content of the actual case: for that decision it will refer a case to a different court (or not if it does not find any procedural mistakes).
The content of the text is therefore highly about procedural matters.

While the court archives date back for centuries, the text that can be reliably detected (was encoded digital-native) starts from the year 2000 onwards.

Not all rulings can be extracted separately: formatting errors in the source files make that splitting the books into individual cases is not always obvious.
For now I just roughly deleted cases that I couldn't split off automatically, so the final dataset lacks 5% to 10% of the total published number of cases. 
This still leaves enough to build a language model for this particular branch of judicial texts.


## Notes

Seems like arrests can also be downloaded individually from links of the form: http://jure.juridat.just.fgov.be/pdfapp/download_blob?idpdf=N-20150217-5
where idpdf contains: N/F (language), date of arrest, sequential number of arrest, starting from 1, up to ? 
Potential to scrape a bigger dataset? However, these might be only partially or not anonymized.  
