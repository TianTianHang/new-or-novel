import numpy as np
import pandas as pd
import plotly.graph_objects as go

from myplotly.temples import base_factory, template_layout, Bing_Map_Template


def MinMaxScaler(df, start, end):
    return (df - df.min()) / (df.max() - df.min() + 1) * (end - start) + start


def Multi_time_word_express_mapbox(df: pd.DataFrame, title, type, index, **kwargs):
    func_map = {'choroplethmapbox': choropleth_map,
                'densitymapbox': density_map}
    frames = []
    for kw in df.columns[5:]:
        for timeframe, df_time in df.groupby(by='timeframe'):
            trace = base_factory(type=type, index=index, z=df_time[kw],
                                 customdata=np.stack((df_time.geoName, df_time.geoCode), axis=-1), meta=[kw, timeframe],
                                 colorbar=dict(title={"text": kw, "font": {"size": 12}}, ypad=0), zmin=0,
                                 zmax=df_time[kw].quantile(0.95))
            trace_update = func_map[type](df_time, kw, timeframe, **kwargs)
            trace.update(**trace_update)
            frames.append(go.Frame(data=trace, name="{kw}-{time}".format(kw=kw, time=timeframe), group=kw))

    # mapbox使用Bing map
    layout = template_layout()
    layout.update(**Bing_Map_Template, title=title)
    fig = go.Figure(data=[], layout=layout, frames=frames)
    return fig


def Multi_time_word_express_basic(df: pd.DataFrame, title, type, index, **kwargs):
    func_map = {'scatter': scatter_basic}
    frames = []
    for timeframe, df_time in df.groupby(by='timeframe'):
        all_trace = []
        for kw in df.columns[2:]:
            trace = base_factory(type=type, index=index, x=df_time.time, y=df_time[kw], name=kw,
                                 meta=[kw, timeframe])
            trace_update = func_map[type](df_time, kw, timeframe, **kwargs)
            trace.update(**trace_update)
            all_trace.append(trace)
            frames.append(go.Frame(data=trace, name="{kw}-{time}".format(kw=kw, time=timeframe), group=kw))
        frames.append(go.Frame(data=all_trace, name="all-{time}".format(time=timeframe), group='all'))
    layout = template_layout()
    layout.update(title=title)
    fig = go.Figure(data=[], layout=layout, frames=frames)
    return fig


def choropleth_map(df_time, kw, timeframe, **kwargs):
    return dict(locations=df_time.geoName, **kwargs)


def density_map(df_time, kw, timeframe, **kwargs):
    return dict(radius=list(MinMaxScaler(df_time[kw], 1, 60).fillna(1)), lon=df_time.lon, lat=df_time.lat, **kwargs)


def scatter_basic(df_time, kw, timeframe, **kwargs):
    return dict(**kwargs)


def choropleth_mapbyword(df: pd.DataFrame, title, index, **kwargs):
    return Multi_time_word_express_mapbox(df, title, type='choroplethmapbox', index=index, **kwargs)


def density_mapbyword(df: pd.DataFrame, title, index, **kwargs):
    return Multi_time_word_express_mapbox(df, title, type='densitymapbox', index=index, **kwargs)


def linechart(df: pd.DataFrame, title, index, **kwargs):
    return Multi_time_word_express_basic(df, title, type='scatter', index=index, **kwargs)
