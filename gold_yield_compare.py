#Yield Curve Analysis

#Compares gold returns with yeilds


from pandas.compat import StringIO
#Sourced from the following site https://github.com/mortada/fredapi
from fredapi import Fred
import StringIO
import quandl
import datetime as dt
import ast
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
('2-Year High Quality Market (HQM) Corporate Bond Par Yield','HQMCB2YRP'),
('5-Year High Quality Market (HQM) Corporate Bond Par Yield','HQMCB5YRP'),
('10-Year High Quality Market (HQM) Corporate Bond Par Yield','HQMCB10YRP'),
('30-Year High Quality Market (HQM) Corporate Bond Par Yield','HQMCB30YRP')]

quandl_list=['gold','LBMA/GOLD']

#Get the Fred data

freddata = pd.DataFrame()
fredfile = pd.DataFrame()

for i in yield_list:     
    try:
        fredvalue=''.join(i[1])
        fredname=''.join(i[0])
        freddata = fred.get_series_all_releases(fredvalue)
        freddata['price']=pd.to_numeric(freddata['value'], errors='coerce')
        freddata['variable'] = fredname
        freddata['ind']=freddata['date']
        freddata.__delitem__('value')
        fredfile = fredfile.append(freddata, ignore_index=False)        
    except:
        print
        
com_list=fredfile.drop_duplicates(['variable'], keep='last')
dflist = com_list['variable'].tolist()

#sort by variable and date
com_list2=fredfile.sort_values(['variable','ind'])


for i in dflist:  
    com_name=''.join(i) 
    #only include the current commodity 
    df = fredfile[fredfile['variable']==com_name]            
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

print compriceslast


 
#Get the quandl data

quandlraw = pd.DataFrame()

for i in quandl_list:
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
    quandlraw = quandlraw.append(dflmba, ignore_index=False)


lmba=quandlraw.append(fredfile, ignore_index=True)

print fredfile

###############################################################################################################
#constuct moving averages to determine if the yield is higher than the gold return over the same period of time
###############################################################################################################

  
