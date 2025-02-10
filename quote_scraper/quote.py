"""Top-level module Quote for Quote-Scraper."""

import re
from typing import List, Optional, Union

from quote_scraper import constants
from quote_scraper.kinds import StrAnyDict


class Quote:  # noqa: WPS230
    """A class to represent Quotation."""

    qid: int
    used: int
    author: str
    category: str
    quote: str
    reference: str
    julian: Optional[int]
    blessed: bool

    def __init__(self, posted: Optional[StrAnyDict] = None) -> None:
        """Construct Qdata type."""
        if posted is None:
            posted = {}
        self.qid = int(posted.get("quote_id", 0))
        self.used = int(posted.get("used_cnt", 0))
        self.author = posted.get(constants.KAUTHOR, "").strip()
        self.category = posted.get("category", "None").strip()
        self.reference = posted.get("reference", "").strip()
        self.quote = posted.get(constants.KQUOTE, "").strip()
        # Remove trailing chars [em dash, ...]
        self.quote = re.sub(r"\s*[–]$", "", self.quote)
        self.julian = posted.get("julian")
        self.blessed = self.strtobool(posted.get("blessed", "no"))

    def strtobool(self, rts: Union[str, bool]) -> bool:
        """Covert string rts to boolean."""
        if isinstance(rts, bool):
            return rts
        return rts.lower() in {"true", "1", "t", "y", "yes"}

    def validate_str(self, field: str, name: str, fmax: int) -> bool:
        """Validate string value."""
        if not field:
            raise ValueError("{0} is missing or empty".format(name))
        elif len(field) > fmax:
            raise ValueError("category length > {0}".format(constants.MAXCAT))
        return True

    def validate_int(
        self,
        field: int,
        name: str,
        fmin: int,
        fmax: Optional[int] = None,
    ) -> int:
        """Validate integer value."""
        if fmax is not None:
            if field < fmin or field > fmax:
                raise ValueError(
                    "{0} must be > {1} and <= {2}".format(name, fmin, fmax),
                )
        elif field < fmin:
            raise ValueError("{0} must be <= {1}".format(name, fmin))
        return field

    def validate(self) -> None:
        """Validate integrity."""
        if not self.category:
            self.category = "None"
        self.validate_str(self.category, "category", constants.MAXCAT)
        # only captalize first word
        self.category = self.category[0].upper() + self.category[1:]  # noqa: WPS221
        self.validate_str(self.author, constants.KAUTHOR, constants.MAXAUTHOR)
        self.validate_str(self.quote, constants.KQUOTE, constants.MAXQUOTE)
        if self.julian is not None:
            self.julian = self.validate_int(
                int(self.julian),
                "julian",
                constants.MINJULIAN,
                constants.MAXJULIAN,
            )
            self.julian = int(self.julian)
        self.used = self.validate_int(int(self.used), "used", 0)
        self.qid = self.validate_int(int(self.qid), "qid", 0)


QdataList = List[Quote]
