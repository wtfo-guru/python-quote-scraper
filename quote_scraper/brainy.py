"""Top-level module for Wtf Quotes."""
import re

from bs4 import BeautifulSoup

from quote_scraper.constants import KAUTHOR, KCATEGORY, KQUOTE
from quote_scraper.kinds import StrAnyDict
from quote_scraper.quote import QdataList, Quote
from quote_scraper.settings import settings


def scrape_brainy_qod(cdata: dict[str, str]) -> QdataList:  # noqa: WPS210 WPS231
    """Scrape brainyquotes quote of the day page."""
    qnbr = 0
    soup = BeautifulSoup(cdata.get("html"), "html.parser")
    display = re.compile("^display:")
    qotd = re.compile("Quote of the Day", re.IGNORECASE)
    # <div class="grid-item qb clearfix bqQt">
    qdatums: QdataList = []
    for div in soup.find_all("div", class_="grid-item qb clearfix bqQt"):
        qpost: StrAnyDict = {KCATEGORY: "None"}
        # <h2 class="qotd-h2">Funny Quote Of the Day</h2>
        qnbr += 1
        category = div.find("h2", class_="qotd-h2")
        if category:
            qpost[KCATEGORY] = (
                qotd.sub("", category.get_text()).strip().replace("Funny", "Humor")
            )
            settings.logger.debug("category: {0}".format(qpost[KCATEGORY]))
            if not qpost[KCATEGORY]:
                qpost[KCATEGORY] = "None"
            # <div style="display: flex;justify-content: space-between">
        quote = div.find("div", {"style": display})
        if quote:
            qpost[KQUOTE] = quote.get_text().strip()
            settings.logger.debug("quote: {0}".format(qpost[KQUOTE]))
        else:  # pragma: no cover
            settings.logger.warn("Scrape quote number {0} failed.".format(qnbr))
            continue
        # <a href="/authors/jonathan-swift-quotes"
        #   class="bq-aut qa_155269 oncl_a"
        #   title="view author">Jonathan Swift</a>
        author = div.find("a", {"title": "view author"})
        if author:
            qpost[KAUTHOR] = author.get_text().strip()
            settings.logger.debug("author: {0}".format(qpost[KAUTHOR]))
        else:  # pragma: no cover
            settings.logger.warn("Scrape author number {0} failed.".format(qnbr))
            continue
        qdatums.append(Quote(qpost))
    return qdatums
