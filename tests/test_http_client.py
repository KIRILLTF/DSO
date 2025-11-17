import httpx

from src.app.security.http_client import fetch_with_retry


def test_fetch_with_retry(monkeypatch):
    class DummyResponse:
        def raise_for_status(self):
            pass

    class DummyClient:
        def get(self, url, follow_redirects=True):
            return DummyResponse()

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            pass

    monkeypatch.setattr(httpx, "Client", lambda *args, **kwargs: DummyClient())
    r = fetch_with_retry("https://example.com")
    assert r is not None
