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

cusip_list = [['912796PY9','08/09/2018'],['912796PY9','06/07/2018']]

for i in cusip_list:
    cusip =''.join(i[0]) 
    issuedate =''.join(i[1])
    cusip_value=(td.security_info(cusip, issuedate))
    cusip_value = [str(r) for r in cusip_value]
    cusip_value=['curr_outstanding']=pd.to_numeric(cusip_value=['currentlyOutstanding'], errors='coerce')
    cusip_value['issue_date']=pd.to_datetime(data2['issuedate'], errors='coerce')
    df=
    #pd.DataFrame(cusip_value.items())
    df = pd.DataFrame(cusip_value, index=['a']) 
    td = td.append(df, ignore_index=False)

