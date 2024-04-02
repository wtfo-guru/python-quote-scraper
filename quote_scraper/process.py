"""Top-level module process for Quote Scraper."""

import json
from pathlib import Path
from typing import Tuple, cast

from quote_scraper import constants
from quote_scraper.brainy import scrape_brainy_qod
from quote_scraper.cache import cache_datums
from quote_scraper.inspiring import (
    scrape_inspiring_qod,
    scrape_inspiringquotes,
)
from quote_scraper.kinds import StrAnyDict
from quote_scraper.quote import QdataList, Quote
from quote_scraper.urls import Qsites, is_known_url


def process_cached(source: str) -> Tuple[QdataList, str]:  # noqa: WPS210 C901 WPS231
    """Process cached quotes."""
    cdata: StrAnyDict
    with open(Path(source)) as json_file:
        cdata = json.load(json_file)

    if constants.KQDATUMS in cdata:
        datums: QdataList = []
        for dat in cdata.get(constants.KQDATUMS, []):
            datums.append(Quote(dat))
        return datums, source
    for key in ("url", "author", "category", "html"):
        if key not in cdata:
            raise KeyError("Missing required key: {0}".format(key))
    site = is_known_url(cast(str, cdata.get("url")))
    if site == Qsites.inspiring_quotes:
        fruit = scrape_inspiringquotes(cdata)
    elif site == Qsites.inspiring_qod:
        fruit = scrape_inspiring_qod(cdata)
    elif site == Qsites.brainy_qod:
        fruit = scrape_brainy_qod(cdata)
    cfn = cache_datums(fruit)
    return fruit, cfn
