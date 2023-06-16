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
