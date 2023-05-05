import numpy as np
import pandas as pd
import plotly.graph_objects as go


def linechart(df: pd.DataFrame, title):
    frames = []

    for i, (timeframe, df_time) in enumerate(df.groupby(by='timeframe')):
        all_trace = []
        for index, kw in enumerate(df.columns[2:]):
            trace = go.Scatter(x=df_time.time, y=df_time[kw],name=kw,
                               meta=[kw, timeframe], visible=True,
                               hovertemplate='timeframe:%{meta[1]}<br>'
                                             '%{meta[0]}:%{y}<br>'
                                             'time:%{x}',
                               )
            all_trace.append(trace)
            frames.append(go.Frame(data=trace, name="{kw}-{time}".format(kw=kw, time=timeframe), group=kw))
        frames.append(go.Frame(data=all_trace, name="all-{time}".format(time=timeframe), group='all'))
    layout = go.Layout(margin=dict(l=0, r=0, b=0, t=0), title=title)
    fig = go.Figure(data=[], layout=layout, frames=frames)
    return fig
