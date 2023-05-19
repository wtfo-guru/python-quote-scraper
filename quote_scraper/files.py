"""Top-level module for Wtf Quotes."""
import json
import os
import re
import tempfile
from enum import Enum
from errno import ENOENT
from glob import glob
from http import HTTPStatus
from pathlib import Path
from time import time
from typing import List, Tuple, Union, cast
from urllib.parse import urlparse

import requests
from flask import current_app as app
from wtforglib.kinds import StrAnyDict

from wtfquotes.brainy import scrape_brainy_qod
from wtfquotes.errors import WtfImportError
from wtfquotes.inspiring import scrape_inspiring_qod, scrape_inspiringquotes
from wtfquotes.qdata import Qdata, QdataList

KQDATUMS = "qdatums"
FAKE_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
REQUEST_TIMEOUT = (6.1, 10)













def get_import_path(subd: str) -> Path:
    """Return specified import subdirectory path."""
    sf = Path(cast(Union[str, os.PathLike[str]], app.static_folder))  # noqa: WPS221
    return sf / "import" / subd


def get_stamped_import_path() -> Path:
    """Create a timestamped path to an import todo file."""
    ts = str(time())
    return get_import_path("todo") / "quote-imports-{0}.json".format(ts)  # noqa: WPS221


def imported(source: str, errors: list[str]) -> None:
    """Move imported file to done subdirectory."""
    sp = Path(source)
    if errors:
        sp.rename(get_import_path("done") / sp.name)
    else:
        ipath = get_import_path("erred")
        sp.rename(ipath / sp.name)
        epath = ipath / "{0}.errors.txt".format(sp.name)
        with open(epath, "w") as efile:
            efile.write("\n".join(errors))
