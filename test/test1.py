import googleTrends
import myplotly

if __name__ == '__main__':
    df = googleTrends.services.getdatabyregion_overtime(['novel idea', 'novel method'],
                                                        ['2004-01-01 2004-02-01', '2005-01-01 2005-12-31'])
    myplotly.hotmapbyword(df, 'test', 'mid')
