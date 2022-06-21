from datetime import date
from email.policy import strict
from time import time
import pendulum as pdl
from pendulum.parsing.exceptions import ParserError
from pendulum.datetime import DateTime
from typing import Union
import holidays

parsing_error_message = """Could not parse date '%s'.

You can use `Create Datetime` keyword to construct valid
date object by giving datetime as string and corresponding
date format. See https://pendulum.eustace.io/docs/#tokens for
valid tokens for the date format.
"""

BUSINESS_DAYS = [1, 2, 3, 4, 5]  # Monday - Friday


def time_difference(
    start_date: Union[str, DateTime],
    end_date: Union[str, DateTime],
    timezone: str = None,
):
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
        start_d = _parse_datetime_string_to_pendulum_datetime(
            start_date, timezone=timezone
        )
    else:
        start_d = start_date
    if isinstance(end_date, str):
        end_d = _parse_datetime_string_to_pendulum_datetime(end_date, timezone=timezone)
    else:
        end_d = end_date

    diff = end_d - start_d
    modifier_for_seconds = 1 if diff.seconds >= 0 else -1
    return {
        "end_date_is_greater": end_d > start_d,
        "years": diff.years,
        "months": diff.months,
        "days": diff.days,
        "hours": diff.hours,
        "minutes": diff.minutes,
        "seconds": diff.seconds
        if abs(diff.seconds) <= 60
        else abs(diff.seconds) % 60 * modifier_for_seconds,
    }


def create_datetime(
    date_string: str,
    date_format_in: str = None,
    timezone: str = None,
    date_format_out: str = None,
):
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
    result = None
    if date_format_in:
        result = pdl.from_format(date_string, date_format_in, tz=timezone)
    else:
        result = _parse_datetime_string_to_pendulum_datetime(
            date_string, timezone=timezone
        )
    return result.format(date_format_out) if date_format_out else result


def time_now(timezone: str = None):
    """Return current datetime

    :param timezone: optional, for example. "America/Boston"
    :return: current datetime as an object
    """
    return pdl.now(tz=timezone)


def _parse_datetime_string_to_pendulum_datetime(date_string, timezone: str = None):
    arguments = {"text": date_string, "strict": False}
    if timezone:
        arguments["tz"] = timezone
    try:
        result = pdl.parse(**arguments)
        return result
    except ParserError as err:
        raise ValueError(parsing_error_message % date_string)


def time_difference_in_months(
    start_date: Union[str, DateTime], end_date: Union[str, DateTime]
):
    diff = time_difference(start_date, end_date)
    diff["months"] += diff["years"] * 12
    return diff


def return_previous_business_day(given_date: Union[str, DateTime], country: str = None):
    if isinstance(given_date, str):
        given_dt = pdl.parse(given_date, strict=False)
    else:
        given_dt = given_date
    previous_dt = given_dt
    while True:
        is_business_day = False
        previous_dt = previous_dt.add(days=-1)
        prev_day = date(previous_dt.year, previous_dt.month, previous_dt.day)
        if previous_dt.day_of_week in BUSINESS_DAYS:
            is_business_day = True
        if country and is_business_day:
            is_business_day = prev_day not in holidays.country_holidays(country)
        if is_business_day:
            break

    return previous_dt


def should_be_equal_in_days(
    first_date: Union[str, DateTime], second_date: Union[str, DateTime]
):
    if isinstance(first_date, str):
        first_d = _parse_datetime_string_to_pendulum_datetime(first_date)
    else:
        first_d = first_date
    if isinstance(second_date, str):
        second_d = _parse_datetime_string_to_pendulum_datetime(second_date)
    else:
        second_d = first_date
    diff_in_days = first_d.diff(second_d).in_days()
    assert diff_in_days == 0, f"difference was {abs(diff_in_days)} days"
