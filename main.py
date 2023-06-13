from datetime import datetime
import time


def main():
    while True:
        print("Hello World, time is now, ", datetime.now())

        # Wait for 1 second
        time.sleep(1)


if __name__ == '__main__':
    main()