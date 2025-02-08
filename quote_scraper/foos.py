"""Top-level module validate for Quote Scraper."""

from typing import Dict

from bs4 import BeautifulSoup


def get_soup(cdata: Dict[str, str]) -> BeautifulSoup:
    """Get BeautifulSoup object from HTML."""
    if "html" in cdata:
        html = cdata.get("html", "")
        if html:
            return BeautifulSoup(html, "html.parser")
        raise ValueError("html data must not be an empty string,")
    raise KeyError("cdata is missing key 'html'.")
