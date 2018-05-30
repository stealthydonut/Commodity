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
#Get the Quandl Data
###################

rice = quandl.get("COM/RICE_2")
rice.columns=['rice']
rice['ind']=rice.index 
paladium = quandl.get("COM/PA_EFP")
paladium.columns=['paladium']
paladium['ind']=paladium.index 
platinum = quandl.get("COM/PL_EFP")
platinum.columns=['platinum']
platinum['ind']=platinum.index     
coffee = quandl.get("COM/COFFEE_BRZL")
coffee.columns=['coffee']
coffee['ind']=coffee.index         
        
df1=paladium.merge(rice, on='ind', how='outer')
df2=df1.merge(platinum, on='ind', how='outer')
df3=df2.merge(coffee, on='ind', how='outer')

test=df3.sort_values('ind')
print rice
print test
