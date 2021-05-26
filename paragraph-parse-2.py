# coding=utf-8
import os
from os import listdir
import io
from pathlib import PurePath
import re
import pandas as pd
#import openpyxl
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
session = "15e-parliament-2013-2018"

#Windows
src = PurePath('***your path here***'+session)

#MAC
#src =  PurePath('/Users/kylechan/Google Drive/Research/ma thesis - immigration and regionalist party competition/legislative proceedings/data/Bolzano/'+session)
#print(src)

files = [f for f in listdir(src) if f.endswith(".txt")] #list all files in the directory
#print(files)

#List of Regionalist MPs
#these are full names

#12e parliament
#regionalist = [u'Durnwalder Luis', u'Kasslatter Mur Sabina', u'Saurer Otto', u'Ladurner Martina', u'Laimer Michl',
#u'Berger Hans', u'Frick Werner', u'Thaler Zelger Rosa Maria', u'Pahl Franz', u'Atz Roland', u'Denicolò Herbert', u'Lamprecht Seppl', u'Hosp Bruno',
#u'Munter Hanspeter', u'Theiner Richard', u'Messner Siegfried', u'Stocker Martha', u'Baumgartner Walter', u'Feichter Arthur', u'Thaler Hermann',
#u'Pürgstaller Albert', u'Klotz Eva', u'Pöder Andreas', u'Willeit Carlo', u'Leitner Pius']

#13e parliament (2003-2008)
#regionalist = [u'Durnwalder Luis', u'Berger Hans', u'Kasslatter Mur Sabina', u'Mussner Florian', u'Pardeller Georg', u'Laimer Michl', u'Unterberger Julia',
#u'Widmann Thomas', u'Theiner Richard', u'Thaler Zelger Rosa', u'Stirner Brantsch Veronika', u'Saurer Otto', u'Pahl Franz', u'Frick Werner', u'Denicolò Herbert', u'Lamprecht Seppl', u'Hosp Bruno',
#u'Munter Hanspeter', u'Theiner Richard', u'Ladurner Martina', u'Stocker Martha', u'Baumgartner Walter', u'Feichter Arthur', u'Thaler Hermann',
#u'Pürgstaller Albert', u'Klotz Eva', u'Pöder Andreas', u'Leitner Pius', u'Mair Ulli']

#14e parliament (2008-2013)
#regionalist = [u'Durnwalder Alois', u'Berger Johann Karl', u'Leitner Pius', u'Mair Ulli', u'Pichler Elmar', u'Theiner Richard', u'Mussner Florian',
#u'Widmann Thomas', u'Schuler Arnold', u'Stocker Martha', u'Kasslatter Mur Sabina', u'Laimer Michael Josef', u'Stirner Brantsch Veronika', u'Egartner Christian',
#u'Lamprecht Seppl', u'Hochgruber Maria Magdalena', u'Klotz Eva', u'Zelger Thaler Rosa Maria', u'Steger Dieter', u'Tinkhauser Roland', u'Noggler Josef',
#u'Pardeller Georg', u'Knoll Sven', u'Unterberger Juliane', u'Munter Hanspeter', u'Baumgartner Walter', u'Von Dellemann Otto', u'Ladurner Martina',
#u'Stocker Sigmar', u'Egger Thomas', u'Pöder Andreas', u'Artioli Elena']

#15e parliament (2008-2013)
regionalist= [u'Kompatscher Arno', u'Leitner Pius', u'Schuler Arnold', u'Mair Ulli', u'Theiner Richard', u'Stocker Marhta', u'Achammer Philipp', u'Widmann Thomas', u'Mussner Florian', u'Tinkhauser Roland',
u'Klotz Eva', u'Noggler Josef', u'Knoll Sven', u'Deeg Waltraud', u'Steger Dieter', u'Hochgruber Kuenzer Maria Magdalena', u'Stocker Sigmar', u'Renzler Helmuth', u'Amhof Magdalena', u'Tschurtschenthaler Christian',
u'Stirner Brantsch Veronika', u'Wurzer Albert', u'Schiefer Oswald', u'Blaas Walter', u'Pöder Andreas', u'Zimmerhofer Bernhard', u'Oberhofer Tamara', u'Zingerle Hannes', u'Atz Tammerle Myriam']
[x.encode('utf-8') for x in regionalist]
#print(regionalist)

#Split them into first and last names:

#get names:
#this version helps split names with more than one word.
lastout = []
firstout = []
for i in regionalist:
    tmp = str(i)
    last, first = tmp.split(" ",1)
    if (len(tmp.split(" ")) > 2 and tmp.split(" ")[1] == "Von"):
        tmp = tmp.split(" ",3)
        last = join(tmp[1], tmp[2])
        first = tmp[3] #to deal with German last names that start with "Von"
    last.encode('utf-8')
    lastout.append(last)
    first.encode('utf-8')
    firstout.append(first)

#print(lastout, file=utf8stdout)


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

#MAC
#outpath = PurePath('/Users/kylechan/Google Drive/Research/ma thesis - immigration and regionalist party competition/legislative proceedings/data/Bolzano/bolzano_paragraph_15eparliament.xlsx')

#Windows
outpath = PurePath('***your path here***/bolzano_paragraph_15eparliament.xlsx')
df.to_excel(outpath, encoding="utf-8")
