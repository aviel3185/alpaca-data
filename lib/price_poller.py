import time
import re
import requests
from uuid import uuid4 as uuid
from lib.db import Price
from lib.headers import NASDAQ_HEADERS
from lib.service import get_ny_gmt


def get_numeric_quote_info(ticker: str, key: str) -> float:
    url = f'https://api.nasdaq.com/api/quote/{ticker.upper()}/info?assetclass=stocks'
    headers = NASDAQ_HEADERS.copy()
    headers['date'] = get_ny_gmt()
    nasdaq_json = requests.get(url, headers=headers).json()
    try:
        value = nasdaq_json['data']['primaryData'][key]
        value = re.sub(r'[^0-9.]', '', value)
    except:
        try:
            value = nasdaq_json['data']['secondaryData'][key]
            value = re.sub(r'[^0-9.]', '', value)
        except:
            return None
    return float(value)


def poll_prices(**kwargs):
    ticker = kwargs["ticker"]
    interation_uuid = str(uuid())
    index = 0

    while index < 6 * 15:
        price = get_numeric_quote_info(ticker, 'lastSalePrice')
        if price is not None:
            instance = Price()
            instance.ticker = ticker
            instance.cik = int(kwargs["cik"])
            instance.iteration_uuid = interation_uuid
            instance.price = price
            instance.created_at = get_ny_gmt()
            instance.save()
        index += 1
        time.sleep(10)
