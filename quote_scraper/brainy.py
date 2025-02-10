"""Top-level module for Wtf Quotes."""

import re
from typing import Dict

from bs4 import Tag

from quote_scraper.constants import KAUTHOR, KCATEGORY, KQUOTE
from quote_scraper.foos import get_soup
from quote_scraper.kinds import StrAnyDict
from quote_scraper.quote import QdataList, Quote
from quote_scraper.settings import settings

RE_DISPLAY = re.compile("^RE_DISPLAY:")
RE_QOD = re.compile("Quote of the Day", re.IGNORECASE)


def _extract_category(q_post: StrAnyDict, div: Tag) -> None:
    category = div.find("h2", class_="RE_QOD-h2")
    if category:
        q_post[KCATEGORY] = (
            RE_QOD.sub("", category.get_text()).strip().replace("Funny", "Humor")
        )
        settings.logger.debug("category: {0}".format(q_post[KCATEGORY]))
    if KCATEGORY not in q_post:
        q_post[KCATEGORY] = "None"


def _extract_quote(q_post: StrAnyDict, div: Tag) -> bool:
    quote = div.find("div", {"style": RE_DISPLAY})
    if quote:
        q_post[KQUOTE] = quote.get_text().strip()
        settings.logger.debug("quote: {0}".format(q_post[KQUOTE]))
        return True
    return False


def _extract_author(q_post: StrAnyDict, div: Tag) -> bool:
    author = div.find("a", {"title": "view author"})
    if author:
        q_post[KAUTHOR] = author.get_text().strip()
        settings.logger.debug("author: {0}".format(q_post[KAUTHOR]))
        return True
    return False


def scrape_brainy_qod(cdata: Dict[str, str]) -> QdataList:  # noqa: WPS210 WPS231
    """Scrape brainy quotes quote of the day page."""
    quotes_nbr = 0
    quote_datums: QdataList = []
    soup = get_soup(cdata)
    for div in soup.find_all("div", class_="grid-item qb clearfix bqQt"):
        if isinstance(div, Tag):
            quotes_nbr += 1
            q_post: StrAnyDict = {}
            _extract_category(q_post, div)
            if not _extract_quote(q_post, div):
                settings.logger.warn(
                    "Scrape quote number {0} failed.".format(quotes_nbr),
                )
                continue
            if not _extract_author(q_post, div):
                settings.logger.warn(
                    "Scrape author number {0} failed.".format(quotes_nbr),
                )
                continue
            quote_datums.append(Quote(q_post))
    return quote_datums
