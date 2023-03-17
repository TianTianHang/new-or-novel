import pandas as pd
import plotly.express as px


def hotmapbyword(df: pd.DataFrame, title):
    token = 'pk.eyJ1IjoidGlhbnRpYW4xIiwiYSI6ImNsY3g5eDBsYzA3NWwzb3A5NHpraXp3Y3AifQ.DH84zUyJcvSpZuRhqLTKfw'
    # radius 影响半经
    fig = px.density_mapbox(df, lat='lat', lon='lon', z='HeatValue', hover_name='geoName',
                            center={'lat': 43, 'lon': 12}, zoom=1, animation_frame='time',
                            animation_group='geoName', radius=30)
    fig.update_layout(mapbox_accesstoken=token)
    fig.update_layout(title=title)
    return fig
