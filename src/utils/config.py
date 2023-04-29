import os

SQLALCHEMY_DATABASE_URI = 'sqlite:///../../db/'+os.getenv('DATABASE_FILE', 'flask.db')
SECRET_KEY = os.getenv('SECRET_KEY', 'dev')
MAP_SOURCE = os.getenv('MAP_SOURCE', 'TianTianHang.pythonanywhere.com/map/{quadkey}/')
