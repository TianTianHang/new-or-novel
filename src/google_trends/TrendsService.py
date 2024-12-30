from utils.cache import cache_decorator

class TrendsService:
    def __init__(self, pytrends):
        self.pytrends = pytrends

    @cache_decorator
    def get_interest_over_time(self, keyword, cat=0, timeframe='today 5-y', geo='', gprop=''):
        data = self.pytrends.interest_over_time([keyword], cat=cat, timeframe=timeframe, geo=geo, gprop=gprop)
        return data

    @cache_decorator
    def get_interest_by_region(self, keyword, cat=0, timeframe='today 5-y', geo='', gprop='', resolution='COUNTRY'):
        data = self.pytrends.interest_by_region([keyword], cat=cat, timeframe=timeframe, geo=geo, gprop=gprop, resolution=resolution, inc_low_vol=True)
        return data

    @cache_decorator
    def get_related_topics(self, keyword, cat=0, timeframe='today 5-y', geo='', gprop=''):
        data = self.pytrends.related_topics([keyword], cat=cat, timeframe=timeframe, geo=geo, gprop=gprop)
        return data

    @cache_decorator
    def get_related_queries(self, keyword, cat=0, timeframe='today 5-y', geo='', gprop=''):
        data = self.pytrends.related_queries([keyword], cat=cat, timeframe=timeframe, geo=geo, gprop=gprop)
        return data

    @cache_decorator
    def suggestions(self, keyword):
        data = self.pytrends.suggestions(keyword)
        return data

    @cache_decorator
    def categories(self):
        return self.pytrends.categories()
