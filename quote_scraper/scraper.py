"""Top-level module scraper for Quote Scraper."""

from pathlib import Path
from typing import List, Tuple, Union

from quote_scraper.cache import cache_url, process_cached
from quote_scraper.errors import QuoteScrapeImportError, raise_fnfe
from quote_scraper.files import get_import_path
from quote_scraper.quote import QdataList
from quote_scraper.validate import url_validator


def scrape_quotes(  # noqa: C901 WPS231
    author: str,
    category: str,
    source: str,
) -> Tuple[QdataList, str]:
    """Import quotes from a url or file."""
    scrape_fn: Union[str, bool] = source
    if url_validator(source):
        scrape_fn = cache_url(source, author, category)
        if not scrape_fn:
            raise QuoteScrapeImportError("Url did not return any data.")
    if not Path(str(scrape_fn)).is_file():
        raise_fnfe(str(scrape_fn))
    return process_cached(str(scrape_fn))


def scrape_cached(src_nm: str) -> Tuple[QdataList, str]:
    """Import previously cached file."""
    source = get_import_path("todo") / src_nm
    src_str = str(source)
    if not source.is_file():
        raise_fnfe(src_str)
    return process_cached(src_str)


def scraped(source: str, errors: List[str]) -> None:
    """Move imported file to done subdirectory."""
    sp = Path(source)
    if errors:
        sp.rename(get_import_path("done") / sp.name)
    else:
        ipath = get_import_path("erred")
        sp.rename(ipath / sp.name)
        epath = ipath / "{0}.errors.txt".format(sp.name)
        with open(epath, "w") as efile:
            efile.write("\n".join(errors))
