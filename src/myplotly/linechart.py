import pandas as pd
import plotly.express as px


def linechart(df: pd.DataFrame, title):
    fig = px.line(data_frame=df, x='time', y='HeatValue', color='word',)
    return fig
