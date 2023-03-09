import pandas as pd
from pytrends.request import TrendReq
from requests import ConnectTimeout
import resource

try:
    pytrends = TrendReq(hl='en-US', tz=360, timeout=(10, 25), retries=2,
                        backoff_factor=0.1)
except ConnectTimeout as e:
    print("无法连接到googletrends")
    exit(404)


def addgeo(df: pd.DataFrame):
    loc_df = resource.values.loc_df
    return df.reset_index().merge(loc_df, on='geoName').dropna()


def getdataovertime(kw: str, timeframe):
    pytrends.build_payload(kw_list=[kw], timeframe=timeframe, cat=0)
    df = pytrends.interest_over_time()
    df.reset_index(names='time', inplace=True)
    return df[['time', kw]]


def getdatabyregion(kw: str, timeframe):
    pytrends.build_payload(kw_list=[kw], timeframe=timeframe, cat=0)
    df = addgeo(pytrends.interest_by_region(resolution='COUNTRY', inc_low_vol=True, inc_geo_code=False))
    df['time'] = timeframe
    return df


def getdatabyregionmultiple(kw_list: list, timeframe):
    df = pd.DataFrame()
    for kw in kw_list:
        pytrends.build_payload(kw_list=[kw], timeframe=timeframe, cat=0)
        if df.empty:
            df = pytrends.interest_by_region(resolution='COUNTRY', inc_low_vol=True, inc_geo_code=False)
        else:
            df = df.join(pytrends.interest_by_region(resolution='COUNTRY', inc_low_vol=True, inc_geo_code=False))
    df = addgeo(df)
    df['mid'] = df[df.columns[~df.columns.isin(resource.values.loc_columns)]].median(axis=1)
    df['time'] = timeframe
    return df
