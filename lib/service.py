from lib.russel_1000_ticker_to_cik import RUSSELL1000_TICKER_TO_CIK


def extract_cik_from_rss_title(title: str):
    start_index = title.find("(") + 1
    end_index = title.find(")")
    cik = title[start_index:end_index]
    return int(cik)


def cik_to_ticker(cik: int):
    for item in RUSSELL1000_TICKER_TO_CIK.items():
        if int(item[1]) == int(cik):
            return item[0]
