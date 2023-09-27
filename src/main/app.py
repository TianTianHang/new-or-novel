import traceback

import requests
from fastapi import FastAPI, Request, HTTPException, status
from fastapi.exceptions import RequestValidationError
from fastapi.logger import logger
from starlette.middleware.cors import CORSMiddleware

from . import models
from .database import engine
from .routers import users, google_trends
from .schemas import RestfulModel
from .settings import get_settings

models.Base.metadata.create_all(bind=engine)
app = FastAPI()
# 允许请求的源
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:3333",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # GET,POST,DELETE,PUT
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(google_trends.router)


@app.exception_handler(Exception)
async def all_exception_handler(request: Request, exc: Exception):
    """
       全局异常
       :param request: 请求头信息
       :param exc: 异常对象
       :return:
       """
    # 日志记录异常详细上下文
    logger.error(f"全局异常\n{request.method}URL{request.url}\nHeaders:{request.headers}\n{traceback.format_exc()}")
    return RestfulModel.exception(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=str(exc))


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    # 日志记录异常详细上下文
    logger.error(f"http异常\n{request.method}URL{request.url}\nHeaders:{request.headers}\n{traceback.format_exc()}")
    return RestfulModel.exception(code=exc.status_code, message={"detail": exc.detail, "headers": exc.headers})


@app.exception_handler(RequestValidationError)
async def request_validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    请求参数验证异常
    :param request: 请求头信息
    :param exc: 异常对象
    :return:
    """
    # 日志记录异常详细上下文
    logger.error(
        f"请求参数验证异常\n{request.method}URL{request.url}\nHeaders:{request.headers}\n{traceback.format_exc()}")
    return RestfulModel.exception(code=status.HTTP_422_UNPROCESSABLE_ENTITY, message=str(exc.errors()))


@app.get('/')
async def index():
    return 'yes'


@app.get('/api/v1/bingMap', response_model=RestfulModel[list[str]])
async def bing_map():
    bing_map_token = get_settings().BING_MAP_TOKEN
    req = requests.get('https://dev.virtualearth.net/REST/V1/Imagery/Metadata/CanvasLight?output=json&include'
                       '=ImageryProviders&uriScheme=https&key={BingMapsKey}'.format(BingMapsKey=bing_map_token))
    if req.ok:
        url_json = req.json()['resourceSets'][0]['resources'][0]
        sources = [url_json['imageUrl'].replace('{subdomain}', sub) for sub in
                   url_json['imageUrlSubdomains']]
        return RestfulModel.success(sources)
    else:
        raise HTTPException(status_code=req.status_code, detail=req.reason, headers=dict(req.headers))
