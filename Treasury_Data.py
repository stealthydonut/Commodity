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
