import numpy as np
import pandas as pd
import plotly.graph_objects as go

from myplotly.temples.temples import TEMPLATES, base_factory, Bing_Map_Template


def choropleth_mapbyword(df: pd.DataFrame, title):
    frames = []
    for index, kw in enumerate(df.columns[5:]):
        for i, (timeframe, df_time) in enumerate(df.groupby(by='timeframe')):
            trace = base_factory(type='choroplethmapbox', index=0, name='choroplet_bingmap', z=df_time[kw],
                                 locations=df_time.geoName,
                                 customdata=np.stack((df_time.geoName, df_time.geoCode), axis=-1), meta=[kw, timeframe],
                                 colorbar=dict(title={"text": kw}), zmin=0, zmax=df_time[kw].quantile(0.95))

            frames.append(go.Frame(data=trace, name="{kw}-{time}".format(kw=kw, time=timeframe), group=kw))

    # mapbox使用Bing map
    layout = TEMPLATES['layout']
    layout.update(**Bing_Map_Template, title=title)

    fig = go.Figure(data=[], layout=layout, frames=frames)
    return fig
