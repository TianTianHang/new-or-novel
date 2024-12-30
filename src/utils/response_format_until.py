import pandas as pd


def format_response(data, code=200, message=''):
    return {'code': code,
            'data': dataframe2json(data) if isinstance(data, pd.DataFrame) else data,
            'message': message}, code


def dataframe2json(df: pd.DataFrame):
    # Convert datetime columns to string
    for col in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            df[col] = df[col].dt.strftime('%Y-%m-%d %H:%M:%S')

    # Convert the DataFrame to a dictionary
    data_dict = df.to_dict(orient='records')

    # Get the keys (column names) of the DataFrame
    keys = list(df.columns)
    return {
        "data": data_dict,
        "keys": keys
    }
