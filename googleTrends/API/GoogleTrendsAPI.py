
def getdataovertime(kw: str, timeframe):
    pytrends.build_payload(kw_list=[kw], timeframe=timeframe, cat=0)
    return pytrends.interest_over_time()


def getdatabyregion(kw: str, timeframe):
    pytrends.build_payload(kw_list=[kw], timeframe=timeframe, cat=0)
    return pytrends.interest_by_region(resolution='COUNTRY', inc_low_vol=True, inc_geo_code=False)

