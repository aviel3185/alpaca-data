from lib.service import cik_to_ticker


def test_aapl_ticker():
    assert cik_to_ticker('0000320193').lower() == 'AAPL'.lower()