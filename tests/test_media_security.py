from pathlib import Path

from src.services.media_security import get_secret, problem, secure_save, sniff_image_type


def test_sniff_image_type():
    assert sniff_image_type(b"\x89PNG\r\n\x1a\n") == "image/png"
    assert sniff_image_type(b"\xff\xd8....\xff\xd9") == "image/jpeg"
    assert sniff_image_type(b"bad_data") is None


def test_rejects_big_file(tmp_path: Path):
    ok, reason = secure_save(tmp_path, b"\x89PNG\r\n\x1a\n" + b"0" * 5_000_001)
    assert not ok and reason == "too_big"


def test_rejects_invalid_type(tmp_path: Path):
    ok, reason = secure_save(tmp_path, b"not_an_image")
    assert not ok and reason == "bad_type"


def test_problem_format():
    resp = problem(400, "Bad Request", "Invalid input")
    data = resp.body.decode()
    assert "correlation_id" in data
    assert "Invalid input" in data


def test_env_loaded(monkeypatch):
    monkeypatch.setenv("MEDIA_KEY", "secret123")
    assert get_secret("MEDIA_KEY") == "secret123"
