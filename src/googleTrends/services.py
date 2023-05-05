import pandas as pd
from googleTrends.API.GoogleTrendsAPI import GoogleTrendsAPI
import gevent

API = GoogleTrendsAPI


# geoName lat lon geoCode time words ......
def getDataByRegionAndOvertime(kw_list: list, timeframe_list: list):
    result = []
    if not kw_list or not timeframe_list:
        return None
    for timeframe in timeframe_list:
        heatValue = []
        for kw in kw_list:
            data = API.getDataByRegion(kw, timeframe)
            if data is not None:
                heatValue.append(data)
        var: pd.DataFrame = pd.concat(heatValue, axis=1).T.drop_duplicates().T
        var.insert(1, 'timeframe', timeframe)
        result.append(var)
    df = pd.concat(result)
    return API.addGeo(df)


def getDataByRegionAndOvertimeGevent(kw_list: list, timeframe_list: list):
    result = []
    greenlets = [gevent.spawn(API.getDataByRegion, kw, timeframe) for timeframe in timeframe_list for kw in
                 kw_list]
    # wait for all greenlets to finish and get their results
    heatValue = [g.value for g in gevent.joinall(greenlets)]
    for i, timeframe in enumerate(timeframe_list):
        var = heatValue[i * len(kw_list)]
        for j in range(i * len(kw_list) + 1, i * len(kw_list) + len(kw_list)):
            var = var.merge(heatValue[j], on=['geoName', 'geoCode'], )
        var.insert(1, 'timeframe', timeframe)
        result.append(var)
    df = pd.concat(result)
    return API.addGeo(df)


# time words ......
def getDataOvertimeMultiWord(kw_list: list, timeframeOrList: str | list):
    result = []
    for timeframe in timeframeOrList:
        heatValue = []
        for kw in kw_list:
            heatValue.append(API.getDataOvertime(kw, timeframe))
        var = pd.concat(heatValue, axis=1).T.drop_duplicates().T
        var.insert(1, 'timeframe', timeframe)
        result.append(var)
    df = pd.concat(result)
    return df
