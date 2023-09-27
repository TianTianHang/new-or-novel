from functools import lru_cache

from pydantic import BaseSettings


# @FileName: settings
class BaseConfig(BaseSettings):
    # 基础配置
    APP_NAME: str = "new_or_novel"
    DATABASE_URI: str
    SECRET_KEY: str


class DevelopmentConfig(BaseConfig):
    # 开发环境配置
    BING_MAP_TOKEN: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    ALGORITHM: str


class TestConfig(BaseConfig):
    BING_MAP_TOKEN: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    ALGORITHM: str
    # 测试环境配置
    pass


class ProductionConfig(BaseConfig):
    # 生产环境(上线环境)配置
    pass


@lru_cache()
def get_settings():
    return DevelopmentConfig()
