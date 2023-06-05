from datetime import datetime

from pytz import timezone


def get_now_datetime_by_timezone(timezone_str: str = "Asia/Seoul") -> datetime:
    """
    Returns a datetime object with the specified timezone.

    Args:
        timezone_str (str): The target timezone, in Olson format (e.g. 'America/New_York').

    Returns:
        datetime: A datetime object with the specified timezone.
    """
    return datetime.now(timezone(timezone_str))
