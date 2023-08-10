

from pytrends.request import TrendReq

if __name__ == '__main__':
    pytrends = TrendReq(hl='en-US', tz=360, timeout=(10, 25), retries=2,
                        backoff_factor=0.1, requests_args={'headers': {}})
    pytrends.build_payload(['new'], cat=0, timeframe='today 5-y', geo='', gprop='', )
    print(pytrends.related_topics())
