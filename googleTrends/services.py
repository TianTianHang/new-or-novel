import pandas as pd
from googleTrends import API
from resource import values


def getdatabyregion_overtime(kw_list, timeframe_list):
    df = pd.DataFrame()
    for timeframe in timeframe_list:
        origin = API.GoogleTrendsAPI.getdatabyregionmultiple(kw_list, timeframe)
        if df.empty:
            df = origin[values.loc_columns+['mid', 'time']]
        else:
            df = df.append(origin[values.loc_columns+['mid', 'time']],ignore_index=True)
    return df
