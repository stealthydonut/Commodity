#Yield Curve Analysis

#Compares gold returns with yeilds


from pandas.compat import StringIO
#Sourced from the following site https://github.com/mortada/fredapi
from fredapi import Fred
import StringIO
import quandl
import datetime as dt
import ast
import pandas as pd
import itertools
#import matplotlib
#import matplotlib.pyplot as plt
import sys
if sys.version_info[0] < 3: 
    from StringIO import StringIO as stio
else:
    from io import StringIO as stio

############
#Quandl Data
#############
quandl.ApiConfig.api_key = 'BVno6pBYgcEvZJ6uctTr'

##########
#Fred Data
##########
fred = Fred(api_key='4af3776273f66474d57345df390d74b6')

#############################################
#corporate bond yields and gold
#############################################
yield_list=[
('2Year Corp Yield','HQMCB2YRP'),
('5Year Corp Yield','HQMCB5YRP'),
('10Year Corp Yield','HQMCB10YRP'),
('30Year Corp Yield','HQMCB30YRP')]
quandl_list=['gold','LBMA/GOLD']
#Get the Fred data
freddata = pd.DataFrame()
fredfile = pd.DataFrame()
compriceslast = pd.DataFrame()


for i in yield_list:     
    fredvalue=''.join(i[1])
    fredname=''.join(i[0])
    freddata = fred.get_series_all_releases(fredvalue)
    freddata[fredname]=pd.to_numeric(freddata['value'], errors='coerce')
    freddata['ind']=freddata['date']
    freddata['year'] = freddata['ind'].dt.strftime("%Y")
    freddata['month'] = freddata['ind'].dt.strftime("%m")
    #freddata['day'] = freddata['ind'].dt.strftime("%d")
    freddata.__delitem__('value')
    freddata.__delitem__('realtime_start')
    freddata.__delitem__('date')
    freddata.__delitem__('ind')        
    if fredfile.empty:
        fredfile = pd.DataFrame(freddata)
    else:
        fredfile = pd.merge(fredfile, freddata, how="left", on=['year','month'])  

####################
#Get the quandl data
####################

df= quandl.get('LBMA/GOLD')
df.columns=['price','EUR AM','GBP AM','USD PM','EUR PM','GBP PM']
df['variable']='gold'
df.__delitem__('EUR AM')
df.__delitem__('GBP AM')
df.__delitem__('USD PM')
df.__delitem__('EUR PM')
df.__delitem__('GBP PM') 
df['ind']=df.index
df['year'] = df['ind'].dt.strftime("%Y")
df['month'] = df['ind'].dt.strftime("%m")
df['day']=1
goldmth = df.groupby(['month','year'], as_index=False)['price','day'].sum()
goldmth['goldprice']=goldmth['price']/goldmth['day']
goldmth.__delitem__('day') 
goldmth.__delitem__('price') 

###############################################################################################################
#constuct moving averages to determine if the yield is higher than the gold return over the same period of time
###############################################################################################################

com_list2=com_list.sort_values(['commodity','ind'])

fredfile['lag6_2YearCorpYield'] = fredfile['2YearCorpYield'].shift(6)
fredfile['6mthreturn_2YearCorpYield'] = fredfile['2YearCorpYield']/fredfile['lag6_2YearCorpYield']-1
fredfile['2yrMA']=pd.rolling_mean(fredfile['6mthreturn_2YearCorpYield'], 6)
fredfile['lag6_5YearCorpYield'] = fredfile['5YearCorpYield'].shift(6)
fredfile['6mthreturn_5YearCorpYield'] = fredfile['5YearCorpYield']/fredfile['lag6_5YearCorpYield']-1
fredfile['5yrMA']=pd.rolling_mean(fredfile['6mthreturn_5YearCorpYield'], 6)
fredfile['lag6_10YearCorpYield'] = fredfile['10YearCorpYield'].shift(6)
fredfile['6mthreturn_10YearCorpYield'] = fredfile['10YearCorpYield']/fredfile['lag6_10YearCorpYield']-1
fredfile['10yrMA']=pd.rolling_mean(fredfile['6mthreturn_10YearCorpYield'], 6)
fredfile['lag6_30YearCorpYield'] = fredfile['30YearCorpYield'].shift(6)
fredfile['6mthreturn_30YearCorpYield'] = fredfile['30YearCorpYield']/fredfile['lag6_30YearCorpYield']-1
fredfile['30yrMA']=pd.rolling_mean(fredfile['6mthreturn_30YearCorpYield'], 6)

compriceslast = compriceslast.append(lastrow, ignore_index=False)

###############################################################################################################
#constuct moving averages to determine if the yield is higher than the gold return over the same period of time
###############################################################################################################

  
