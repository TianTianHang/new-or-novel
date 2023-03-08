import re

import pandas as pd


def data_process(path, canshu):
    df = pd.read_json(path.format(canshu['word'], canshu['f']))
    pattern = re.compile('{} \S*'.format(canshu['word']))
    df = df.applymap(lambda s: re.findall(pattern, s), )
    df = df[~df.text.isin([[]])]
    df = df.applymap(lambda e: [t.split(' ')[1] for t in e])
    wordlist = []
    for words in df['text']:
        wordlist.extend(words)
    newdf = pd.DataFrame(data=wordlist, columns=['word'])
    newdf['word'] = newdf.applymap(lambda e: re.sub('[^A-Za-z]+', '', e))
    newdf = newdf[~newdf.isin([''])]
    newdf['word'] = newdf['word'].str.lower()
    vcounts=newdf['word'].value_counts()
    pd.DataFrame(vcounts, columns=['word']).to_json('.\\words_count-{}-{}.json'.format(canshu['word'], canshu['f']))


if __name__ == '__main__':
    canshu = {
        'word': 'new',
        'f': 'live'
    }
    data_process('.\\twitter-{}-{}.json', canshu)

