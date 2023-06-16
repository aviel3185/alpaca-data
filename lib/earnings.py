from datetime import datetime, timedelta
import threading
import requests
from bs4 import BeautifulSoup

from lib.db import EarningsDate, db
from lib.headers import SEC_API_HEADERS
from lib.price_poller import poll_prices
from lib.russel_1000_ticker_to_cik import RUSSELL1000_TICKER_TO_CIK
from lib.service import extract_cik_from_rss_title, cik_to_ticker

arrived_tickers = list()


def ingest_earnings_calendar():
    url = "https://financialmodelingprep.com/api/v3/earning_calendar?apikey=ca7b76ae19c3db4e187707479efd60c8"
    earnings = requests.get(url, headers=SEC_API_HEADERS).json()
    values = list()
    for earning in earnings:
        if RUSSELL1000_TICKER_TO_CIK.get(earning["symbol"].lower()) is not None:
            earnings_date = EarningsDate()
            earnings_date.cik = int(RUSSELL1000_TICKER_TO_CIK[earning["symbol"].lower()])
            earnings_date.ticker = earning["symbol"].lower()
            earnings_date.date = earning["date"]
            values.append(earnings_date.__dict__['__data__'])
            print(earning["symbol"], int(RUSSELL1000_TICKER_TO_CIK[earning["symbol"].lower()]))

    with db.atomic():
        EarningsDate.insert_many(values).on_conflict_ignore().execute()
    print("Done inserting earnings calendar")


def poll_earnings_event():
    print(f"Polling at {datetime.now()}")
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)
    tomorrow = today + timedelta(days=1)
    query = EarningsDate.select().where(EarningsDate.date.between(yesterday, tomorrow))
    rows = query.execute()
    tickers = list(map(lambda row: row.ticker, rows))
    url = "https://www.sec.gov/cgi-bin/browse-edgar?action=getcurrent&type=8-K&output=atom"
    response = requests.get(url, headers=SEC_API_HEADERS)
    html_content = response.content

    # Parse the HTML using BeautifulSoup
    soup = BeautifulSoup(html_content, "html.parser")

    # Find all the entries in the table
    entries = soup.find_all("entry")

    # Iterate over the entries and extract the event information
    for entry in entries:
        title = entry.title.get_text()
        cik = extract_cik_from_rss_title(title)
        ticker = cik_to_ticker(cik)
        if ticker is not None and ticker in tickers and ticker not in arrived_tickers:
            print(f"Filing of {ticker} arrived at {datetime.now()}, Starting price polling...")
            arrived_tickers.append(ticker)
            thread = threading.Thread(target=poll_prices, kwargs=dict(ticker=ticker, cik=cik))
            thread.start()
