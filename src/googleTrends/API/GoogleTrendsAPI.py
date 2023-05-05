import functools

import pandas as pd
from pytrends.request import TrendReq
from requests import ConnectTimeout


class GoogleTrendsAPI:
    try:
        pytrends = TrendReq(hl='en-US', tz=360, timeout=(10, 25), retries=2,
                            backoff_factor=0.1, requests_args={'headers': {}})
    except ConnectTimeout as e:
        print("无法连接到googletrends")
    loc_df = pd.read_csv('src/googleTrends/API/geoLocation.csv', sep='\t')

    @classmethod
    def addGeo(cls, df: pd.DataFrame):
        return cls.loc_df.merge(df, on='geoCode')

    # time word
    @classmethod
    # 缓存函数结果
    @functools.lru_cache(maxsize=100)
    def getDataOvertime(cls, kw: str, timeframe, geo=''):
        cls.pytrends.build_payload(kw_list=[kw], timeframe=timeframe, cat=0, geo=geo)
        df = cls.pytrends.interest_over_time()
        df.reset_index(names='time', inplace=True)
        return df[['time', kw]]

    @classmethod
    def getDataOvertimeMultirange(cls, kw: str, timeframe_list: list, geo=''):
        cls.pytrends.build_payload(kw_list=[kw], timeframe=timeframe_list, cat=0, geo=geo)
        df = cls.pytrends.multirange_interest_over_time()
        return df

    # resolution='DMA' |'CITY'| 'REGION'
    @classmethod
    @functools.lru_cache(maxsize=100)
    def getDataByRegion(cls, kw: str, timeframe, resolution='COUNTRY'):
        cls.pytrends.build_payload(kw_list=[kw], timeframe=timeframe, cat=0)
        df = cls.pytrends.interest_by_region(resolution=resolution, inc_low_vol=True, inc_geo_code=True).reset_index()
        return df[['geoName', 'geoCode', kw]]

    # 清除缓存
    @classmethod
    def deleteCache(cls):
        cls.getDataByRegion.cache_clear()
        cls.getDataOvertime.cache_clear()
