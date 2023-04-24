import pandas as pd
import plotly.express as px


def linechart(df: pd.DataFrame, title):
    fig = px.line(df, x='time', y='value', color='word',title=title)
    return fig
