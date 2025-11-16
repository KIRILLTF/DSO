from pathlib import Path

import pytest

from src.app.security.files import secure_save

ROOT = Path(__file__).parent / "tmp"
ROOT.mkdir(exist_ok=True)


def test_secure_save_ok(tmp_path):
    data = b"\x89PNG\r\n\x1a\nrest"
    f = secure_save(tmp_path, data)
    assert f.exists()


def test_secure_save_too_big(tmp_path):
    data = b"x" * 6_000_000
    with pytest.raises(ValueError, match="too_big"):
        secure_save(tmp_path, data)


def test_secure_save_bad_type(tmp_path):
    data = b"abcdef"
    with pytest.raises(ValueError, match="bad_type"):
        secure_save(tmp_path, data)
