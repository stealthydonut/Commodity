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
####################
#Get the Quandl Data and build two files
#File 1 : all prices
#File 2 : the price changes over time - determine what commodity is cyclical
###################

comlist=[['rice','COM/RICE_2'],
['paladium','COM/PA_EFP'],
['platinum','COM/PL_EFP']]

comprices = pd.DataFrame()
compriceslast = pd.DataFrame()

comprices = pd.DataFrame()
compriceslast = pd.DataFrame()

for i in comlist:
    commodity=''.join(i[0]) 
    value=''.join(i[1]) 
    df= quandl.get(value)
    df.columns=['price']
    df['commodity']=commodity
    #Generate the calculations
    df['lag125'] = df['price'].shift(125)
    df['lag250'] = df['price'].shift(250)
    df['lag500'] = df['price'].shift(500)
    df['lag750'] = df['price'].shift(750)
    df['lag1000'] = df['price'].shift(1000)
    df['lag1250'] = df['price'].shift(1250)
    df['lag1500'] = df['price'].shift(1500)
    df['max'] = df['price'].max()
    df['min'] = df['price'].min()
    lastrow=df.tail(1)
    #All commodity prices
    comprices = comprices.append(df, ignore_index=False)
    compriceslast = compriceslast.append(lastrow, ignore_index=False)
