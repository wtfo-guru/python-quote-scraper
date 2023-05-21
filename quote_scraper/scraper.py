"""Top-level module import for Quote Scraper."""

import os

from time import time
from typing import cast, Optional, Tuple, Union
from pathlib import Path
from quote_scraper.cache import cache_url
from quote_scraper.errors import QuoteScrapeImportError, raise_fnfe
from quote_scraper.process import process_cached
from quote_scraper.quote import QdataList
from quote_scraper.validate import url_validator

class Scraper(object):
    """Settings for Quote Scraper."""

    cachedir: Path
    logger: object

    def __init__(self, **kwargs):
        """Constructs a new Quote Scraper."""
        self.cachedir = kwargs.pop(
            "cachedir",
            Path.home() / ".cache" / "quote-scraper",
        )
        logger: Optional[object] = kwargs.pop("logger", None)
        if logger is None:
            from loguru import logger
            self.logger = logger
        self.logger - logger

    def scrape_quotes(  # noqa: C901 WPS231
        self,
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


    def scrape_cached(self, src_nm: str) -> Tuple[QdataList, str]:
        """Import previously cached file."""
        source = self._get_import_path("todo") / src_nm
        src_str = str(source)
        if not source.is_file():
            raise_fnfe(src_str)
        return process_cached(src_str)

    def _get_import_path(self, subd: str) -> Path:
        """Return specified import subdirectory path."""
        sf = Path(cast(Union[str, os.PathLike[str]], self.cachedir))  # noqa: WPS221
        return sf / "import" / subd


    def _get_stamped_import_path(self) -> Path:
        """Create a timestamped path to an import todo file."""
        ts = str(time())
        return self._get_import_path("todo") / "quote-imports-{0}.json".format(ts)  # noqa: WPS221


    def _scraped(self, source: str, errors: list[str]) -> None:
        """Move imported file to done subdirectory."""
        sp = Path(source)
        if errors:
            sp.rename(self._get_import_path("done") / sp.name)
        else:
            ipath = self._get_import_path("erred")
            sp.rename(ipath / sp.name)
            epath = ipath / "{0}.errors.txt".format(sp.name)
            with open(epath, "w") as efile:
                efile.write("\n".join(errors))
