#!/usr/bin/env python3


def is_black_friday(date):
    """
    Checks if the given date belong to black friday dates
    Nov 23, 24 and 25
    """
    return date.month == 11 and 23 <= date.day <= 25


def is_2019(date):
    """
    Checks if the given date is after 2019 jan 1
    """
    return date.year >= 2019
