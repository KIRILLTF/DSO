import uuid
from pathlib import Path

MAX = 5_000_000
PNG = b"\x89PNG\r\n\x1a\n"
SOI = b"\xff\xd8"
EOI = b"\xff\xd9"


def sniff(data: bytes) -> str | None:
    """Определяем mime-type по magic bytes"""
    if data.startswith(PNG):
        return "image/png"
    if data.startswith(SOI) and data.endswith(EOI):
        return "image/jpeg"
    return None


def secure_save(root: Path, data: bytes) -> Path:
    """Безопасное сохранение файла"""
    if len(data) > MAX:
        raise ValueError("too_big")
    mt = sniff(data)
    if not mt:
        raise ValueError("bad_type")

    root = root.resolve(strict=True)
    ext = ".png" if mt == "image/png" else ".jpg"
    p = (root / f"{uuid.uuid4()}{ext}").resolve()

    if not str(p).startswith(str(root)):
        raise ValueError("path_traversal")
    if any(x.is_symlink() for x in p.parents):
        raise ValueError("symlink_parent")

    p.write_bytes(data)
    return p
