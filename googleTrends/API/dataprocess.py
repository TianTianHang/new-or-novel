import pandas as pd


def addgeo(df: pd.DataFrame):
    geodf = pd.read_csv('.\\geoLocation.csv', sep='\t')
    df.join(geodf, on='geoName')
    return df.dropna()
