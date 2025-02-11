import pytest
import testfixtures
from click.testing import CliRunner

from quote_scraper import cli
from quote_scraper.constants import VERSION

HELP = """Usage: main [OPTIONS]

  Tool to scrape quotes from web pages.

Options:
  -a, --author TEXT             Specify author of quotes.
  -b, --brainy                  Specify scrape brainyquotes of the day.
  --cache TEXT                  Specify cache directory (default ~/.cache/quote-
                                scraper)
  -c, --category TEXT           Specify category of quotes.
  -d, --debug / --no-debug      Specify debug mode, default: False
  -i, --inspiring               Specify scrape inquiring quote of the day.
  -u, --url TEXT                Specify scrape url.
  -v, --verbose / --no-verbose  Specify verbose mode, default: False
  --version                     Show the version and exit.
  --help                        Show this message and exit.
"""


@pytest.fixture
def runner():
    """Function runner."""
    return CliRunner()


def test_cli_version(runner):
    """Function test_cli_version."""
    test_result = runner.invoke(cli.main, ["--version"])
    assert not test_result.exception
    assert test_result.exit_code == 0
    assert test_result.output.strip() == "main, version {0}".format(VERSION)


def test_cli_help(runner):
    """Function test_cli_version."""
    test_result = runner.invoke(cli.main, ["--help"])
    assert not test_result.exception
    assert test_result.exit_code == 0
    testfixtures.compare(HELP, test_result.output)
