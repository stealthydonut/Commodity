#This program will get the historical data for a number of tickers
import urllib
import pandas as pd
import numpy as np
import StringIO
import datetime
import sys
if sys.version_info[0] < 3: 
    from StringIO import StringIO as stio
else:
    from io import StringIO as stio

from google.cloud import storage
client = storage.Client()
bucket = client.get_bucket('oiltrade')
# Get the complete ticker list
blob = bucket.get_blob('all_alligator.csv')
content = blob.download_as_string()
inMemoryFile = StringIO.StringIO()
inMemoryFile.write(content)
#When you buffer, the "cursor" is at the end, and when you read it, the starting position is at the end and it will not pick up anything
inMemoryFile.seek(0)
df=pd.read_csv(inMemoryFile, low_memory=False)
# Append debt levels to the ticker list
blob = bucket.get_blob('oil_debtload.csv')
content = blob.download_as_string()
inMemoryFile = StringIO.StringIO()
inMemoryFile.write(content)
#When you buffer, the "cursor" is at the end, and when you read it, the starting position is at the end and it will not pick up anything
inMemoryFile.seek(0)
df2=pd.read_csv(inMemoryFile, low_memory=False)

#Append the files together





