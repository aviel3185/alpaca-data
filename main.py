from datetime import datetime
import pycron


@pycron.cron("* * * * * */20")
async def test(timestamp: datetime):
    print(f"test cron job running at {timestamp}")
    print("hi")


if __name__ == '__main__':
    pycron.start()
