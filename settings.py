import os


# @FileName: settings
class BaseConfig(object):
    # 基础配置
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev')


class DevelopmentConfig(BaseConfig):
    # 开发环境配置
    BING_MAP_TOKEN = os.getenv('BING_MAP_TOKEN', None)


class TestConfig(BaseConfig):
    # 测试环境配置
    pass


class ProductionConfig(BaseConfig):
    # 生产环境(上线环境)配置
    pass
