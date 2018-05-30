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

for i in comlist:
    commodity=''.join(i[0]) 
    value=''.join(i[1]) 
    flag= quandl.get(value)
    flag.columns=['price']
    flag['commodity']=commodity
    flag['lag52'] = flag['price'].shift(52)
    lastrow=flag.tail(1)
    #All commodity prices
    comprices = comprices.append(flag, ignore_index=False)
    compriceslast = compriceslast.append(lastrow, ignore_index=False)
    print compriceslast
