import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import text

engine = create_engine(
    'mysql+pymysql://{}:{}@{}:{}/{}'.format('root', '19771201qwer', 'localhost', '3306', 'new or novel'))


def saveregion(df: pd.DataFrame):
    df[['geoCode', 'geoName', 'time', 'word', 'HeatValue']].to_sql('byregion', engine, if_exists='append', index=False)


def readregion(word, time):
    sql_query = "SELECT geoCode,geoName,time,HeatValue '{}' " \
                "FROM byregion WHERE word='{}' AND time='{}'".format(word, word, time)
    df = pd.read_sql(text(sql_query), engine.connect())
    return df


def saveovertime(df: pd.DataFrame):
    df[['time', 'word', 'HeatValue']].to_sql('byovertime', engine, if_exists='append', index=False)


def readovertime(word):
    sql_query = "SELECT time,HeatValue '{}' FROM byovertime WHERE word='{}'".format(word, word)
    df = pd.read_sql(text(sql_query), engine.connect())
    return df
