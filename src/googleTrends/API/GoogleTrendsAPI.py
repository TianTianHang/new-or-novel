import pandas as pd
from pytrends.request import TrendReq
from requests import ConnectTimeout
import resource

try:
    pytrends = TrendReq(hl='en-US', tz=360, timeout=(10, 25), retries=2,
                        backoff_factor=0.1, requests_args={'headers': {}})
except ConnectTimeout as e:
    print("无法连接到googletrends")
    exit(404)


def addgeo(df: pd.DataFrame):
    loc_df = resource.values.loc_df
    return df.reset_index().merge(loc_df, on='geoName').dropna()


# time word
def getdataovertime(kw: str, timeframe):
    pytrends.build_payload(kw_list=[kw], timeframe=timeframe, cat=0)
    df = pytrends.interest_over_time()
    df.reset_index(names='time', inplace=True)
    return df[['time', kw]]


#
def getdatabyregion(kw: str, timeframe):
    pytrends.build_payload(kw_list=[kw], timeframe=timeframe, cat=0)
    df = addgeo(pytrends.interest_by_region(resolution='COUNTRY', inc_low_vol=True, inc_geo_code=False))
    df['time'] = timeframe
    return df


# ['geoName','geoCode','lat','lon','time',word]
def getdatabyregionmultiple(kw_list: list, timeframe):
    df = pd.DataFrame()
    for kw in kw_list:
        if df.empty:
            df = getdatabyregion(kw, timeframe)
        else:
            df = df.merge(getdatabyregion(kw, timeframe), on='geoCode')
    if len(kw_list) > 1:
        df['mid'] = df[df.columns[~df.columns.isin(['geoName', 'geoCode', 'lat', 'lon', 'time'])]].median(axis=1)
        df = df[['geoName', 'geoCode', 'lat', 'lon', 'time', 'mid']]
    return df[['geoName', 'geoCode', 'lat', 'lon', 'time', kw_list[0]]]
