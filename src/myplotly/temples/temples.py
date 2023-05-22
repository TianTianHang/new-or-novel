import json
import plotly.io
import plotly.graph_objects as go

from utils.helper import getmapsource

Bing_Map_Template = dict(
    mapbox=dict(style="white-bg",
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
)
# 颜色表
COLOR_MAP = [
    [0.0, "#00FF00"],
    [0.3, '#BDDF31'],
    [0.4, '#FFFF00'],
    [0.6, '#FF6600'],
    [1, "red"]
]
TEMPLATES = go.layout.Template()
with open('src/myplotly/temples/template.json', 'r') as f:
    TEMPLATES.update(json.load(f))


def template_to_json():
    with open('src/myplotly/temples/template.json', 'w') as f:
        f.write(json.dumps(TEMPLATES.to_plotly_json()))


def template_layout():
    return TEMPLATES.layout


def add_template(template, type):
    if type == 'choroplethmapbox' or type == 'densitymapbox' or type == 'scattermapbox':
        TEMPLATES['date'][type].appned(template)
        template_to_json()
    else:
        raise ValueError('the type is one of choroplethmapbox,densitymapbox,scattermapbox')


def get_template(type, index):
    tf = TEMPLATES['data'][type][index]
    tf.update(colorscale=COLOR_MAP)
    return tf


def mapbox_factory(type, index, **kwargs):
    trace = get_template(type, index)
    trace.update(kwargs)
    return trace
