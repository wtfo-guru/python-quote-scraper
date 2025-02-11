"""Top-level module settings for Quote Scraper."""

import sys
from pathlib import Path
from typing import Any, Dict, Optional

import yaml


class Ajustes:
    """Settings for Quote Scraper."""

    cachedir: Path
    debug: bool
    logger: Any
    verbose: bool
    config: Dict[str, str]

    def __init__(self) -> None:
        """Initialize settings."""
        """Constructs a new Quote Scraper."""
        self.debug = False
        self.verbose = False
        self.cachedir = Path.home() / ".cache" / "quote-scraper"
        self.logger = self._get_logger()
        cfg: Path = Path.home() / ".config" / "quote-scraper.yaml"
        if cfg.is_file():
            with open(cfg, "r") as yfile:
                self.config = yaml.safe_load(yfile)
        else:
            self.config = {}
        if "brainy_qod" not in self.config:
            self.config["brainy_qod"] = "https://www.brainyquote.com/quote_of_the_day"
        if "inspiring_qod" not in self.config:
            self.config["inspiring_qod"] = "https://www.inspiringquotes.com/"

    def initialize(self, **kwargs) -> None:
        """Constructs a new Quote Scraper."""
        self.debug = kwargs.pop("debug", False)
        self.verbose = kwargs.pop("verbose", False)
        self.cachedir = kwargs.pop(
            "cachedir",
            Path.home() / ".cache" / "quote-scraper",
        )
        logger: Optional[Any] = kwargs.pop("logger", None)
        if logger is not None:
            self.logger = logger
        cfg = kwargs.get("cfgfn", "")
        if cfg:
            with open(cfg, "r") as yfile:
                self.config = yaml.safe_load(yfile)

    def _get_logger(self) -> Any:
        from loguru import logger  # noqa: WPS433

        if not self.debug:
            level = "INFO" if self.verbose else "WARNING"
            logger.remove()
            logger.add(sys.stderr, level=level)
        return logger


settings = Ajustes()
