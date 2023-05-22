from flask.views import MethodView
from marshmallow import Schema, fields, validates_schema, ValidationError
from flask import request


class OptionSchema(Schema):
    timeframe_list = fields.List(fields.List(fields.Str()))
    kw_list = fields.List(fields.Str())
    title = fields.Str(empyt=True)

    @validates_schema
    def validate_lists(self, data, **kwargs):
        """验证 timeframe_list 和 kw_list 字段都不为空"""
        if 'timeframe_list' in data and not data['timeframe_list']:
            raise ValidationError('timeframe_list cannot be empty!')
        if 'kw_list' in data and not data['kw_list']:
            raise ValidationError('kw_list cannot be empty!')


class ChartAPI(MethodView):
    def __init__(self, chart_func, data_func):
        self.chart_func = chart_func
        self.data_func = data_func

    def post(self):
        result = self.valid_message(request)
        if result[0]:
            kw_list, timeframe_list, title = result[1:]
            df = self.data_func(kw_list, timeframe_list)
            fig = self.chart_func(df, title, 0)
            return fig.to_json()
        else:
            return result[1:]

    def valid_message(self, request):
        schema = OptionSchema()
        form = request.get_json()
        result = schema.validate(form)
        if result:
            return False, result, 400
        else:
            timeframe_list = form['timeframe_list']
            kw_list = form['kw_list']
            title = form['title']
            timeframe_list_c = list(map(lambda e: ' '.join(e), timeframe_list))
        return True, kw_list, timeframe_list_c, title
