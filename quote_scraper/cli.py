"""Top-level module cli for Quote Scraper."""

import sys
from pathlib import Path
from typing import List, Tuple

import click

from quote_scraper.constants import VERSION
from quote_scraper.quote import QdataList
from quote_scraper.scraper import scrape_quotes
from quote_scraper.settings import settings


@click.command()
@click.option(
    "--author",
    "-a",
    default="unknown",
    help="Specify author of quotes.",
)
@click.option(
    "--brainy",
    "-b",
    is_flag=True,
    show_default=True,
    default=False,
    help="Specify scrape brainyquotes of the day.",
)
@click.option(
    "--cache",
    default=str(Path.home() / ".cache" / "quote-scraper"),
    help="Specify cache directory (default ~/.cache/quote-scraper)",
)
@click.option(
    "--category",
    "-c",
    default="Life Lessons",
    help="Specify category of quotes.",
)
@click.option(
    "--debug/--no-debug",
    "-d",
    default=False,
    help="Specify debug mode, default: False",
)
@click.option(
    "--inspiring",
    "-i",
    is_flag=True,
    show_default=True,
    default=False,
    help="Specify scrape inquiring quote of the day.",
)
@click.option(
    "--url",
    "-u",
    default="",
    help="Specify scrape url.",
)
@click.option(
    "--verbose/--no-verbose",
    "-v",
    default=False,
    help="Specify verbose mode, default: False",
)
@click.version_option(VERSION)
def main(  # noqa: WPS211, WPS216
    author,
    brainy,
    cache,
    category,
    inspiring,
    debug,
    url,
    verbose,
) -> int:
    """Tool to scrape quotes from web pages."""
    settings.initialize(debug=debug, verbose=verbose, cachedir=cache)
    urls: List[str] = []
    if brainy:
        urls.append(settings.config["brainy_qod"])
    if inspiring:
        urls.append(settings.config["inspiring_qod"])
    if url:
        urls.append(url)
    resultados: List[Tuple[QdataList, str]] = []
    for source in urls:
        resultados.append(scrape_quotes(author, category, source))
    print(resultados)  # noqa: WPS421
    return 0


if __name__ == "__main__":  # pragma no cover
    sys.exit(main())
# vim:ft=py noqa: E800
