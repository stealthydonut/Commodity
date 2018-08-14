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
