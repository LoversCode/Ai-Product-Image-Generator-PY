import time
import logging

def retry(func, retries=3, delay=2, backoff=2):
    for attempt in range(retries):
        try:
            return func()
        except Exception as e:
            logging.warning(f"[Retry {attempt+1}] Function failed: {e}")
            if attempt < retries - 1:
                time.sleep(delay)
                delay *= backoff
            else:
                logging.error("All retries failed.")
                raise e
