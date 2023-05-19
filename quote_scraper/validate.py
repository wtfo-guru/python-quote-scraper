"""Top-level module validate for Quote Scraper."""

from urllib.parse import urlparse

def url_validator(url: str) -> bool:
    """Validate url."""
    try:
        parts = urlparse(url)
        return all([parts.scheme, parts.netloc, parts.path])
    except ValueError:
        return False
