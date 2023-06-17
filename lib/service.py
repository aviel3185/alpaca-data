from datetime import datetime

import pytz

from lib.russel_1000_ticker_to_cik import RUSSELL1000_TICKER_TO_CIK
import re


def extract_cik_from_rss_title(title: str) -> int | None:
    pattern = r'\(\D*(\d+)\D*\)'
    match = re.search(pattern, title)
    if match:
        cik = match.group(1)
        return int(cik)
    else:
        return None


def cik_to_ticker(cik: int):
    for item in RUSSELL1000_TICKER_TO_CIK.items():
        if int(item[1]) == int(cik):
            return item[0]


def get_ny_gmt() -> str:
    time = get_ny_time().replace(tzinfo=None)
    return time.strftime('%a, %d %b %Y %H:%M:%S GMT')


def get_ny_time() -> datetime:
    # Get the timezone object for New York
    tz_NY = pytz.timezone('America/New_York')
    # Get the current time in New York
    datetime_NY = datetime.now(tz_NY)
    return datetime_NY


def is_stock_market_open():
    # Get the current time in New York timezone
    ny_timezone = pytz.timezone('America/New_York')
    current_time = datetime.now(ny_timezone)

    # Check if the current time is within the stock market trading hours
    weekday = current_time.weekday()
    is_weekday = 0 <= weekday <= 4  # Monday to Friday
    is_trading_hours = (current_time.hour > 9 or (current_time.hour == 9 and current_time.minute >= 30)) and (
            current_time.hour < 16)

    return is_weekday and is_trading_hours
