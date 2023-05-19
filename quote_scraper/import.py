"""Top-level module import for Quote Scraper."""

from typing import Tuple, Union
from pathlib import Path
from quote_scraper.cache import cache_url
from quote_scraper.errors import QuoteScrapeImportError, raise_fnfe
from quote_scraper.quote import QdataList
from quote_scraper.validate import url_validator


def import_quotes(  # noqa: C901 WPS231
    author: str,
    category: str,
    source: str,
) -> Tuple[QdataList, str]:
    """Import quotes from a url or file."""
    import_fn: Union[str, bool] = source
    if url_validator(source):
        import_fn = cache_url(source, author, category)
        if not import_fn:
            raise QuoteScrapeImportError("Url did not return any data.")
    if not Path(str(import_fn)).is_file():
        raise_fnfe(str(import_fn))
    return process_cached(str(import_fn))


def import_cached(src_nm: str) -> Tuple[QdataList, str]:
    """Import previously cached file."""
    source = get_import_path("todo") / src_nm
    src_str = str(source)
    if not source.is_file():
        raise_fnfe(src_str)
    return process_cached(src_str)
