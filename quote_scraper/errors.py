"""Top-level module errors for Quote-Scrape."""

import os
from errno import ENOENT
from typing import NoReturn


class QuoteScrapeImportError(Exception):
    """Class respresting import quote execptions."""


class QuoteScrapeNotYetError(Exception):
    """Class respresting not implemented yet execptions."""


def raise_fnfe(file_name: str) -> NoReturn:
    """Raise FileNotFoundError for file_name."""
    raise FileNotFoundError(ENOENT, os.strerror(ENOENT), file_name)
