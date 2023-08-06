import pandas as pd
import requests
from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse
from pytrends.request import TrendReq
from requests import ConnectTimeout

import app

parser = reqparse.RequestParser()
parser.add_argument('keyword', type=str, required=True, help='keyword cannot be empty')
parser.add_argument('timeframe', type=str, required=True, help='timeframe cannot be empty')
parser.add_argument('cat', type=int, default=0)
parser.add_argument('geo', type=str, default='')
parser.add_argument('gprop', type=str, default='')
region_parser = parser.copy()
region_parser.add_argument('resolution', type=str, default='COUNTRY')

suggest_parser = reqparse.RequestParser()
suggest_parser.add_argument('keyword', type=str, required=True, help='keyword cannot be empty')


def jsonify_dataframe(f):
    def wrapper(*args, **kwargs):
        # Call the wrapped function to get the pandas DataFrame
        result = f(*args, **kwargs)

        # Check if the result is a pandas DataFrame
        if not isinstance(result, pd.DataFrame):
            return result

        # Convert the DataFrame to a dictionary
        data_dict = result.to_dict(orient='records')

        # Get the keys (column names) of the DataFrame
        keys = list(result.columns)

        # Return the data and keys as a JSON response
        response = {'code': 200,
                    'data': {
                        "data": data_dict,
                        "keys": keys
                    }, 'message': ''}

        return response

    return wrapper


class BingMapResource(Resource):
    def get(self):
        bing_map_token = app.app.config['BING_MAP_TOKEN']
        req = requests.get('https://dev.virtualearth.net/REST/V1/Imagery/Metadata/CanvasLight?output=json&include'
                           '=ImageryProviders&uriScheme=https&key={BingMapsKey}'.format(BingMapsKey=bing_map_token))
        if req.ok:
            url_json = req.json()['resourceSets'][0]['resources'][0]
            sources = [url_json['imageUrl'].replace('{subdomain}', sub) for sub in
                       url_json['imageUrlSubdomains']]
            return {'code': 200, 'data': sources, 'message': 'get bing_map_api success'}
        else:
            return {'code': req.status_code, 'data': None, 'message': req.reason}


class TrendsRestful(Resource):
    def __init__(self):
        try:
            self.pytrends = TrendReq(hl='en-US', tz=360, timeout=(10, 25), retries=2,
                                     backoff_factor=0.1, requests_args={'headers': {}})
        except ConnectTimeout as e:
            raise e

    @jwt_required()
    @jsonify_dataframe
    def post(self, query_type):
        if 'region' == query_type:
            args = region_parser.parse_args(strict=True)
            data = self.get_interest_by_region(**args)
            # data = pd.read_csv('resource/data/geo_country_with_location.csv', index_col=1)
            data.reset_index(names=['geoName'], inplace=True)
            return data
        if 'overTime' == query_type:
            args = parser.parse_args(strict=True)
            data = self.get_interest_over_time(**args)
            data.reset_index(names=['time'], inplace=True)
            data['time'] = data['time'].apply(lambda e: str(e))
            return data
        if 'topics' == query_type:
            args = parser.parse_args(strict=True)
            data = self.get_related_topics(**args)
            return data
        if 'queries' == query_type:
            args = parser.parse_args(strict=True)
            data = self.get_related_queries(**args)
            return data

    @jwt_required()
    def get(self, query_type):
        if 'suggestions' == query_type:
            args = suggest_parser.parse_args(strict=True)
            keyword = args['keyword']
            data = self.suggestions(keyword)
            return {'code': 200,
                    'data': data,
                    'message': ''}
        if 'categories' == query_type:
            data = self.categories()
            categories = [{'name': data['name'], 'id': data['id']}]
            categories.extend(data['children'])
            return {'code': 200,
                    'data': categories,
                    'message': ''}

    def get_interest_over_time(self, keyword, cat=0, timeframe='today 5-y', geo='', gprop='', ):
        self.pytrends.build_payload([keyword], cat=cat, timeframe=timeframe, geo=geo, gprop=gprop)
        data = self.pytrends.interest_over_time()
        return data

    def get_interest_by_region(self, keyword, cat=0, timeframe='today 5-y', geo='', gprop='', resolution='COUNTRY'):
        self.pytrends.build_payload([keyword], cat=cat, timeframe=timeframe, geo=geo, gprop=gprop)
        data = self.pytrends.interest_by_region(resolution=resolution, inc_low_vol=True, inc_geo_code=True)
        return data

    def get_related_topics(self, keyword, cat=0, timeframe='today 5-y', geo='', gprop='', ):
        self.pytrends.build_payload([keyword], cat=cat, timeframe=timeframe, geo=geo, gprop=gprop)
        data = self.pytrends.related_topics()

        return data

    def get_related_queries(self, keyword, cat=0, timeframe='today 5-y', geo='', gprop='', ):
        self.pytrends.build_payload([keyword], cat=cat, timeframe=timeframe, geo=geo, gprop=gprop)
        data = self.pytrends.related_queries()
        return data

    def suggestions(self, keyword):
        data = self.pytrends.suggestions(keyword)
        return data

    def categories(self):
        return self.pytrends.categories()
