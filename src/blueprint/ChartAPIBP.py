from flask import Blueprint

from blueprint.apiclass import ChartAPI
from googleTrends.services import getDataByRegionAndOvertime, getDataOvertimeMultiWord
from myplotly import density_mapbyword, linechart


def heatmap_data_func(kw_list, timeframe_list):
    df = getDataByRegionAndOvertime(kw_list, timeframe_list)
    df['HeatValue'] = df.iloc[..., 5:].sum(axis=1)
    return df


def line_chart_data_func(kw_list, timeframe_list):
    df = getDataOvertimeMultiWord(kw_list, timeframe_list)
    df['HeatValue'] = df.iloc[..., 2:].sum(axis=1)
    return df


heatmap_bp = Blueprint('heatmap', __name__)
heatmap_view = ChartAPI.as_view('kwlist', chart_func=density_mapbyword, data_func=heatmap_data_func)

line_chart_bp = Blueprint('line_chart', __name__)
line_chart_view = ChartAPI.as_view('kwlist', chart_func=linechart, data_func=line_chart_data_func)


heatmap_bp.add_url_rule('/api/chart/heatmap', view_func=heatmap_view, methods=['POST'])
line_chart_bp.add_url_rule('/api/chart/linechart', view_func=line_chart_view, methods=['POST'])

