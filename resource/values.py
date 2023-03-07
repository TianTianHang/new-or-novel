import pandas as pd

loc_df = pd.read_csv('..\\resource\\geoLocation.csv', sep='\t')
loc_columns = loc_df.columns.tolist()
