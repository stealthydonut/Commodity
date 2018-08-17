#Source is from https://github.com/npezolano/PyTreasuryDirect/blob/master/README.md#
#requirs CUSIP, and ISSUE Date
#list of all identifiers for CUSIP https://www.treasurydirect.gov/instit/auctfund/work/auctime/auctime_securitiestable.htm
#the date is the issue date of the cusip number
#for a list of cusips and issue dates https://www.treasurydirect.gov/govt/reports/pd/mspd/2010/2010_jan.htm - this can be downloaded
#in excel form
import pandas as pd
import pandas as pd
from pytreasurydirect import TreasuryDirect

td = TreasuryDirect()
tdraw = pd.DataFrame()

cusip_list=[['912796PS2','02/01/2018'],
['912796PS2','05/03/2018'],
['912796PS2','07/05/2018'],
['912796PU7','02/08/2018'],
['912796PU7','05/10/2018'],
['912796PU7','07/12/2018'],
['912796NQ8','08/17/2017'],
['912796NQ8','02/15/2018'],
['912796NQ8','05/17/2018'],
['912796NQ8','07/19/2018'],
['912796PV5','02/22/2018'],
['912796PV5','05/24/2018']]

#Build a dataframe that contains all of the treasury cusip numbers

for i in cusip_list:
    cusip =''.join(i[0]) 
    issuedate =''.join(i[1])
    cusip_value=(td.security_info(cusip, issuedate))
    df = pd.DataFrame(cusip_value, index=['a']) 
    tdraw = tdraw.append(df, ignore_index=False)

    
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
    print cusip
    print issuedate
    cusip_value=(td.security_info(cusip, issuedate))
    dfraw = pd.DataFrame(cusip_value, index=['a']) 
    tdraw = tdraw.append(dfraw, ignore_index=False)





df['good']=df['cusipissuedate'].str[:6]
df['char2']=df['cusipissuedate'].str[2:]


#Generate the cusip list
df['d']=df['cusipissuedate'].str[:2]
df['m']=df['cusipissuedate'].str[3:5]
df['y']=df['cusipissuedate'].str[6:]
df['y2'] = df['y'].astype(str).convert_objects(convert_numeric=True)
df['y3'] = np.where(df['y2']>20, '19', '20')
df["year"] = df["y3"].map(str) + df["y"]
df['/']='/'
df["day"] = df["d"].map(str) + df["/"]
df["month"] = df["m"].map(str) + df["/"]
df['daymonth'] = df['day'].map(str) + df['month']
df['cusipdate'] = df['daymonth'].map(str) + df['year']
df.__delitem__('d')
df.__delitem__('m')
df.__delitem__('y')
df.__delitem__('y2')
df.__delitem__('y3')
df.__delitem__('/')
df.__delitem__('month')
df.__delitem__('day')
df.__delitem__('Date')
df.__delitem__('year')
df.__delitem__('daymonth')
df2=df[df['cusipdate'].notnull()]
df3=df2[df2['CUSIP'].notnull()]
df_date=df3['cusipdate']
df_value=df3['CUSIP']
dfdatelist=df_date.values.T.tolist()
dfvaluelist=df_value.values.T.tolist()  
#merge the list so that the value from list 1 is in first position and value from list 2 is in second position
dfcusipdatelist=zip(dfdatelist, dfvaluelist)

#Build a dataframe that contains all of the treasury cusip numbers

for i in dfcusipdatelist:
    cusip =''.join(i[0]) 
    issuedate =''.join(i[1])
    cusip_value=(td.security_info(cusip, issuedate))
    df = pd.DataFrame(cusip_value, index=['a']) 
    tdraw = tdraw.append(df, ignore_index=False)
