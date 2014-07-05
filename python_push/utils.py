from datetime import datetime
import collections
import time


def now_epoch():
    dt = datetime.now()
    epoch = datetime.utcfromtimestamp(0)
    delta = dt - epoch
    return round(delta.days * 86400 + delta.seconds + delta.microseconds / 1e6 * 1000)


def date2utc(date):
    return time.strftime(
        "%Y-%m-%dT%H:%M:%SZ",
        time.gmtime(time.mktime(date.timetuple()))
    )


def deep_update(origin, destiny):
    for key, val in origin.iteritems():
        if isinstance(val, collections.Mapping):
            destiny[key] = deep_update(val, {})
        else:
            destiny[key] = origin[key]
    return destiny
