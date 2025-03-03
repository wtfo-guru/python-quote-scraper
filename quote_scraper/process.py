"""Top-level module cli for Quote Scraper."""

import pprint
import sys
from pathlib import Path

import click
from wtforglib.errors import raise_filenotfound_if

from quote_scraper.cache import process_cached
from quote_scraper.constants import VERSION
from quote_scraper.settings import settings


@click.command()
@click.option(
    "--cache",
    default=str(Path.home() / ".cache" / "quote-scraper"),
    help="Specify cache directory (default ~/.cache/quote-scraper)",
)
@click.option(
    "--debug/--no-debug",
    "-d",
    default=False,
    help="Specify debug mode, default: False",
)
@click.option(
    "--file",
    "-f",
    "filename",
    type=str,
    help="Specify cached file to process.",
)
@click.option(
    "--verbose/--no-verbose",
    "-v",
    default=False,
    help="Specify verbose mode, default: False",
)
@click.version_option(VERSION)
def main(  # noqa: WPS216
    cache,
    debug,
    filename,
    verbose,
) -> int:
    """Tool to process cached quotes."""
    settings.initialize(debug=debug, verbose=verbose, cachedir=cache)
    raise_filenotfound_if(filename)
    pprint.pp(process_cached(filename))
    return 0


if __name__ == "__main__":  # pragma no cover
    sys.exit(main())
# vim:ft=py noqa: E800
