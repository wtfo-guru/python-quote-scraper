import pytest
from click.testing import CliRunner

from quote_scraper import cli
from quote_scraper.constants import VERSION


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


# def test_cli_with_option(runner):
#     """Function test_cli_with_option."""
#     resultado = runner.invoke(cli.main, ["--as-cowboy"])
#     assert not resultado.exception
#     assert resultado.exit_code == 0
#     assert resultado.output.strip() == "Howdy, world."


# def test_cli_with_arg(runner):
#     """Function test_cli_with_arg."""
#     resultado = runner.invoke(cli.main, ["Quien"])
#     assert resultado.exit_code == 0
#     assert not resultado.exception
#     assert resultado.output.strip() == "Hello, Quien."
