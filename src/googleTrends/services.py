import pandas as pd

from googleTrends.API import *
import gevent


# geoName lat lon geoCode time words ......
def getDataByRegionAndOvertime(kw_list: list, timeframe_list: list):
    result = []
    for timeframe in timeframe_list:
        heatValue = []
        for kw in kw_list:
            heatValue.append(GoogleTrendsAPI.getDataByRegion(kw, timeframe))
        var: pd.DataFrame = pd.concat(heatValue, axis=1).T.drop_duplicates().T
        var.insert(1, 'time', timeframe)
        result.append(var)
    df = pd.concat(result)
    return GoogleTrendsAPI.addGeo(df)


def getDataByRegionAndOvertimeGevent(kw_list: list, timeframe_list: list):
    result = []
    greenlets = [gevent.spawn(GoogleTrendsAPI.getDataByRegion, kw, timeframe) for timeframe in timeframe_list for kw in kw_list]
    # wait for all greenlets to finish and get their results
    heatValue = [g.value for g in gevent.joinall(greenlets)]
    for i, timeframe in enumerate(timeframe_list):
        var = heatValue[i * len(kw_list)]
        for j in range(i * len(kw_list)+1, i * len(kw_list) + len(kw_list)):
            var = var.merge(heatValue[j], on=['geoName', 'geoCode'],)
        var.insert(1, 'time', timeframe)
        result.append(var)
    df = pd.concat(result)
    return GoogleTrendsAPI.addGeo(df)


# time words ......
def getDataOvertimeMultiWord(kw_list: list, timeframeOrList: str | list):
    getDataFun = GoogleTrendsAPI.getDataOvertime
    # if isinstance(timeframeOrList, list):
    #     getDataFun = GoogleTrendsAPI.getDataOvertimeMultirange
    result = []
    for kw in kw_list:
        result.append(getDataFun(kw, timeframeOrList))
    var = pd.concat(result, axis=1).T.drop_duplicates().T
    return var
