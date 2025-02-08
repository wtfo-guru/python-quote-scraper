"""Top-level module for Wtf Quotes."""

import re
from typing import Dict, Tuple

from bs4 import Tag

from quote_scraper.constants import KAUTHOR, KCATEGORY, KQUOTE
from quote_scraper.foos import get_soup
from quote_scraper.kinds import StrAnyDict
from quote_scraper.quote import QdataList, Quote


def scrape_inspiring_qod(cdata: Dict[str, str]) -> QdataList:
    """Scrape inspiring quote of the day."""
    # TODO: Handle cases where HTML might not contain a quote of the day.
    # TODO: Handle cases where HTML might not contain an author.
    # TODO: Handle cases where HTML might not contain a category.
    qdatums: QdataList = []
    ok = False
    qpost: StrAnyDict = {KCATEGORY: cdata.get("category", "None")}
    soup = get_soup(cdata)
    div = soup.find("div", {"class": "IQDailyInspiration__quoteContainer"})
    if div is not None:
        qpost[KQUOTE] = div.get_text().strip()
        div = soup.find("div", {"class": "IQDailyInspiration__authorContainer"})
        if div is not None:
            qpost[KAUTHOR] = div.get_text().strip()
            ok = True
    if ok:
        qdatums.append(Quote(qpost))
    return qdatums


def _get_author(tag: Tag, quote: str, default: str) -> Tuple[str, str]:
    em = tag.find("em")
    if em:
        author = em.get_text().strip()
        return quote.replace(author, ""), author
    return quote, default


def scrape_inspiring_quotes(cdata: Dict[str, str]) -> QdataList:  # noqa: WPS210
    """Scrape inspring quotes."""
    qnbr = 0
    soup = get_soup(cdata)
    author = cdata.get("author", "Unknown")
    category = cdata.get("category", "None")
    qdatums: QdataList = []
    quotes: Dict[str, int] = {}
    for bq in soup.find_all("blockquote"):
        qnbr += 1
        qpost: StrAnyDict = {KCATEGORY: category}
        e_quote = bq.get_text().strip()
        if isinstance(bq, Tag):
            e_quote, e_author = _get_author(bq, e_quote, author)
        e_quote = e_quote.replace(" / ", " ")
        # To add space after dot or comma using regular expression (re):
        e_quote = re.sub(r"(?<=[.,])(?=[^\s])", " ", e_quote)
        # Remove trailing chars [em dash, ...]
        e_quote = re.sub("[–]$", "", e_quote)
        # multiple consecutive space to one
        e_quote = " ".join(e_quote.split())
        if e_author:
            e_author = re.sub(",.*", "", e_author)
            e_author = re.sub("^[^A-Za-z]+", "", e_author)
        if e_quote in quotes:
            quotes[e_quote] += 1  # noqa: WPS529
            continue
        quotes[e_quote] = 1
        qpost[KQUOTE] = e_quote
        qpost[KAUTHOR] = e_author
        qdatums.append(Quote(qpost))
    return qdatums
