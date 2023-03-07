import googleTrends

if __name__ == '__main__':
    df = googleTrends.services.getdatabyregion_overtime(['novel idea', 'novel method'], ['2004-01-01 2004-12-31',
                                                                                         '2005-01-01 2005-12-31'])
    print(df)
