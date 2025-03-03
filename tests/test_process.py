import pytest
import testfixtures
from click.testing import CliRunner

from quote_scraper import process
from quote_scraper.constants import VERSION

HELP = """Usage: main [OPTIONS]

  Tool to process cached quotes.

Options:
  --cache TEXT                  Specify cache directory (default ~/.cache/quote-
                                scraper)
  -d, --debug / --no-debug      Specify debug mode, default: False
  -f, --file TEXT               Specify cached file to process.
  -v, --verbose / --no-verbose  Specify verbose mode, default: False
  --version                     Show the version and exit.
  --help                        Show this message and exit.
"""


@pytest.fixture
def runner():
    """Function runner."""
    return CliRunner()


def test_process_version(runner):
    """Function test_cli_version."""
    test_result = runner.invoke(process.main, ["--version"])
    assert not test_result.exception
    assert test_result.exit_code == 0
    assert test_result.output.strip() == "main, version {0}".format(VERSION)


def test_process_help(runner):
    """Function test_cli_version."""
    test_result = runner.invoke(process.main, ["--help"])
    assert not test_result.exception
    assert test_result.exit_code == 0
    testfixtures.compare(HELP, test_result.output)


def test_process_brainy_qod(runner):
    """Function test_cli_version."""
    test_result = runner.invoke(
        process.main,
        ["-f", "./tests/data/cached-brainy-qod.json"],
    )
    assert not test_result.exception
    assert test_result.exit_code == 0
    authors = [
        "Mencius",
        "Stephen Jay Gould",
        "Henry Wadsworth Longfellow",
        "Ludwig Mies van der Rohe",
        "Michel de Montaigne",
        "Frances Wright",
    ]
    for author in authors:
        assert author in test_result.output


def test_process_inspire_qod(runner):
    """Function test_cli_version."""
    test_result = runner.invoke(
        process.main,
        ["-f", "./tests/data/cached-inspire-qod.json"],
    )
    assert not test_result.exception
    assert test_result.exit_code == 0
    assert "Miriam Miranda" in test_result.output


def test_process_inspire_bedtime(runner):
    """Function test_cli_version."""
    test_result = runner.invoke(
        process.main,
        ["-f", "./tests/data/cached-inspire-bedtime.json"],
    )
    assert not test_result.exception
    assert test_result.exit_code == 0
    count = 0
    for line in test_result.output.splitlines():
        if "quote_id" in line:
            count += 1
    assert count == 15


def test_process_inspire_running(runner):
    """Function test_cli_version."""
    test_result = runner.invoke(
        process.main,
        ["-f", "./tests/data/cached-inspire-running.json"],
    )
    assert not test_result.exception
    assert test_result.exit_code == 0
    count = 0
    for line in test_result.output.splitlines():
        if "quote_id" in line:
            count += 1
    assert count == 15
