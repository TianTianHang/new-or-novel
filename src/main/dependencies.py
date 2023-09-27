# Dependency
from functools import lru_cache

import pandas as pd

from pytrends.request import TrendReq

from .database import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@lru_cache()
def get_countries():
    return pd.read_csv('resource/data/geo_country_with_location.csv')


def get_trends():
    try:
        pytrends = TrendReq(hl='en-US', tz=360, timeout=(10, 25), retries=2,
                            backoff_factor=0.1, requests_args={'headers': {}})
        yield pytrends
    except ConnectionError as e:
        raise e
