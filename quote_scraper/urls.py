"""Top-level module urls for Quote Scraper."""

import re

from typing import cast, Enum, Union
from urllib.parse import urlparse

from quote_scraper.errors import QuoteScrapeImportError

class Qsites(Enum):
    """Class respresting scrapable sites."""

    inspiring_quotes = 1
    inspiring_qod = 2
    brainy_qod = 3

def strorbytes_tostr(uvar: Union[str, bytes]) -> str:
    """Converts bytes to str."""
    utyp = type(uvar)
    if utyp is str:
        return cast(str, uvar)
    if utyp is bytes:
        return cast(bytes, uvar).decode("utf-8")
    raise ValueError(
        "Variable uvar type is {0}. Expected str or bytes.".format(str(utyp)),
    )

def is_known_url(url: str) -> Qsites:  # noqa: WPS231
    """Return enum of matching site."""
    parts = urlparse(url)
    path = strorbytes_tostr(parts.path)
    netloc = strorbytes_tostr(parts.netloc)
    if re.search("inspiringquotes.com", netloc):
        if len(path) > 1:
            fruit = Qsites.inspiring_quotes
        else:
            fruit = Qsites.inspiring_qod
    elif re.search("brainyquote.com", netloc):
        if re.search("quote_of_the_day", path):
            fruit = Qsites.brainy_qod
        else:
            raise QuoteScrapeImportError("Unknown brainyquote.com path: {0}".format(path))
    else:
        raise QuoteScrapeImportError("Unknown import netloc: {0}".format(netloc))
    return fruit
