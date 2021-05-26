"""


@author: Kyle
"""

#to do: automatically get links from .asp
#example:
#http://www.consiglio.regione.taa.it/it/banche-dati/resoconti-stenografici.asp?somepubl_action=300&somepubl_image_id=304867
#every PDF has the string "sompubl_action=300" in the middle. We can use BeautifulSoup to decompose the HTML, then use regex to pinpoint the links
#Then we download with requests.

import re
import requests
from bs4 import BeautifulSoup
import os
import urllib

fit = ""
for i in range(1,67): #manually determine number of pages.
    r = requests.get('http://www.parlament.cat/web/documentacio/publicacions/diari-ple/index.html?p_pagina='+ str(i), verify=False) #shortcut to loop over 25 pages of data
    soup = BeautifulSoup(r.text, "html.parser") #parse the page with bs4
    for j in soup.find_all('table'): #tell soup to find all tables
            for anchor in j.findAll('a'):
                try:
                    href = anchor['href']
                    if re.search('^DSPC-P', anchor.text): #Only interested in full text (stenographic report.)
                        #print(href)
                        fit = fit+ "http://www.parlament.cat" + href + os.linesep #we've located the link we need, and write to the output
                except KeyError:
                    pass

print(fit) #show the output

with open('output_cat.txt', mode='a') as f:
    f.write(fit) #write to output
