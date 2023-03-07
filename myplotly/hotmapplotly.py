import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def hotmapbyall(df: pd.DataFrame, title):
    token = 'pk.eyJ1IjoidGlhbnRpYW4xIiwiYSI6ImNsY3g5eDBsYzA3NWwzb3A5NHpraXp3Y3AifQ.DH84zUyJcvSpZuRhqLTKfw'
    # radius 影响半经
    fig = px.density_mapbox(lat=df['lat'], lon=df['lon'], z=df['mid'], hover_name=df['geoName'],
                            center={'lat': 43, 'lon': 12}, zoom=1, animation_frame=df['time'],
                            animation_group=df['geoName'], radius=30)
    fig.update_layout(mapbox_accesstoken=token)
    fig.update_layout(title=title)
    fig.show()


def hotmapbyword(df: pd.DataFrame, title, word):
    token = 'pk.eyJ1IjoidGlhbnRpYW4xIiwiYSI6ImNsY3g5eDBsYzA3NWwzb3A5NHpraXp3Y3AifQ.DH84zUyJcvSpZuRhqLTKfw'
    # radius 影响半经
    fig = px.density_mapbox(lat=df['lat'], lon=df['lon'], z=df[word], hover_name=df['geoName'],
                            center={'lat': 43, 'lon': 12}, zoom=1, animation_frame=df['time'],
                            animation_group=df['geoName'], radius=30)
    fig.update_layout(mapbox_accesstoken=token)
    fig.update_layout(title=title)
    fig.show()
