import time

import myplotly

if __name__ == '__main__':
    pytrends = TrendReq(hl='en-US', tz=360, timeout=(10, 25), retries=2,
                        backoff_factor=0.1, requests_args={'headers': {}})
    print(pytrends.categories())
