"""
The Campaign clock for the Noobhammer Chronicles
"""
import telisaran
from calendar import Calendar
import fire


class Campaign:
    """
    The current campaign's calendar.
    """
    today = telisaran.datetime(year=3206, season=8, day=11, era=3)
    calendar = Calendar(today)


if '__main__' == __name__:
    fire.Fire(Campaign.calendar)
