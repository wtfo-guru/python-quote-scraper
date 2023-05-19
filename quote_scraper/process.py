from quote_scraper.kinds import StrAnyDict

def process_cached(source: str) -> Tuple[QdataList, str]:  # noqa: WPS210 C901 WPS231
    """Process cached quotes."""
    cdata: StrAnyDict
    with open(Path(source)) as json_file:
        cdata = json.load(json_file)

    if constants.KQDATUMS in cdata:
        datums: QdataList = []
        for dat in cdata.get(contants.KQDATUMS, []):
            datums.append(Qdata(dat))
        return datums, source
    for key in ("url", "author", "category", "html"):
        if key not in cdata:
            raise KeyError("Missing required key: {0}".format(key))
