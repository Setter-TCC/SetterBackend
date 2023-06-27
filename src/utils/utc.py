from datetime import datetime

import pytz

utc = pytz.utc


def localize(date: datetime):
    try:
        offset_date = utc.localize(date)

    except Exception:
        offset_date = date

    return offset_date
