#Source is from https://github.com/npezolano/PyTreasuryDirect/blob/master/README.md#
from pytreasurydirect import TreasuryDirect

td = TreasuryDirect()
cusip = '912796CJ6'

print(td.security_info(cusip, '02/11/2014'))
# or 
print(td.security_info(cusip, datetime.date(2014, 2, 11)))
