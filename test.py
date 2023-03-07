from googleTrends.API import GoogleTrendsAPI

if __name__ == '__main__':
    df = GoogleTrendsAPI.getdataovertime("novel idea", "today 5-y")
    print(df)
