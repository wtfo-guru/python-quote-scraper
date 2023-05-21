"""Top-level module cli for Quote Scraper."""

import sys
from pathlib import Path
from typing import AnyStr

import click
from click.core import Context

from quote_scraper.settings import settings


def print_version(ctx: Context, aparam: AnyStr, avalue: AnyStr) -> None:
    """Prints package version and exits.

    Parameters
    ----------
    ctx : Context
        click context object
    aparam : AnyStr
        dunno
    avalue : AnyStr
        dunno
    """
    if not avalue or ctx.resilient_parsing:
        return
    print("Not implemented yet!")
    ctx.exit()


@click.command()
@click.option(
    "--cache",
    "-c",
    default=str(Path.home() / ".cache" / "quote-scraper"),
    help="Specify debug mode, default: False",
)
@click.option(
    "--debug/--no-debug",
    "-d",
    default=False,
    help="Specify debug mode, default: False",
)
@click.option(
    "--verbose/--no-verbose",
    "-v",
    default=False,
    help="Specify verbose mode, default: False",
)
@click.option(
    "-V",
    "--version",
    is_flag=True,
    expose_value=False,
    callback=print_version,
    is_eager=True,
    help="Show version and exit",
)
def main(cache, debug, verbose):
    """Tool to scrape quotes from web pages."""
    settings.initialize(debug=debug, verbose=verbose, cachedir=cache)


if __name__ == "__main__":  # pragma no cover
    sys.exit(main())

# vim:ft=py noqa: E800
