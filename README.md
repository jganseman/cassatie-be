# cassatie-be
Dutch language NLP dataset for legaltech applications

## Introduction

## Requirements
These scripts rely on a few dependencies to do scraping. If you use Conda for your Python environment, first run:
``` conda install selenium ```
``` conda install -c conda-forge geckodriver ```
If you don't use conda, check the websites of these projects for appropriate installation instructions.

You need to have Firefox installed

## Running the project
1. Clone this repository
2. Navigate to its main directory using the terminal
3. Run ```./cassweb_download.py``` --> Firefox will launch and download a bunch of pdf files into a subfolder named ```cassweb```.
