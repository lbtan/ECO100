#-----------------------------------------------------------------------
# utils.py
# Author: Hita Gupta
# 
#-----------------------------------------------------------------------

import datetime
from pytz import timezone

# get's today's date in Eastern Time
# https://stackoverflow.com/questions/11710469/how-to-get-python-to-display-the-current-eastern-time
def today():
    return datetime.datetime.now(timezone('US/Eastern')).date()

def now():
    return datetime.datetime.now(timezone('US/Eastern')).replace(tzinfo=None)