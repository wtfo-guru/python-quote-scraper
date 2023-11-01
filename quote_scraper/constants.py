"""Top-level module constants for Quote-Scraper."""

VERSION = "0.1.0-dev5"
KCATEGORY = "category"
KAUTHOR = "author"
KQUOTE = "quote"
KQDATUMS = "qdatums"

FAKE_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"  # noqa: E501
REQUEST_TIMEOUT = (6.1, 10)
SCRAPEOPS_TIMEOUT = (6, 60)

MINJULIAN = 1
MAXJULIAN = 366
MAXQUOTE = 512
MAXCAT = 32
MAXAUTHOR = 128
MAXFLD16 = 16
MAXFLD50 = 50
MAXFLD80 = 80
