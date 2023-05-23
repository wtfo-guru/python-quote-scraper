"""Top-level module settings for Quote Scraper."""

import sys
from pathlib import Path
from typing import Any, Dict, Optional

import yaml


class Ajustes(object):
    """Settings for Quote Scraper."""

    cachedir: Path
    debug: bool
    logger: Any
    verbose: bool
    config: Dict[str, str]

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
        cfg: Path = Path(
            kwargs.pop(
                "cfgfn",
                Path.home() / ".cache" / "quote-scraper.yaml",
            ),
        )
        if cfg.is_file():
            with open(cfg, "r") as yfile:
                self.config = yaml.safe_load(yfile)
        else:
            self.config = {}
            self.config["brainy_qod"] = "https://www.brainyquote.com/quote_of_the_day"
            self.config["inspiring_qod"] = "https://www.inspiringquotes.com/"

    def _get_logger(self) -> Any:
        from loguru import logger  # noqa: WPS433

        if not self.debug:
            level = "INFO" if self.verbose else "WARNING"
            logger.remove()
            logger.add(sys.stderr, level=level)
        return logger


settings = Ajustes()
