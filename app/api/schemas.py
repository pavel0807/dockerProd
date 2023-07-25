import re
import uuid

from datetime import date, datetime, time, timedelta
from fastapi import HTTPException, UploadFile
from pydantic import BaseModel, EmailStr, validator, DateNotInTheFutureError

class TunedModel(BaseModel):
    class Config:
        orm_mode = True


###########################
# BLOCK WITH USERE MODELS #
###########################
LETTEER_MATCH_PATTERN_NAME_SURNAME = re.compile(r"^[а-яА-Я\-]+$")
LETTEER_MATCH_PATTERN_NAME_LOGIN = re.compile(r"^[a-zA-Z0-9\-]+$")
LETTEER_MATCH_PATTERN_NAME_MAIL = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')


class ShowUser(TunedModel):
    user_id: uuid.UUID
    name: str
    surname: str
    login: str
    email: EmailStr
    password:str
    dataBirthday: date
    is_author: bool
    path_to_image:str

class ActiveEmail(BaseModel):
    id: uuid.UUID


class UserLogin(BaseModel):
    login: str
    password: str


class UserCreate(BaseModel):
    name: str
    surname: str
    login: str
    email: EmailStr
    password:str
    dataBirthday: date
    is_author: bool
    path_to_image: str

    @validator("name")
    def validate_name(cls, value):
        if not LETTEER_MATCH_PATTERN_NAME_SURNAME.match(value):
            raise HTTPException(status_code=422,detail="Name should contains only letters")
        return value

    @validator("surname")
    def validate_surname(cls, value):
        if not LETTEER_MATCH_PATTERN_NAME_SURNAME.match(value):
            raise HTTPException(status_code=422,detail="Surname should contains only letters")
        return value

    @validator("login")
    def validate_login(cls, value):
        if not LETTEER_MATCH_PATTERN_NAME_LOGIN.match(value):
            raise HTTPException(status_code=422,detail="Login should contains only letters")
        return value




###########################
# BLOCK WITH FILM MODELS #
###########################
LETTEER_MATCH_PATTERN_NAME_FILM = re.compile(r"^[а-яА-Яa-zA-Z0-9\-]+$")

class ShowFilm(TunedModel):
    film_id: uuid.UUID
    name: str
    description: str
    url: str
    rating: float
    type_of_film: str
    age_restriction: str
    data_create: date
    data_add: date

class Film(BaseModel):
    images: UploadFile
    name: str

class FilmCreate():
    def __init__(self,uuid,name,description,url,rating,type_of_film,age_restriction,data_create,data_add):
        self.uuid = uuid
        self.name = name
        self.description = description
        self.url=url
        self.rating = rating
        self.type_of_film = type_of_film
        self.age_restriction = age_restriction
        self.data_create = data_create
        self.data_add = data_add
    uuid: uuid.UUID
    name: str
    description: str
    url: str
    rating: str
    type_of_film:str
    age_restriction: str
    data_create: str
    data_add: str

class Token(BaseModel):
    access_token: str
    token_type: str


class AuthorCreateDirector(BaseModel):
    user_id : uuid.UUID
    film_id : uuid.UUID
    type = "DIRECTOR"


class News_AD(BaseModel):
    news_id: uuid.UUID
    title : str
    description: str
    news_or_ad : bool