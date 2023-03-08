import pandas as pd
from sqlalchemy import create_engine

engine = create_engine(
    'mysql+pymysql://{}:{}@{}:{}/{}'.format('root', '19771201qwer', 'localhost', '3306', 'new or novel'))


def saveregion(df: pd.DataFrame):
    word = df.columns[1]
    df['word'] = word
    df.rename(columns={word: 'HeatValue'}, inplace=True)
    df[['geoCode', 'geoName', 'time', 'word', 'HeatValue']].to_sql('byregion', engine, if_exists='append', index=False)


def saveovertime(df: pd.DataFrame):
    word = df.columns[1]
    df['word'] = word
    df.rename(columns={word: 'HeatValue'}, inplace=True)
    df[['time', 'word', 'HeatValue']].to_sql('byovertime', engine, if_exists='append', index=False)
