import pandas as pd

from googleTrends import API
from resource import values


def getdatabyregion_overtime(kw_list, timeframe_list):
    df = pd.DataFrame()
    for timeframe in timeframe_list:
        origin = API.getdatabyregionmultiple(kw_list, timeframe)
        if df.empty:
            df = origin[values.loc_columns + ['mid', 'time']]
        else:
            df = df.append(origin[values.loc_columns + ['mid', 'time']], ignore_index=True)
    return df


def getdatabyovertime(kw_list, timeframe):
    df = pd.DataFrame()
    for kw in kw_list:
        if df.empty:
            df = API.getdataovertime(kw, timeframe)
        else:
            df = df.merge(API.getdataovertime(kw, timeframe), on='time')
    if len(kw_list) == 1:
        return df[['time', kw_list[0]]]
    df['sum'] = df.iloc[..., 1:].sum(axis=1)
    return df[['time', 'sum']]
