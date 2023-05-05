import numpy as np
import pandas as pd
import plotly.graph_objects as go
from utils.helper import getmapsource

color_map = [
    [0.0, "#00FF00"],
    [0.3, '#BDDF31'],
    [0.4, '#FFFF00'],
    [0.6, '#FF6600'],
    [1, "red"]
]


def MinMaxScaler(df, start, end):
    return (df - df.min()) / (df.max() - df.min() + 1) * (end - start) + start


def hotmapbyword(df: pd.DataFrame, title):
    frames = []
    for index, kw in enumerate(df.columns[5:]):
        for i, (timeframe, df_time) in enumerate(df.groupby(by='timeframe')):
            trace = go.Densitymapbox(lon=df_time.lon, lat=df_time.lat, z=df_time[kw],
                                     customdata=np.stack((df_time.geoName, df_time.geoCode), axis=-1),
                                     meta=[kw, timeframe], visible=True, opacity=0.5,
                                     radius=list(MinMaxScaler(df_time[kw], 1, 60).fillna(1)),
                                     hovertemplate='%{customdata[0]} %{customdata[1]}<br>'
                                                   'timeframe:%{meta[1]}<br>'
                                                   'lat: %{lat:.2f},lon:%{lon:.2f}<br>'
                                                   '%{meta[0]}:%{z}',
                                     colorbar=dict(title={"text": kw}), zmin=0,
                                     zmax=df_time[kw].quantile(0.95), colorscale=color_map)

            frames.append(go.Frame(data=trace, name="{kw}-{time}".format(kw=kw, time=timeframe), group=kw))

    # mapbox使用Bing map
    layout = go.Layout(mapbox=dict(style="white-bg",
                                   layers=[
                                       dict(
                                           below="traces",
                                           sourcetype="raster",
                                           # 地图提供商
                                           sourceattribution="Bing Map",
                                           # 地图块请求api
                                           source=getmapsource()
                                       )
                                   ]
                                   ),
                       margin=dict(l=0, r=0, b=0, t=0), title=title)

    fig = go.Figure(data=[], layout=layout, frames=frames)
    return fig
