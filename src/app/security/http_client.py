import time

import httpx

TIMEOUT = httpx.Timeout(5.0, read=5.0, connect=3.0)


def fetch_with_retry(url: str, max_attempts: int = 3) -> httpx.Response:
    """HTTP GET с таймаутами и retry"""
    for attempt in range(max_attempts):
        try:
            with httpx.Client(timeout=TIMEOUT) as client:
                r = client.get(url, follow_redirects=True)
                r.raise_for_status()
                return r
        except Exception:
            if attempt == max_attempts - 1:
                raise
            time.sleep(0.5 * (attempt + 1))
