"""Time keeping shouldn't be hard and should be in UTC.  This module attempts
to make it very easy to do that.
"""

import time
from datetime import datetime
from dateutil.parser import parse


###
### Main Time Function
###

def curtime():
    """This funciton is the central method for getting the current time. It
    represents the time in milliseconds and the timezone is UTC.
    """
    return long(time.time() * 1000)


###
### Converstion Helpers
###

def datestring_to_millis(ds):
    """Takes a string representing the date and converts it to milliseconds
    since epoch.
    """
    dt = parse(ds)
    return datetime_to_millis(dt)


def datetime_to_millis(dt):
    """Takes a datetime instances and converts it to milliseconds since epoch.
    """
    seconds = dt.timetuple()
    seconds_from_epoch = time.mktime(seconds)
    return seconds_from_epoch * 1000  # milliseconds


def millis_to_datetime(ms):
    """Converts milliseconds into it's datetime equivalent
    """
    seconds = ms / 1000.0
    return datetime.fromtimestamp(seconds)


###
### Neckbeard date parsing (fuzzy!)
###

def prettydate(d):
    """I <3 U, StackOverflow.

    http://stackoverflow.com/questions/410221/natural-relative-days-in-python
    """
    diff = datetime.utcnow() - d
    s = diff.seconds
    if diff.days > 7 or diff.days < 0:
        return d.strftime('%d %b %y')
    elif diff.days == 1:
        return '1 day ago'
    elif diff.days > 1:
        return '{0} days ago'.format(diff.days)
    elif s <= 1:
        return 'just now'
    elif s < 60:
        return '{0} seconds ago'.format(s)
    elif s < 120:
        return '1 minute ago'
    elif s < 3600:
        return '{0} minutes ago'.format(s / 60)
    elif s < 7200:
        return '1 hour ago'
    else:
        return '{0} hours ago'.format(s / 3600)