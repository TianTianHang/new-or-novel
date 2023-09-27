from fastapi import FastAPI
from pydantic.tools import lru_cache

from main import settings
from main.databaseresource.user import UserResource, UserMethods
from main.databaseresource.word import WordResource, WordListResource
from main.google_trends import TrendsRestful
from main.google_trends.TrendsRestful import BingMapResource


def create_app():
    app = FastAPI()

    @lru_cache()
    def get_settings():
        return settings.DevelopmentConfig()
    cors.init_app(app, max_age=6000)
    jwt.init_app(app)
    api.add_resource(TrendsRestful, '/trends/<query_type>')
    api.add_resource(UserResource, '/users', '/users/<int:user_id>')
    api.add_resource(UserMethods, '/users/<method>')
    api.add_resource(WordResource, '/word', '/word/<word_id_or_text>')
    api.add_resource(WordListResource, '/word-list', '/word-list/<category>')
    api.add_resource(BingMapResource, '/bingMap')
    api.init_app(app)

    return app
