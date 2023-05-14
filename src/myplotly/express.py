import numpy as np
import pandas as pd

from myplotly.temples import mapbox_factory, template_layout, Bing_Map_Template
import plotly.graph_objects as go


def Multi_time_word_express_mapbox(df: pd.DataFrame, title, type, index):
    frames = []
    for kw in df.columns[5:]:
        for timeframe, df_time in df.groupby(by='timeframe'):
            trace = mapbox_factory(type=type, index=index,
                                   z=df_time[kw], locations=df_time.geoName,
                                   customdata=np.stack((df_time.geoName, df_time.geoCode), axis=-1),
                                   meta=[kw, timeframe],
                                   colorbar=dict(title={"text": kw}), zmin=0,
                                   zmax=df_time[kw].quantile(0.95))

            frames.append(go.Frame(data=trace, name="{kw}-{time}".format(kw=kw, time=timeframe), group=kw))

    # mapbox使用Bing map
    layout = template_layout()
    layout.update(**Bing_Map_Template, title=title)
    fig = go.Figure(data=[], layout=layout, frames=frames)
    return fig


def choropleth_mapbyword(df: pd.DataFrame, title, geojson, index):
    fig = Multi_time_word_express_mapbox(df, title, type='choroplethmapbox', index=index)
    fig.update_traces(geojson=geojson)
    return fig


def density_mapbyword(df: pd.DataFrame, title, index):
    return Multi_time_word_express_mapbox(df, title, type='densityhmapbox', index=index)
