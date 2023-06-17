from lib.price_poller import get_numeric_quote_info
from lib.service import is_stock_market_open


def test_google_stock_price():
    assert get_numeric_quote_info('GOOGL', 'lastSalePrice') == 123.65


def test_is_stock_market_open():
    assert is_stock_market_open() == False
