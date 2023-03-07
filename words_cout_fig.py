import pandas as pd
from plotly import express as px


def words_count_fig(path, param):
    df = pd.read_json(path.format(param['word'], param['f']))
    fig = px.bar(df)
    fig.show()


if __name__ == '__main__':
    param = {
        'word': 'new',
        'f': 'live'
    }
    words_count_fig('.\\words_count-{}-{}.json', param)
