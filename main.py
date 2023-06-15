from datetime import datetime
import pycron
import requests
from bs4 import BeautifulSoup

from lib.headers import SEC_API_HEADERS
from lib.service import extract_cik_from_rss_title

print("starting cron job")


# @pycron.cron("* * * * * */20")
def cron_job(timestamp: datetime):
    print(f"Polling at {timestamp}")
    url = "https://www.sec.gov/cgi-bin/browse-edgar?action=getcurrent&type=8-K&output=atom"
    response = requests.get(url, headers=SEC_API_HEADERS)
    html_content = response.content

    # Parse the HTML using BeautifulSoup
    soup = BeautifulSoup(html_content, "html.parser")

    # Find all the entries in the table
    entries = soup.find_all("entry")

    # Iterate over the entries and extract the event information
    for entry in entries:
        title = entry.title.get_text()  # Event title
        cik = extract_cik_from_rss_title(title)
        print("Title:", title)


if __name__ == '__main__':
    cron_job(datetime.now())
    pycron.start()
