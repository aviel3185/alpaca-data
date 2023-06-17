import time
import re
import requests
from uuid import uuid4 as uuid

from bs4 import BeautifulSoup

from lib.db import Price
from lib.headers import NASDAQ_HEADERS, SEC_API_HEADERS
from lib.service import get_ny_gmt, is_stock_market_open


def get_numeric_quote_info(ticker: str, key: str = None) -> float:
    is_open = is_stock_market_open()
    if is_open:
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
    else:

        url = f"https://finance.yahoo.com/quote/{ticker.upper()}?p={ticker.upper()}&.tsrc=fin-srch"
        response = requests.get(url, headers=SEC_API_HEADERS)
        soup = BeautifulSoup(response.text, 'html.parser')
        try:
            after_hours_price = soup.find_all('fin-streamer', class_='C($primaryColor) Fz(24px) Fw(b)')[0].text
            return float(after_hours_price)
        except IndexError:
            return None


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


if __name__ == '__main__':
    get_numeric_quote_info('aapl', 'lastSalePrice')
