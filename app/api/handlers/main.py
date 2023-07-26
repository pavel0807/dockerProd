import uuid

from fastapi import Request, UploadFile
from fastapi import Depends
from fastapi.responses import StreamingResponse
from fastapi import HTTPException, Form
from fastapi.responses import HTMLResponse

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from api.actions.auth import enter_or_not,get_current_user_from_token
from api.actions.film import _create_new_film,_get_film_by_uuid,_get_15_new_film
from api.actions.additional import _get_best_view,_get_notification_for_user
from api.actions.user import _get_status_user
from fastapi import Response
from fastapi.responses import RedirectResponse
from starlette.exceptions import HTTPException as StarletteHTTPException


from api.schemas import  FilmCreate


from api.actions.film import _get_film_by_type

from db.session import get_db


import shutil
from fastapi import APIRouter
from fastapi.templating import Jinja2Templates

main_router = APIRouter()

templates = Jinja2Templates(directory="public")
#########################
#         Main          #
#########################

@main_router.get("/")
async def get_main_page(request: Request,db: AsyncSession = Depends(get_db)):

    withSize = request
    dictStatus = {"is_log": False, "is_author": False, "notification": list()}
    if request.cookies.get('auth'):
        jwt = request.cookies.get('auth')
        try:
            user = await get_current_user_from_token(jwt,db)
            if user is not None:
                user_status = await _get_status_user(user.user_id,db)
                user_notification = await _get_notification_for_user(user.user_id,db)
                dictStatus = {"is_log":True, "is_author":user_status,"notification":user_notification}
        except:
            dictStatus = {"is_log":False,"is_author":False,"notification": list()}
            pass

    #get 15 the best count and 15 the new film
    new_film = await _get_15_new_film(db)
    best_film = await _get_best_view(db)

    a = 1
    #best_film = _get_best_view(db)
    return templates.TemplateResponse("main_page.html", {"request": request,"dictStatus":dictStatus,"new_film":new_film,"best_film":best_film})


@main_router.get("/p/")
async def get_main_page(request: Request,db: AsyncSession = Depends(get_db)):
    dictStatus = {"is_log": False, "is_author": False, "notification": list()}
    if request.cookies.get('auth'):
        jwt = request.cookies.get('auth')
        try:
            user = await get_current_user_from_token(jwt,db)
            if user is not None:
                user_status = await _get_status_user(user.user_id,db)
                user_notification = await _get_notification_for_user(user.user_id,db)
                dictStatus = {"is_log":True, "is_author":user_status,"notification":user_notification}
        except:
            dictStatus = {"is_log":False,"is_author":False,"notification": list()}
            pass

    #get 15 the best count and 15 the new film
    new_film = await _get_15_new_film(db)
    best_film = await _get_best_view(db)

    a = 1
    #best_film = _get_best_view(db)
    return templates.TemplateResponse("main_page_mobile.html", {"request": request,"dictStatus":dictStatus,"new_film":new_film,"best_film":best_film})

@main_router.get("/{type_film}")
async def get_one_of_type(type_film: str, request: Request, db: AsyncSession = Depends(get_db)):
    dictStatus = {"is_log": False, "is_author": False, "notification": list()}
    if request.cookies.get('auth'):
        jwt = request.cookies.get('auth')
        try:
            user = await get_current_user_from_token(jwt, db)
            if user is not None:
                user_status = await _get_status_user(user.user_id, db)
                user_notification = await _get_notification_for_user(user.user_id, db)
                dictStatus = {"is_log": True, "is_author": user_status, "notification": user_notification}
        except:
            dictStatus = {"is_log": False, "is_author": False, "notification": list()}
            pass


    list_type_of_film = ["COMEDY","DRAMA","FANTASY","HORROR","TRILLER","STUDY","MELODRAMMA","MULT","WEB","DOC"]
    if type_film not in list_type_of_film:
        return get_main_page(request=request)
    needed_film = await _get_film_by_type(type_film,db)
    listFilm = []
    for film in needed_film:
        listFilm.append((film[0]))
    return templates.TemplateResponse("film/showOneType.html",{"request": request,"dictStatus":dictStatus,"type":type_film,"filmArray":listFilm})





@main_router.get("/{type_film}/p")
async def get_one_of_type(type_film: str, request: Request, db: AsyncSession = Depends(get_db)):
    dictStatus = {"is_log": False, "is_author": False, "notification": list()}
    if request.cookies.get('auth'):
        jwt = request.cookies.get('auth')
        try:
            user = await get_current_user_from_token(jwt, db)
            if user is not None:
                user_status = await _get_status_user(user.user_id, db)
                user_notification = await _get_notification_for_user(user.user_id, db)
                dictStatus = {"is_log": True, "is_author": user_status, "notification": user_notification}
        except:
            dictStatus = {"is_log": False, "is_author": False, "notification": list()}
            pass


    list_type_of_film = ["COMEDY","DRAMA","FANTASY","HORROR","TRILLER","STUDY","MELODRAMMA","MULT","WEB","DOC"]
    if type_film not in list_type_of_film:
        return get_main_page(request=request)
    needed_film = await _get_film_by_type(type_film,db)
    listFilm = []
    for film in needed_film:
        listFilm.append((film[0]))
    return templates.TemplateResponse("film/showOneType_mobile.html",{"request": request,"dictStatus":dictStatus,"type":type_film,"filmArray":listFilm})


@main_router.get("/doc")
async def get_doc():
    headers = {'Content-Disposition': 'inline; filename="sample.pdf"',"content-type": "application/octet-stream"}
    return StreamingResponse("doc/license.docx",media_type='application/pdf',headers=headers)
