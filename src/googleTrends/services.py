import pandas as pd

from googleTrends import API


def getdatabyregion_overtime(kw_list: list, timeframe_list: list):
    df = pd.DataFrame()
    for timeframe in timeframe_list:
        origin = API.getdatabyregionmultiple(kw_list, timeframe)
        if df.empty:
            df = origin
        else:
            df = df.append(origin, ignore_index=True)
    if len(kw_list) == 1:
        df.rename(columns={kw_list[0]: 'HeatValue'}, inplace=True)
        df['word'] = kw_list[0]
    else:
        df.rename(columns={'mid': 'HeatValue'}, inplace=True)
        df['word'] = 'mid'

    return df


def getdatabyovertime(kw_list: list, timeframe):
    df = pd.DataFrame()
    for kw in kw_list:
        if df.empty:
            df = API.getdataovertime(kw, timeframe)
        else:
            df = df.merge(API.getdataovertime(kw, timeframe), on='time')
    if len(kw_list) == 1:
        df.rename(columns={kw_list[0]: 'HeatValue'}, inplace=True)
        df['word'] = kw_list[0]
        return df[['time', 'HeatValue', 'word']]
    df['HeatValue'] = df.iloc[..., 1:].sum(axis=1)
    df['word'] = 'sum'
    return df[['time', 'HeatValue', 'word']]
