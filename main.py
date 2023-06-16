import schedule
import time
from lib.earnings import ingest_earnings_calendar, poll_earnings_event

print("Starting process...")

if __name__ == '__main__':
    schedule.every().day.at("00:00").do(ingest_earnings_calendar)
    schedule.every(20).seconds.do(poll_earnings_event)

    # ingest_earnings_calendar()
    poll_earnings_event()

    while True:
        schedule.run_pending()
        time.sleep(1)
