import pendulum as pdl
from pendulum.parsing.exceptions import ParserError
from pendulum.datetime import DateTime
from typing import Union

parsing_error_message = """Could not parse date '%s'.

You can use `Create Datetime` keyword to construct valid
date object by giving datetime as string and corresponding
date format. See https://pendulum.eustace.io/docs/#tokens for
valid tokens for the date format.
"""


def time_difference(start_date: Union[str, DateTime], end_date: Union[str, DateTime]):
    """Compare 2 dates and get the time difference.

    Returned dictionary contains following properties:

        - end_date_is_greater, `True` if end_date is more recent
          than start_date, otherwise `False`
        - days, time difference in days
        - hours, time difference in hours (in addition to the days)
        - minutes, time difference in minutes (in addition to the hours)
        - seconds, time difference in seconds (in addition to the minutes)
    """
    if isinstance(start_date, str):
        start_d = _parse_datetime_string_to_pendulum_datetime(start_date)
    else:
        start_d = start_date
    if isinstance(end_date, str):
        end_d = _parse_datetime_string_to_pendulum_datetime(end_date)
    else:
        end_d = end_date

    diff = end_d - start_d
    modifier_for_seconds = 1 if diff.seconds >= 0 else -1
    return {
        "end_date_is_greater": end_d > start_d,
        "days": diff.days,
        "hours": diff.hours,
        "minutes": diff.minutes,
        "seconds": diff.seconds
        if abs(diff.seconds) <= 60
        else abs(diff.seconds) % 60 * modifier_for_seconds,
    }


def create_datetime(date_string: str, date_format: str, timezone: str = "UTC"):
    """This keyword tries to construct valid datetime
    object from given date string and its expected date
    format.

    See https://pendulum.eustace.io/docs/#tokens for
    valid tokens for the date format. Tokens are
    used to form correct date_format.

    :param date_string: for example. "22 May 19"
    :param date_format: for example. "DD MMM YY"
    :param timezone: default timezone is "UTC"

    :return: datetime object which can be used
     with `Time Difference` keyword
    """
    return pdl.from_format(date_string, date_format, tz=timezone)


def time_now(timezone: str = None):
    """Return current datetime

    :param timezone: optional, for example. "America/Boston"
    :return: current datetime as an object
    """
    return pdl.now(tz=timezone)


def _parse_datetime_string_to_pendulum_datetime(date_string):
    try:
        result = pdl.parse(date_string, strict=False)
        return result
    except ParserError as err:
        raise ValueError(parsing_error_message % date_string)
