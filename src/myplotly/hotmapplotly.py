import pandas as pd
import plotly.express as px
import requests

bing_map_token = 'AlokyiLvd54vljDRnjUfkF_STJ2nGNZ9N1j_FAFtAMERXrTc57hJdKRyq6yc2EDk'
req = requests.get('https://dev.virtualearth.net/REST/V1/Imagery/Metadata/CanvasLight?output=json&include'
                   '=ImageryProviders&key={BingMapsKey}'.format(BingMapsKey=bing_map_token))
url_json = req.json()['resourceSets'][0]['resources'][0]
source = [url_json['imageUrl'].replace('{subdomain}', sub) for sub in
          url_json['imageUrlSubdomains']]


def hotmapbyword(df: pd.DataFrame, title):
    # radius 影响半经
    fig = px.density_mapbox(df, lat='lat', lon='lon', z='HeatValue', hover_name='geoName',
                            center={'lat': 43, 'lon': 12}, zoom=1, animation_frame='time',
                            animation_group='geoName', radius=30, title=title)
    fig.update_layout(mapbox=dict(style="white-bg",
                                  layers=[
                                      dict(
                                          below="traces",
                                          sourcetype="raster",
                                          sourceattribution="Bing Map",
                                          source=source
                                      )
                                  ]
                                  ))

    return fig
