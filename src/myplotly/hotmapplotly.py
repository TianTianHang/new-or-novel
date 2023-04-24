import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import requests

bing_map_token = 'AlokyiLvd54vljDRnjUfkF_STJ2nGNZ9N1j_FAFtAMERXrTc57hJdKRyq6yc2EDk'
req = requests.get('https://dev.virtualearth.net/REST/V1/Imagery/Metadata/CanvasLight?output=json&include'
                   '=ImageryProviders&key={BingMapsKey}'.format(BingMapsKey=bing_map_token))
url_json = req.json()['resourceSets'][0]['resources'][0]
source = [url_json['imageUrl'].replace('{subdomain}', sub) for sub in
          url_json['imageUrlSubdomains']]


def MinMaxScaler(df, start, end):
    return (df - df.min()) / (df.max() - df.min() + 1) * (end - start) + start


def hotmapbyword(df: pd.DataFrame, title):
    color_map = [
        [0.0, "#00FF00"],
        [0.3, '#BDDF31'],
        [0.4, '#FFFF00'],
        [0.6, '#FF6600'],
        [1,  "red"]
    ]
    # fig = px.density_mapbox(df, lat='lat', lon='lon', z='HeatValue', hover_name='geoName',
    #                         center={'lat': 43, 'lon': 12}, zoom=1, animation_frame='time',
    #                         animation_group='geoName', radius=30, title=title,
    #                         color_continuous_scale=color_map, opacity=0.5,
    #                         range_color=[0, df['HeatValue'].quantile(0.9)])
    traces = []
    frames = []
    for index, kw in enumerate(df.columns[5:]):
        for i, (time, df_time) in enumerate(df.groupby(by='time')):
            trace_density = go.Densitymapbox(lon=df_time.lon, lat=df_time.lat, z=df_time[kw],
                                             customdata=np.stack((df_time.geoName, df_time.geoCode), axis=-1),
                                             meta=[kw, time], visible=True, opacity=0.5,
                                             radius=list(MinMaxScaler(df_time[kw], 1, 60).fillna(1)),
                                             hovertemplate='%{customdata[0]} %{customdata[1]}<br>'
                                                           'time:%{meta[1]}<br>'
                                                           'lat: %{lat:.2f},lon:%{lon:.2f}<br>'
                                                           '%{meta[0]}:%{z}',
                                             colorbar=dict(title={"text": kw}), zmin=0,
                                             zmax=df_time[kw].quantile(0.95), colorscale=color_map)
            if i == 0:
                trace_density.update(name="{kw}-trace".format(kw=kw))
                traces.append(trace_density)
            frames.append(go.Frame(data=trace_density, name="({kw})-({time})".format(kw=kw, time=time), group=kw))
    # mapbox使用Bing map
    layout = go.Layout(mapbox=dict(style="white-bg",
                                   layers=[
                                       dict(
                                           below="traces",
                                           sourcetype="raster",
                                           sourceattribution="Bing Map",
                                           source=source
                                       )
                                   ]
                                   ),
                       margin=dict(l=0, r=0, b=0, t=0), title=title)
    fig = go.Figure(data=traces, layout=layout, frames=frames)
    return fig
