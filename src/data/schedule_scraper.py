import time
from datetime import datetime

import schedule

from .scraper import setup_db, scrape_and_store


def run_job():
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Starting daily Jumia scrape...")
    setup_db()
    scrape_and_store()
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Finished daily Jumia scrape.")


def main():
    # Schedule the job to run every day at 08:00 local time
    schedule.every().day.at("08:00").do(run_job)

    # Immediately show the next run time
    print("Scheduler started. Job scheduled daily at 08:00 local time.")
    print("Keep this process running to execute the job.")

    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        print("Scheduler stopped by user.")


if __name__ == "__main__":
    main()
