"""Top-level module for Wtf Quotes."""

import re
from typing import Dict

from bs4 import BeautifulSoup

from quote_scraper.constants import KAUTHOR, KCATEGORY, KQUOTE
from quote_scraper.kinds import StrAnyDict
from quote_scraper.quote import QdataList, Quote


def scrape_inspiring_qod(cdata: Dict[str, str]) -> QdataList:
    """Scrape inspring quote of the day."""
    qdatums: QdataList = []
    ok = False
    qpost: StrAnyDict = {KCATEGORY: cdata.get("category", "None")}
    soup = BeautifulSoup(cdata.get("html"), "html.parser")
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


def scrape_inspiringquotes(cdata: Dict[str, str]) -> QdataList:  # noqa: WPS210
    """Scrape inspring quotes."""
    qnbr = 0
    soup = BeautifulSoup(cdata.get("html"), "html.parser")
    author = cdata.get("author", "Unknown")
    category = cdata.get("category", "None")
    qdatums: QdataList = []
    quotes: Dict[str, int] = {}
    for bq in soup.find_all("blockquote"):
        qnbr += 1
        qpost: StrAnyDict = {KCATEGORY: category}
        e_quote = bq.get_text().strip()
        em = bq.find("em")
        if em:
            e_author = em.get_text().strip()
            e_quote = e_quote.replace(e_author, "")
        else:
            e_author = author

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
