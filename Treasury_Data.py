#Source is from https://github.com/npezolano/PyTreasuryDirect/blob/master/README.md#
#requirs CUSIP, and ISSUE Date
#list of all identifiers for CUSIP https://www.treasurydirect.gov/instit/auctfund/work/auctime/auctime_securitiestable.htm
#the date is the issue date of the cusip number
#for a list of cusips and issue dates https://www.treasurydirect.gov/govt/reports/pd/mspd/2010/2010_jan.htm - this can be downloaded
#all of the cusips by year https://www.treasurydirect.gov/instit/annceresult/auctdata/auctdata_stat.htm
#https://www.treasurydirect.gov/instit/annceresult/press/preanre/preanre.htm -2018 cusips
#in excel form
import pandas as pd
import pandas as pd
from pytreasurydirect import TreasuryDirect
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

td = TreasuryDirect()
tdraw = pd.DataFrame()    
    
#Get the data from google cloud storage
from google.cloud import storage
client = storage.Client()
bucket = client.get_bucket('mastfiles')
# Then do other things...
blob = bucket.get_blob('cusip_list.csv')
content = blob.download_as_string()
#Because the pandas dataframe can only read from buffers or files, we need to take the string and put it into a buffer
inMemoryFile = StringIO.StringIO()
inMemoryFile.write(content)
#When you buffer, the "cursor" is at the end, and when you read it, the starting position is at the end and it will not pick up anything
inMemoryFile.seek(0)
#Note - anytime you read from a buffer you need to seek so it starts at the beginning
#The low memory false exists because there was a lot of data
df=pd.read_csv(inMemoryFile, low_memory=False)
df.drop_duplicates(subset=['cusipnum','cusipissuedate'], keep=False)
df['cudt'] =  pd.to_datetime(df['cusipissuedate'])
df['day'] = df['cudt'].dt.strftime("%d")
df['month'] = df['cudt'].dt.strftime("%m")
df['year'] = df['cudt'].dt.strftime("%Y")
df['/']='/'
df['cup_dt']=df['day']+df['/']+df['month']+df['/']+df['year']
dfdate=df['cup_dt']
df_date = [str(r) for r in dfdate]
dfvalue=df['cusipnum']
df_value = [str(r) for r in dfvalue]
#merge the list so that the value from list 1 is in first position and value from list 2 is in second position
dflist=zip(df_value,df_date)

for i in dflist:
    cusip =''.join(i[0]) 
    issuedate =''.join(i[1])
    try:
        cusip_value=(td.security_info(cusip, issuedate))
        dfraw = pd.DataFrame(cusip_value, index=['a']) 
        tdraw = tdraw.append(dfraw, ignore_index=False)
    except:
        print cusip
        print issuedate




