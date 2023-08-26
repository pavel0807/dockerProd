import uvicorn

from fastapi import FastAPI
from fastapi.routing import APIRouter
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import HTTPException

from sqlalchemy import Column, Boolean, String
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.dialects.postgresql import UUID

import settings
import uuid
import re

from api.handlers.user import user_router
from api.handlers.film import film_router
from api.handlers.main import main_router
from api.handlers.news import news_router
from api.handlers.author import author_router
from api.handlers.additional import additional_router
from api.handlers.fest import fest_router
from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import validator

from fastapi.responses import RedirectResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from db.session import get_db
from fastapi import Request
from fastapi import Depends


from sqlalchemy.ext.asyncio import AsyncSession
from api.actions.auth import enter_or_not,get_current_user_from_token
from api.actions.film import _create_new_film,_get_film_by_uuid,_get_15_new_film
from api.actions.additional import _get_best_view,_get_notification_for_user
from api.actions.user import _get_status_user

#########################
# BLOCK WITH api ROUTES #
#########################

app = FastAPI(title="donateat")

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/public", StaticFiles(directory="public"), name="public")
app.mount("/Img", StaticFiles(directory="Img"), name="Img")
main_api_router = APIRouter()


main_api_router.include_router(user_router,prefix="/user",tags=["user"])
main_api_router.include_router(film_router,prefix="/film",tags=["film"])
main_api_router.include_router(main_router,prefix="/main",tags=["main"])
main_api_router.include_router(news_router,prefix="/news",tags=["news"])
main_api_router.include_router(author_router,prefix="/author",tags=["author"])
main_api_router.include_router(additional_router,prefix="/additional",tags=["additional"])
main_api_router.include_router(fest_router,prefix="/fest",tags=["fest"])


app.include_router(main_api_router)

templates = Jinja2Templates(directory="public")

@app.exception_handler(404)
async def get_main_page(request: Request,db: AsyncSession = Depends(get_db)):
    dictStatus = {"is_log": False, "is_author": False, "notification": list()}
    #best_film = _get_best_view(db)
    return templates.TemplateResponse("auth/login.html", {"request": request,"dictStatus":dictStatus})

@app.get("/")
async def get_main_page(request: Request,db: AsyncSession = Depends(get_db)):
     dictStatus = {"is_log": False, "is_author": False, "notification": list()}
     return templates.TemplateResponse("main_page.html", {"request": request,"dictStatus":dictStatus})

@app.exception_handler(500)
async def get_main_page(request: Request,db: AsyncSession = Depends(get_db)):
    dictStatus = {"is_log": False, "is_author": False, "notification": list()}
    #best_film = _get_best_view(db)
    return templates.TemplateResponse("auth/login.html", {"request": request,"dictStatus":dictStatus})



if __name__ == "__main__":
    uvicorn.run(app,host="0.0.0.0",port=80)