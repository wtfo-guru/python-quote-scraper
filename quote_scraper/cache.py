"""Top-level module cache for Quote Scraper."""

import json
import os
import tempfile
from glob import glob
from http import HTTPStatus
from pathlib import Path
from typing import Dict, List, Tuple, Union, cast

import requests

from quote_scraper.brainy import scrape_brainy_qod
from quote_scraper.constants import (
    FAKE_AGENT,
    K_QUOTE_DATUMS,
    KEY_URL,
    REQUEST_TIMEOUT,
    SCRAPEOPS_TIMEOUT,
)
from quote_scraper.files import get_stamped_import_path
from quote_scraper.inspiring import scrape_inspiring_qod, scrape_inspiring_quotes
from quote_scraper.kinds import StrAnyDict
from quote_scraper.quote import QdataList, Quote
from quote_scraper.settings import settings
from quote_scraper.urls import Qsites, is_known_url


def cache_datums(datums: QdataList) -> str:
    """Cache QdataList."""
    cache_data: Dict[str, List[StrAnyDict]] = {K_QUOTE_DATUMS: []}
    for dat in datums:
        cache_data[K_QUOTE_DATUMS].append(dat.__dict__)
    fp = get_stamped_import_path()
    if not fp.parent.exists():
        perm = 0o755
        fp.parent.mkdir(mode=perm, parents=True, exist_ok=False)
    with open(fp, "w") as jfile:
        jfile.write(json.dumps(cache_data, indent=2))
    return str(fp)


def get_cached_names() -> List[str]:
    """Return list of available cached quotes."""
    cached_names: List[str] = []
    # TODO: verify next line on windoze
    mask = "{0}/import/todo/*.json".format(settings.cachedir)
    for cnm in glob(mask):
        cached_names.append(Path(cnm).name)
    return cached_names


def cache_url(url: str, author: str, category: str) -> Union[str, bool]:
    """Cache url to file."""
    if not author:
        author = "unknown"
    if not category:
        category = "Life Lessons"
    fruit: Union[str, bool]
    site = is_known_url(url)
    if site == Qsites.inspiring_quotes:
        fruit = cache_url_type_one(url, author, category)
    elif site == Qsites.inspiring_qod:
        fruit = cache_url_type_one(url, author, category)
    elif site == Qsites.brainy_qod:
        scrapeopts = True
        fruit = cache_url_type_one(url, author, category, scrapeopts)
    return fruit


def cache_url_type_one(
    url: str,
    author: str,
    category: str,
    scrapeopts: bool = False,
) -> Union[str, bool]:
    """Cache quote data from url."""
    cache_data = {}
    cache_data[KEY_URL] = url
    cache_data["author"] = author
    cache_data["category"] = category
    if scrapeopts:
        resp = requests.get(
            url="https://proxy.scrapeops.io/v1/",
            params={
                "api_key": settings.config.get("scrapeops_api_key", ""),
                KEY_URL: url,
            },
            timeout=SCRAPEOPS_TIMEOUT,
        )
    else:
        hdrs = {"User-Agent": FAKE_AGENT}
        resp = requests.get(url, headers=hdrs, timeout=REQUEST_TIMEOUT)

    settings.logger.debug(
        "cache_url_type_two response status_code: {0}".format(resp.status_code),
    )
    if resp.status_code < HTTPStatus.BAD_REQUEST:
        cache_data["html"] = resp.text[:]
        if cache_data["html"]:
            cache, name = tempfile.mkstemp(suffix=".json", text=True)
            os.write(cache, json.dumps(cache_data, indent=2).encode())
            os.close(cache)
            return name
    return False


def process_cached(source: str) -> Tuple[QdataList, str]:  # noqa: WPS210 C901 WPS231
    """Process cached quotes."""
    cdata: StrAnyDict
    with open(Path(source)) as json_file:
        cdata = json.load(json_file)

    if K_QUOTE_DATUMS in cdata:
        datums: QdataList = []
        for dat in cdata.get(K_QUOTE_DATUMS, []):
            datums.append(Quote(dat))
        return datums, source
    for key in (KEY_URL, "author", "category", "html"):
        if key not in cdata:
            raise KeyError("Missing required key: {0}".format(key))

    site = is_known_url(cast(str, cdata.get(KEY_URL)))
    fruit: QdataList = []
    if site == Qsites.inspiring_quotes:
        fruit = scrape_inspiring_quotes(cdata)
    elif site == Qsites.inspiring_qod:
        fruit = scrape_inspiring_qod(cdata)
    elif site == Qsites.brainy_qod:
        fruit = scrape_brainy_qod(cdata)
    cfn = cache_datums(fruit)
    return fruit, cfn
