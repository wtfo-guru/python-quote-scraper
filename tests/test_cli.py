import pytest
from click.testing import CliRunner

from quote_scraper import cli


@pytest.fixture()
def runner():
    """Function runner."""
    return CliRunner()


def test_cli(runner):
    """Function test_cli."""
    resultado = runner.invoke(cli.main)
    assert resultado.exit_code == 0
    assert not resultado.exception
    assert resultado.output.strip() == "Hello, world."


def test_cli_with_option(runner):
    """Function test_cli_with_option."""
    resultado = runner.invoke(cli.main, ["--as-cowboy"])
    assert not resultado.exception
    assert resultado.exit_code == 0
    assert resultado.output.strip() == "Howdy, world."


def test_cli_with_arg(runner):
    """Function test_cli_with_arg."""
    resultado = runner.invoke(cli.main, ["Quien"])
    assert resultado.exit_code == 0
    assert not resultado.exception
    assert resultado.output.strip() == "Hello, Quien."
