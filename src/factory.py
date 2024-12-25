from flask import Flask

import settings
from databaseresource.user import UserResource, UserMethods
from databaseresource.word import WordResource, WordListResource
from extendsions import db, api, cors, jwt
from google_trends import TrendsRestful
from google_trends.TrendsRestful import BingMapResource


def create_app():
    app = Flask(__name__)

    app.config.from_object(settings.DevelopmentConfig)

    db.init_app(app)
    with app.app_context():
        db.create_all()

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
