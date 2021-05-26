# coding=utf-8
import os
from os import listdir
import io
from pathlib import PurePath
import re
import pandas as pd
import openpyxl
# Example: Single-case
# os.chdir(dir) #define working directory.

#Objective:
#Write up a bot to extract paragraphs of text in the stenographic report. Each MP's statement will be presented by their last name in all caps, followed by :, and the pdf scraper noted the paragraphs by . followed by two spaces.
#Psuedocode:
#1. For each parliamentary session, we have a fixed list of MPs represented in a regional parliament. Create this list, save this list as a python list.
#2. Load up the files: Loop through the entire txt directory and then loop through each document in the directory:
    #3. For each document, loop through the regionalist MP list. Find and extract all statements made by this MP, even if its procedural (clean them by hand afterwards.)
#4. Attach name of file for reference
#5. Output as .csv or .txt


#######The 11th parliament (1993-1998).##########
#TAA numbers run from TAA-3.pdf to TAA-178.pdf

######setup######
#routine to print in utf-8 -  DO NOT CHANGE!!!
utf8stdout = open(1, 'w', encoding='utf-8', closefd=False) # fd 1 is stdout


#####IO######
session = "11e-parliament-1993-1998"

#Windows
#src = PurePath('C:/Users/Kyle/Google Drive/Research/ma thesis - immigration and regionalist party competition/legislative proceedings/data/Bolzano/'+session)

#MAC
src =  PurePath('***your path here***'+session)
#print(src)

files = [f for f in listdir(src) if f.endswith(".txt")] #list all files in the directory
#print(files)

#List of Regionalist MPs
#these are full names
regionalist = [u'Durnwalder Luis', u'Brugger Siegfried', u'Messner Siegfried', u'Atz Roland', u'Achmüller Erich', u'Mayr Sepp', u'Kasslatter Mur Sabina', u'Sour Otto', u'Kofler Alois',
u'Feichter Arthur', u'Berger Hans', u'Frick Werner', u'Merry Hanspeter', u'Frasnelli Hubert', u'Laimer Michl', u'Mayr Christine', u'Denicolò Herbert', u'Peterlini Oskar', u'Hosp Bruno',
u'Pahl Franz', u'Waldner Christian', u'Tarfusser Ulrike', u'Leitner Pius', u'Klotz Eva', u'Benedikter Alfons', u'Willeit Carlo']
[x.encode('utf-8') for x in regionalist]
#print(regionalist)

#Split them into first and last names:

#last name:
lastout = []
for i in regionalist:
    tmp = str(i)
    last, first = tmp.split(" ",1)
    last.encode('utf-8')
    lastout.append(last)

#print(lastout, file=utf8stdout)

#probably dont need this, but this is possible: get first names
firstout = []
for i in regionalist:
    tmp = str(i)
    last, first = tmp.split(" ",1)
    first.encode('utf-8')
    firstout.append(first)

#the main Loop
#3 outputs:
#document name
#last name
# and the extract variable (statements)
os.chdir(src) #not necessary
#print(lastout)

#init vars
out = []
docname = []
mpname = []
mpfirst = []
meta = []
checkmeta = True
def match(val, testlist):
    for i,x in enumerate(testlist):
        if (x == val):
            return i

#main loop:
#document-level, check every time we move to a new doc.
#paragraph approach (with re.finditer returning paragraphs)
#using re to split things into paragraphs, then find if the speaker spoke in that paragraph. return the paragraph if the speaker is identified.
for i in files:
    with io.open(i, "r", encoding='utf-8') as f:
        txt = f.read()
        checkmeta == True
        para_pat = re.compile('(?s)((?:[^\n][\n]?)+)', re.M | re.DOTALL | re.U)
        for para in re.finditer(para_pat, txt): #match paragraphs
            #print("DEBUG: Checking paragraph:" + str(para))
            if checkmeta == True: find_meta = re.search('^.*SEDUTA.*$', txt, re.IGNORECASE) #match meta data (looking for session info)

            for j in lastout:
                #print("DEBUG: checking for "+j)
                txt_pat = re.compile(j.upper()+'.*', re.M | re.DOTALL | re.U)
                extract = re.findall(txt_pat, para.group()) #match speaker

                if extract:
                    #print(extract)
                    docname.append(i) #return document name
                    mpname.append(j) #return MP last name
                    mpfirst.append(firstout[match(j, lastout)]) #return MP first name
                    out.append(extract) #return matched output (paragraph)

#put together a pandas df.
d = {'doc': docname, 'mp': mpname, 'mp_first':mpfirst, 'output' : out}
df = pd.DataFrame(data=d)

print(df.head())

outpath = PurePath('***your path here***/bolzano_paragraph_11eparliament.xlsx')
df.to_excel(outpath, encoding="utf-8")
