import pandas as pd


def format_response(data, code=200, message=''):
    return {'code': code,
            'data': data,
            'message': message}, code


def dataframe2json(df: pd.DataFrame):
    # Convert the DataFrame to a dictionary
    data_dict = df.to_dict(orient='records')

    # Get the keys (column names) of the DataFrame
    keys = list(df.columns)
    return {
        "data": data_dict,
        "keys": keys
    }
