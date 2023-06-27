from datetime import datetime

import pytz

utc = pytz.utc


def localize(date: datetime):
    return utc.localize(date)
