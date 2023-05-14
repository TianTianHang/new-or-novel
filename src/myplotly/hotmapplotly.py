import numpy as np
import pandas as pd
import plotly.graph_objects as go
from utils.helper import getmapsource
from myplotly.temples.temples import TEMPLATES, mapbox_factory, Bing_Map_Template


def MinMaxScaler(df, start, end):
    return (df - df.min()) / (df.max() - df.min() + 1) * (end - start) + start


def hotmapbyword(df: pd.DataFrame, title):
    frames = []
    for index, kw in enumerate(df.columns[5:]):
        for i, (timeframe, df_time) in enumerate(df.groupby(by='timeframe')):
            trace = mapbox_factory(type='densitymapbox', name='density_bingmap',
                                   lon=df_time.lon, lat=df_time.lat, z=df_time[kw],
                                   customdata=np.stack((df_time.geoName, df_time.geoCode), axis=-1),
                                   meta=[kw, timeframe], visible=True, opacity=0.5,
                                   radius=list(MinMaxScaler(df_time[kw], 1, 60).fillna(1)),
                                   hovertemplate='%{customdata[0]} %{customdata[1]}<br>'
                                                 'timeframe:%{meta[1]}<br>'
                                                 'lat: %{lat:.2f},lon:%{lon:.2f}<br>'
                                                 '%{meta[0]}:%{z}',
                                   colorbar=dict(title={"text": kw}), zmin=0,
                                   zmax=df_time[kw].quantile(0.95)
                                   )

            frames.append(go.Frame(data=trace, name="{kw}-{time}".format(kw=kw, time=timeframe), group=kw))

    # mapbox使用Bing map
        # mapbox使用Bing map
        layout = TEMPLATES['layout']
        layout.update(**Bing_Map_Template, title=title)

    fig = go.Figure(data=frames[0].data, layout=layout, frames=frames)
    return fig
