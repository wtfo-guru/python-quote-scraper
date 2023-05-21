"""Top-level module settings for Quote Scraper."""

import sys
from pathlib import Path
from typing import Any, Optional


class Ajustes(object):
    """Settings for Quote Scraper."""

    cachedir: Path
    debug: bool
    logger: Any
    verbose: bool

    def initialize(self, **kwargs) -> None:
        """Constructs a new Quote Scraper."""
        self.debug = kwargs.pop("debug", False)
        self.verbose = kwargs.pop("verbose", False)
        self.cachedir = kwargs.pop(
            "cachedir",
            Path.home() / ".cache" / "quote-scraper",
        )
        logger: Optional[Any] = kwargs.pop("logger", None)
        if logger is None:
            self.logger = self._get_logger()

    def _get_logger(self) -> Any:
        from loguru import logger  # noqa: WPS433

        if not self.debug:
            level = "INFO" if self.verbose else "WARNING"
            logger.remove()
            logger.add(sys.stderr, level=level)
        return logger


settings = Ajustes()
