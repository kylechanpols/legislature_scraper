import os, ssl
import re
import certifi
import time
from pathlib import Path
import urllib.request as urllib
import requests

##### SSL cert stuff
#if (not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None)):
#    ssl._create_default_https_context = ssl._create_unverified_context

##### DOWNLOADING FILES #####
os.chdir(r'***your path here***') #windows
#os.chdir(r'/Users/kylechan/Google Drive/Research/ma thesis - immigration and regionalist party competition/legislative proceedings') #macos
DOWNLOADS_DIR = Path(r'***your path here***') #download directory!
#DOWNLOADS_DIR = Path(r'/Users/kylechan/Google Drive/Research/ma thesis - immigration and regionalist party competition/legislative proceedings/data/Catalonia') #macos
# For every line in the file
for url in open('out_cat.txt').read().splitlines(): #change this for each output you got from scrapping
    # Split on the rightmost / and take everything on the right side of that
    # Combine the name and the downloads directory to get the local filename
    try:
        x = re.search('p\/.*', url)
        to_write = x.group(0).replace("/","_")
        to_write = to_write.replace("p_","")
        print("On to: "+ to_write)
        if x:
            filename = os.path.join(DOWNLOADS_DIR, to_write)
            filename = filename.replace("?","_")

            # Download the file if it does not exist
            if not os.path.isfile(filename):
            #v2 . using the requests library
                request = requests.get(url, verify=False, timeout=100, stream=True)
                with open(filename, 'wb') as fh:
                    try:
                        fh.write(request.content)
                        print("Sleeper: Writing complete. Now sleeping 5 seconds.")
                        time.sleep(5)
                    except:
                        print("ERROR: Server refuses to connect! Retrying in 60 secs.")
                        time.sleep(60)
    except:
        pass
#v1. using urlretrieve from urllib. THIS DOES NOT ALLOW TIMEOUT settings. This will literally take forever if the connection has timed out.
#try:
#    print("Downloading "+ to_write)
#    urllib.urlretrieve(url, filename, timeout= 5)
#    print("Sleeper: sleep 5 seconds.")
#    time.sleep(5) #the Catalonia website has some sort of built-in ping protection. Sleep 3 seconds per doc.
#except:
#    print("ERROR: Server refuses to connect. Retrying in 60 secs.")
#    time.sleep(60)
