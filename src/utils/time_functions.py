from datetime import datetime
from pytz import timezone

UTC = timezone('UTC')

def get_current_time():
    """
    Returns the current year, month, day and time in UTC.
    """

    return datetime.now(UTC)
