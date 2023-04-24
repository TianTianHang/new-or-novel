import geopandas as gpd
import pandas as pd

if __name__ == '__main__':
    Table = gpd.read_file('ne_10m_admin_0_countries.dbf')
    df = pd.DataFrame(Table)
    df = df[['ISO_A2', 'LABEL_X', 'LABEL_Y']]
    df.to_csv('geoLocation.csv', sep='\t', index=False)
