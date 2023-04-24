import time

from googleTrends.services import *
import database
import myplotly

if __name__ == '__main__':
    df = getDataByRegionAndOvertimeGevent(['apple', 'iphone'], ['2004-01-01 2005-01-01', '2005-01-01 2006-01-01'])
    start1 = time.time()
    myplotly.hotmapbyword(df, 'test')
    print(time.time() - start1)
