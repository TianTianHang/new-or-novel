from typing import TypeVar, Generic, Union

from pydantic import BaseModel
from pydantic.generics import GenericModel
from starlette.responses import JSONResponse


class RoleBase(BaseModel):
    role_name: str


class UserBase(BaseModel):
    email: str = None
    username: str


class WordBase(BaseModel):
    word_category: str
    word_text: str


class GoogleTrendsRequestWithList(BaseModel):
    q: list[str]
    date: str
    cat: int = 0
    geo: str = ''
    gprop: str = ''


class GoogleTrendsRequest(BaseModel):
    q: str
    date: str
    cat: int = 0
    geo: str = ''
    gprop: str = ''


class GoogleTrendsRequestRegion(GoogleTrendsRequestWithList):
    resolution: str = 'COUNTRY'


class UserCreate(UserBase):
    password: str


class RoleCreate(RoleBase):
    pass


class WordCreate(WordBase):
    pass


class UserRole(RoleBase):
    id: int

    class Config:
        orm_mode = True


class RoleUser(UserBase):
    id: int

    class Config:
        orm_mode = True


class User(UserBase):
    id: int
    roles: list["UserRole"] = []

    class Config:
        orm_mode = True


class UserInDB(User):
    hashed_password: str


class LoginModel(BaseModel):
    username: str = None
    password: str = None


class UserInfo(UserBase):
    roles: list[str]


class Role(RoleBase):
    id: int
    users: list["RoleUser"] = []

    class Config:
        orm_mode = True


class Word(WordBase):
    id: int
    word_details: str

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


T = TypeVar('T')  # 泛型类型 T


class RestfulModel(GenericModel, Generic[T]):
    code: int
    message: str
    data: T

    @staticmethod
    def success(data: T, message: str = "success"):
        return RestfulModel(code=200, message=message, data=data)

    @staticmethod
    def exception(code: int, message: Union[str, dict], data: T = None):
        return JSONResponse(status_code=code,
                            content={"code": code,
                                     "message": message,
                                     "data": data})
