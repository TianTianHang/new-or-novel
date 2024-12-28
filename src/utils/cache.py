from functools import wraps
import json
from datetime import datetime, timedelta

import pandas as pd

from models import Cache
from extendsions import db

class CacheResult:
    def __init__(self, db):
        """初始化时传入数据库连接对象"""
        self.db = db  # 存储数据库连接对象
        self.session = db.session  # 获取数据库会话

    def __call__(self, func):
        """实际的装饰器实现"""
        @wraps(func)
        def wrapper(*args, **kwargs):

            # 将参数序列化为 JSON 字符串
            params = json.dumps((args[1:], kwargs), default=str)
            func_name = func.__name__

            try:
                # 查询缓存：检查缓存是否已经存在且未过期
                cached = self.session.query(Cache).filter(
                    Cache.func_name == func_name,
                    Cache.params == params,
                ).first()

                if cached:
                    # 如果缓存存在并且未过期，返回缓存的结果
                    print(f"Cache hit for {func_name} with params {params}")
                    return pd.read_json(cached.result)
                else:
                    # 如果缓存不存在，调用函数并存储结果
                    print(f"Cache miss for {func_name} with params {params}")
                    result = func(*args, **kwargs)

                    # 存储缓存
                    cache_entry = Cache(
                        func_name=func_name,
                        params=params,
                        result=result.to_json(orient='records') if isinstance(result, pd.DataFrame) else json.dumps(result),
                        created_at=datetime.now(),
                    )
                    self.session.add(cache_entry)
                    self.session.commit()

                    return result
            finally:
                self.session.close()

        return wrapper


cache_decorator = CacheResult(db)