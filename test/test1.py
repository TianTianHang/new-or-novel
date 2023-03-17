import googleTrends
import database
import myplotly
import resource

if __name__ == '__main__':
    df1 = googleTrends.getdatabyovertime(['novel idea'], '2022-01-01 2022-12-31')
    df2 = googleTrends.getdatabyovertime(['new idea'], '2022-01-01 2022-12-31')
    df = df1.append(df2)
    fig = myplotly.linechart(df, 'novel idea vs new idea')
