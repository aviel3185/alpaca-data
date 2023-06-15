from datetime import timedelta, datetime
import os
import pytz as pytz


def get_user_agent() -> str:
    if os.name == 'nt':
        agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
    else:
        agent = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:108.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
    return agent


def get_ny_tomorrow_gmt() -> str:
    time = get_ny_time().replace(tzinfo=None)
    time = time + timedelta(days=1)
    return time.strftime('%a, %d %b %Y %H:%M:%S GMT')


def get_ny_time() -> datetime:
    # Get the timezone object for New York
    tz_NY = pytz.timezone('America/New_York')
    # Get the current time in New York
    datetime_NY = datetime.now(tz_NY)
    return datetime_NY


SEC_API_HEADERS = {
    "User-Agent": get_user_agent(),
    "Authority": "api.sec-api.io",
    "sec-ch-ua": '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
    "accept": "",
    "dnt": "1",
    "sec-ch-ua-mobile": "?0",
    "content-type": "text/html",
    "origin": "https://sec-api.io",
    "sec-fetch-site": "same-site",
    "sec-fetch-mode": "cors",
    "sec-fetch-dest": "empty",
    "referer": "https://sec-api.io/",
    "Accept-Language": "en-US,en;q=0.5",
    "Date": get_ny_tomorrow_gmt(),
    "Clear-Site-Data": "*",
}

NASDAQ_HEADERS = {
    "User-Agent": get_user_agent(),
    "Authority": "api.nasdaq.com",
    "Host": "api.nasdaq.com",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "DNT": "1",
    "Upgrade-Insecure-Requests": "1",
    "content-type": "application/json; charset=utf-8",
    "Sec-Fetch-Site": "cross-site",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Dest": "document",
    "Clear-Site-Data": "*",
}
