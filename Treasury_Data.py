#Source is from https://github.com/npezolano/PyTreasuryDirect/blob/master/README.md#
#requirs CUSIP, and ISSUE Date
#list of all identifiers for CUSIP https://www.treasurydirect.gov/instit/auctfund/work/auctime/auctime_securitiestable.htm
#the date is the issue date of the cusip number

from pytreasurydirect import TreasuryDirect

td = TreasuryDirect()
cusip = '912796CJ6'

print(td.security_info(cusip, '02/11/2014'))
# or 
print(td.security_info(cusip, datetime.date(2014, 2, 11)))

from pytreasurydirect import TreasuryDirect

td = TreasuryDirect()
cusip = '912796CJ6'
2018-08-09

cusip='912796QW2'
test=(td.security_info(cusip, '08/09/2018'))

for i in dateval:
    test=(td.security_info(cusip, '08/14/2018'))

912796QV4
#Make a dictionary file#

for i in dateval:
    test=(td.security_info(cusip, '02/11/2014'))
#
pd.DataFrame(test.items())
df = pd.DataFrame(test, index=['a'])
