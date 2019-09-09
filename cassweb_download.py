#!/usr/bin/env python
# coding: utf-8
# author: Joachim Ganseman

### Download cassatie documents from their website
# first run "conda install selenium"
# first run "conda install -c conda-forge geckodriver"


from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from os import path, makedirs, listdir, rename, getcwd
from urllib import request, error

dataroot = getcwd()
dataset = "cassweb"
target_dir = path.join(dataroot, dataset)

mainurl = "https://justitie.belgium.be/nl/rechterlijke_orde/hoven_en_rechtbanken/hof_van_cassatie/documenten/arresten_van_cassatie"


# Launch browser and navigate to website
browser = webdriver.Firefox()
browser.implicitly_wait(30)  # wait for up to 30 seconds before throwing element not found errs
browser.get(mainurl)
elems = browser.find_elements_by_tag_name('a')

# extract all data as text NOW, because the browser object and its elements get invalidated once the browser connection is closed
hrefs = [ elem.get_attribute("href") for elem in elems ]

# create destination directory if needed
if not path.exists(target_dir):
    print("Created directory ", target_dir)
    makedirs(target_dir)
 
# download pdf files
for myhref in hrefs:
    #myhref = mylink.get_attribute("href")
    if "pdf" in myhref:
        print("Accessing ", myhref)
        filename = path.basename(myhref)
        if not path.exists(path.join(target_dir, filename)):
            try:
                pdfFile = request.urlopen(myhref)
                with open(path.join(target_dir, filename), 'wb') as file:
                    file.write(pdfFile.read())
                    file.close()
                print ("Saved ", path.join(target_dir, filename))
            except error.URLError as e:
                print("error: ", e.reason)
            except error.HTTPError as e:
                print("error: ", e.reason) 

# no more need for the browser anymore
browser.quit()

# do some cleanup of the filenames
for myfile in listdir(target_dir):
    newname = myfile.replace("%20", "-")
    newname = newname.replace("--", "-")
    newname = newname.replace("%5B", "[")
    newname = newname.replace("%5D", "]")
    
    # currently not doing the following, to keep some naming difference between the subcollections in this dataset:
    # newname = newname.replace("AC", "ac")
    # newname = newname.replace("_", "-")
    
    if (newname != myfile):
        print(myfile, " --> ", newname)
        rename(path.join(target_dir, myfile), path.join(target_dir, newname))

# end
