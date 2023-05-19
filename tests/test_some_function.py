import pytest

from quote_scraper.example import some_function


@pytest.mark.parametrize(  # noqa: WPS317
    ("first", "second", "expected"),
    [
        (1, 2, 3),
        (2, 4, 6),
        (-2, -3, -5),
        (-5, 5, 0),
    ],
)
def test_some_function(first, second, expected):
    """Example test with parametrization."""
    assert some_function(first, second) == expected
