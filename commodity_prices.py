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
['platinum','COM/PL_EFP'],
['gold','COM/AU_LPM'],
['coffee','COM/COFFEE_BRZL'],
['cotton','COM/COTTON'],
['silver lmba','COM/AG_USD'],
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
 

    
compriceslast.to_csv('Desktop\comm.csv')
