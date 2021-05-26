import PyPDF2
import os
from os import listdir
from os.path import isfile, join
import multiprocessing as mp #parallel computing
import json
import numpy as np

#for a single file
dir = '***your path here***'
newdir = "***your path here***"
tmp=""
tmp2="" #dont use lists. use string, then string split in R.
tmp3=""

#pdfFileObj = open(dir+'2005-19-1.pdf', 'rb') #open pdf file
#pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
#pagenumber = pdfReader.numPages
#print(range(pagenumber))
#tmp=""

#for i in range(pagenumber):
#    pageObj = pdfReader.getPage(i)
#    tmp = tmp + os.linesep+ pageObj.extractText()

#with open('converted.txt', 'a') as f:
#    f.write(tmp + os.linesep) #write to output

#now, loop over the entire data directory, save each page into text, so that we have a CORPUS.
onlyfiles = [f for f in listdir(dir) if isfile(join(dir, f))] #list all files in the directory
print(onlyfiles[1])
#print(type(onlyfiles))

def pdf2txt(i,tmp=tmp): #necessary for parallelizing. Take the loop on the top-level, then parallel process the actual conversion.
        #
            pdfFileObj = open(dir+i, 'rb') #open pdf file
            pdfReader = PyPDF2.PdfFileReader(pdfFileObj) #pass the file to the PdfFileReader
            pagenumber = pdfReader.numPages #get the number of pages
            print("DEBUG: Reading "+i) #show which file is being read.
            try:
                for j in range(pagenumber): #second loop : extract every single page, save to new file, and carry on
                    pageObj = pdfReader.getPage(j) #extract 1 page
                    tmp = tmp+ os.linesep+ pageObj.extractText() #save the context of a page to memory
                    print("DEBUG: Extracted text from page "+str(j) +" in Document "+i)
            except:
                print("Task failed successfully")

            with open(join(newdir,i+".txt"), 'w') as f: #write new file with what we've got
                print(i + " Converted and Saved sucessfully...")
                f.write(tmp + os.linesep) #write to output

def metadata(i,tmp2=tmp2,tmp3=tmp3):
    try:
        pdfFileObj = open(dir+i, 'rb')
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
        info = pdfReader.getDocumentInfo()
    #***stop: still don't know how to put the entire thing as part of an empty list and convert to pd df
    #print(info.creator)
        tmp2 = tmp2+","+i
        tmp3 = tmp3+","+info.creator #creation date
        print("DEBUG: Metadata for " + i + " extracted") #examine
    except:
        print("ERROR: Cannot get metadata for "+i)

        #out = np.asarray(tmp2,tmp3)

    #print(tmp2)
    #print(tmp3)
    return tmp2,tmp3
    #return out

#begin parallelizing
#1. text extraction
pool = mp.Pool(mp.cpu_count()-1) #how many CPUs?
print("Using "+ str(mp.cpu_count()-1)+ " Cores for parallelization")
pool.map(pdf2txt,[i for i in onlyfiles]) #tell the parallel workers to loop over the entire directory
pool.close() #remember to shut down the parallelization block when done

#2. metadata extraction
pool = mp.Pool(mp.cpu_count()-1)
results = pool.map(metadata,[i for i in onlyfiles]) #tell the parallel workers to loop over the entire directory
pool.close()
#results is a pair of file name and meta data.
print(results[1])

#write to file

with open(join(newdir,'meta.txt'), 'w') as filehandle:
    json.dump(results, filehandle) #in JSON format

#now data ready for analysis in R.
