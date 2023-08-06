# @FileName: extendsions
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

# 扩展类实例化
db = SQLAlchemy()
api = Api(prefix='/api/v1/')
cors = CORS()
jwt = JWTManager()
