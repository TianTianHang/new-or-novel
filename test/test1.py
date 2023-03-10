import googleTrends
import database
import myplotly
import resource

if __name__ == '__main__':
    df1 = googleTrends.getdatabyovertime(['novel idea'], '2004-01-01 2022-12-31')
    df2=googleTrends.getdatabyovertime(['new idea'], '2004-01-01 2022-12-31')
    df= df1.append(df2)
    print(df)
    myplotly.linechart(df, 'test')
