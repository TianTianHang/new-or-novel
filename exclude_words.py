import pandas as pd


def main(path, canshu):
    excludelist = pd.read_json('exclude_words.json')
    df = pd.read_json(path.format(canshu['word'], canshu['f']))
    df[~df.index.isin(excludelist['word'].tolist())].sort_values(ascending=False, by='word'). \
        to_json(".//exclude_words-{}-{}.json".format(canshu['word'], canshu['f']))


if __name__ == '__main__':
    canshu = {
        'word': 'new',
        'f': 'live'
    }
    main('.\\words_count-{}-{}.json', canshu)
