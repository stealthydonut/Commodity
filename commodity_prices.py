#This file will display commodity prices in a graphical or tabular form in google data studio

import quandl
import urllib
import pandas as pd
import quandl
import urllib
import pandas as pd
import numpy as np
import StringIO
import datetime
import requests
import sys
from pandas.compat import StringIO
if sys.version_info[0] < 3: 
    from StringIO import StringIO as stio
else:
    from io import StringIO as stio
    
############
#Quandl Data
#############
quandl.ApiConfig.api_key = 'BVno6pBYgcEvZJ6uctTr'

####################################################
#Stage 1 - Build the list that will acquire the data
####################################################

wikicomlist=[['rice','COM/RICE_2'],
['coffee','COM/COFFEE_BRZL'],
['cotton','COM/COTTON'],
['cocoa','COM/COCOA'],
['hogs iowa','COM/HOGS'],
['us fed funds rate','COM/FEDFU'],
['copper commex','COM/COPPER'],
['aluminum','COM/AL_LME'],
['fertilizers index','COM/WLD_IFERTILIZERS'],
['iron ore','COM/WLD_IRON_ORE'],
['potash','COM/WLD_POTASH'],
['phosphate','COM/WLD_PHOSROCK'],
['banana','COM/WLD_BANANA_US'],
['beef','COM/WLD_BEEF'],
['chicken','COM/WLD_CHICKEN'],
['orange','COM/WLD_ORANGE'],
['wheat','COM/WLD_WHEAT_US_SRW'],
['soybeanns','COM/WLD_SOYBEANS'],
['natural gas','COM/WLD_NGAS_US'],
['oil','COM/WLD_CRUDE_BRENT']]

lmbacomlist=[['platinum','LPPM/PLAT'],['gold','LBMA/GOLD'],['paladium','LPPM/PALL']]

lmbacomlist1=[['silver','LBMA/SILVER']]

JMcomlist=[['JOHNMATT/RHOD','JOHNMATT/IRID','JOHNMATT/RUTH']]

#IRID = iridium
#RUTH = ruthenium

############################################################
#Stage 2 - Normalize the data so there is a consistent price
############################################################

dfwikiraw = pd.DataFrame()
dflmbaraw = pd.DataFrame()
dflmbaraw1 = pd.DataFrame()

#Wiki prices
for i in wikicomlist:
    commodity=''.join(i[0]) 
    value=''.join(i[1]) 
    dfwiki= quandl.get(value)
    dfwiki.columns=['price']
    dfwiki['commodity']=commodity
    dfwiki['ind']=dfwiki.index
    dfwikiraw = dfwikiraw.append(dfwiki, ignore_index=False)

#lmba prices    
for i in lmbacomlist:
    commodity=''.join(i[0]) 
    value=''.join(i[1]) 
    dflmba= quandl.get(value)
    dflmba.columns=['price','EUR AM','GBP AM','USD PM','EUR PM','GBP PM']
    dflmba['commodity']=commodity
    dflmba.__delitem__('EUR AM')
    dflmba.__delitem__('GBP AM')
    dflmba.__delitem__('USD PM')
    dflmba.__delitem__('EUR PM')
    dflmba.__delitem__('GBP PM') 
    dflmba['ind']=dflmba.index
    dflmbaraw = dflmbaraw.append(dflmba, ignore_index=False)

for i in lmbacomlist1:
    commodity=''.join(i[0]) 
    value=''.join(i[1]) 
    dflmba= quandl.get(value)
    dflmba.columns=['price','EUR AM','GBP AM',]
    dflmba['commodity']=commodity
    dflmba.__delitem__('EUR AM')
    dflmba.__delitem__('GBP AM')
    dflmba['ind']=dflmba.index
    dflmbaraw1 = dflmbaraw1.append(dflmba, ignore_index=False)

#append all the data together into one file

lmba=dflmbaraw.append(dflmbaraw1, ignore_index=True)
commodityraw=lmba.append(dfwikiraw, ignore_index=True)

#########################################################################
#Stage 3 - Iterate through the commodity to build the analytical data set
#########################################################################

#Create a list from a pandas dataframe variable

com_list=commodityraw.drop_duplicates(['commodity'], keep='last')
dflist = com_list['commodity'].tolist()

#sort by variable and date
com_list2=com_list.sort_values(['commodity','ind'])

#Generate the Analytical File
comprices = pd.DataFrame()
compriceslast = pd.DataFrame()
    

for i in dflist:  
    com_name=''.join(i) 
    #only include the current commodity 
    df = commodityraw[commodityraw['commodity']==com_name]            
    #Generate the calculations
    df['lag125'] = df['price'].shift(125)
    df['lag250'] = df['price'].shift(250)
    df['lag500'] = df['price'].shift(500)
    df['lag750'] = df['price'].shift(750)
    df['lag1000'] = df['price'].shift(1000)
    df['lag1250'] = df['price'].shift(1250)
    df['lag1500'] = df['price'].shift(1500)
    df['maxalltime'] = df['price'].max()
    df['minalltime'] = df['price'].min()
    #do the five year max and min
    lastrow1250=df.tail(1250)
    lastrow1250['max5year'] = lastrow1250['price'].max()
    lastrow1250['min5year'] = lastrow1250['price'].min()    
    #do the three year max and min
    lastrow750=lastrow1250.tail(750)
    lastrow750['max3year'] = lastrow750['price'].max()
    lastrow750['min3year'] = lastrow750['price'].min()
    #Gets the final row of data
    lastrow=lastrow750.tail(1)
    #Calculate percentages
    lastrow['6mochange']=(lastrow['price']/lastrow['lag125'])-1
    lastrow['1yrchange']=(lastrow['price']/lastrow['lag250'])-1
    lastrow['2yrchange']=(lastrow['price']/lastrow['lag500'])-1
    lastrow['3yrchange']=(lastrow['price']/lastrow['lag750'])-1
    lastrow['4yrchange']=(lastrow['price']/lastrow['lag1000'])-1
    lastrow['5yrchange']=(lastrow['price']/lastrow['lag1250'])-1
    lastrow['5yrmaxdiff']=(lastrow['price']/lastrow['max5year'])-1 
    lastrow['5yrmindiff']=(lastrow['price']/lastrow['min5year'])-1 
    lastrow['3yrmaxdiff']=(lastrow['price']/lastrow['max3year'])-1     
    lastrow['3yrmindiff']=(lastrow['price']/lastrow['min3year'])-1 
    #All commodity prices
    #comprices = comprices.append(df, ignore_index=False)
    compriceslast = compriceslast.append(lastrow, ignore_index=False)
 
  
 

##################################
#Put the dataset back into storage
##################################
from google.cloud import storage
client = storage.Client()
bucket2 = client.get_bucket('macrofiles')
df_out = pd.DataFrame(compriceslast)
df_out.to_csv('commodity_report.csv', index=False)
blob2 = bucket2.blob('commodity_report.csv')
blob2.upload_from_filename('commodity_report.csv')


    
#compriceslast.to_csv('Desktop\comm.csv')
