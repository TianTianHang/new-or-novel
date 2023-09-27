# @FileName: extendsions
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# 扩展类实例化
api = Api(prefix='/api/v1/')
cors = CORS()
jwt = JWTManager()



