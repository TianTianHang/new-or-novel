import json
from typing import Union

import pandas as pd
from fastapi import APIRouter, Depends, status
from pytrends.request import TrendReq

from main.dependencies import get_trends, get_countries
from main.schemas import RestfulModel, GoogleTrendsRequestRegion, GoogleTrendsRequestWithList, \
    GoogleTrendsRequestWithList, GoogleTrendsRequest

router = APIRouter(prefix="/api/v1/trends", tags=["Google Trends API"])


@router.get('/suggestions', response_model=RestfulModel[dict])
async def suggestions(q: str, pytrends: TrendReq = Depends(get_trends)):
    data: pd.DataFrame = pytrends.suggestions(q)
    return RestfulModel.success(data)


@router.get('/categories', response_model=RestfulModel[list[dict]])
async def categories(pytrends: TrendReq = Depends(get_trends)):
    data = pytrends.categories()

    return RestfulModel.success([data])


@router.post('/region', response_model=RestfulModel[list[dict]])
async def region(request: GoogleTrendsRequestRegion,
                 pytrends: TrendReq = Depends(get_trends), location: pd.DataFrame = Depends(get_countries)):
    pytrends.build_payload(request.q, cat=request.cat, timeframe=request.date, geo=request.geo, gprop=request.gprop)
    data = pytrends.interest_by_region(resolution=request.resolution, inc_low_vol=True, inc_geo_code=True)
    data.reset_index(names=['geoName'], inplace=True)
    data = data.merge(location)
    return RestfulModel.success(json.loads(data.to_json(orient="records")))


@router.post('/overTime', response_model=RestfulModel[list[dict]])
async def overTime(request: GoogleTrendsRequestWithList,
                   pytrends: TrendReq = Depends(get_trends)):
    pytrends.build_payload(request.q, cat=request.cat, timeframe=request.date, geo=request.geo, gprop=request.gprop)
    data = pytrends.interest_over_time()
    data.reset_index(names=['time'], inplace=True)
    data['time'] = data['time'].apply(lambda e: str(e))
    return RestfulModel.success(json.loads(data.to_json(orient="records")))


@router.post('/topics', response_model=RestfulModel[dict])
async def topics(request: GoogleTrendsRequest,
                 pytrends: TrendReq = Depends(get_trends)):
    pytrends.build_payload([request.q], cat=request.cat, timeframe=request.date, geo=request.geo, gprop=request.gprop)
    data = pytrends.related_topics()
    data = {key: json.loads(value.to_json(orient="records")) for key, value in
            data[request.q].items() if value is not None}
    return RestfulModel.success(data)


@router.post('/queries', response_model=RestfulModel[dict])
async def queries(request: GoogleTrendsRequest,
                  pytrends: TrendReq = Depends(get_trends)):
    pytrends.build_payload([request.q], cat=request.cat, timeframe=request.date, geo=request.geo, gprop=request.gprop)
    data = pytrends.related_queries()

    data = {key: json.loads(value.to_json(orient="records")) for key, value in
            data[request.q].items() if value is not None}
    return RestfulModel.success(data)

