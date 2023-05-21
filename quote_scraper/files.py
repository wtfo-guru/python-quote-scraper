"""Top-level module files for Quote Scraper."""

from pathlib import Path
from time import time

from quote_scraper.settings import settings


def get_import_path(subd: str) -> Path:
    """Return specified import subdirectory path."""
    sf = settings.cachedir
    return sf / "import" / subd


def get_stamped_import_path() -> Path:
    """Create a timestamped path to an import todo file."""
    ts = str(time())
    return get_import_path("todo") / "quote-imports-{0}.json".format(ts)  # noqa: WPS221
