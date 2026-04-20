import hashlib
from urllib.parse import urlparse


def validate_url(url: str) -> bool:
    parsed = urlparse(url)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def make_code(url: str) -> str:
    return hashlib.sha256(url.encode("utf-8")).hexdigest()[:8]
