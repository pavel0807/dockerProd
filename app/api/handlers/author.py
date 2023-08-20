import uuid
import shutil
import os

from fastapi import Request
from fastapi import Depends
from fastapi import  Form

from sqlalchemy.ext.asyncio import AsyncSession
from api.actions.user import _get_user_by_id_for_auth, _set_user_author
from api.actions.autor import _create_new_director_author,_get_id_author_by_film,_get_about_author_by_user_id,_get_author_or_not,_add_about_author_by_user_id,_update_about_author,_get_all_film_by_user_id,_create_new_author
from api.actions.film import _get_film_by_uuid
from db.session import get_db
from api.actions.auth import get_current_user_from_token
from api.actions.user import _get_status_user
from api.actions.additional import _get_notification_for_user


import shutil
from fastapi import APIRouter
from fastapi.templating import Jinja2Templates

author_router = APIRouter()

templates = Jinja2Templates(directory="public")

#AUTHOR#
#добавить роль пользователю#
@author_router.get("/add_role")
async def add_role_get(request: Request,db: AsyncSession = Depends(get_db)):
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
    if request.cookies.get('auth'):
        jwt = request.cookies.get('auth')
        try:
            user = await get_current_user_from_token(jwt,db)
        except:
            return templates.TemplateResponse("auth/login.html", {"request": request,"dictStatus":dictStatus})
        if user is None:
            return templates.TemplateResponse("auth/login.html", {"request": request,"dictStatus":dictStatus})
        else :
            return templates.TemplateResponse("author/addRole.html",{"request": request,"dictStatus":dictStatus})
    else:
        return templates.TemplateResponse("auth/login.html", {"request": request,"dictStatus":dictStatus})

@author_router.get("/p/add_role")
async def add_role_get(request: Request,db: AsyncSession = Depends(get_db)):
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
    if request.cookies.get('auth'):
        jwt = request.cookies.get('auth')
        try:
            user = await get_current_user_from_token(jwt,db)
        except:
            return templates.TemplateResponse("auth/login_mobile.html", {"request": request,"dictStatus":dictStatus})
        if user is None:
            return templates.TemplateResponse("auth/login_mobile.html", {"request": request,"dictStatus":dictStatus})
        else :
            return templates.TemplateResponse("author/addRole_mobile.html",{"request": request,"dictStatus":dictStatus})
    else:
        return templates.TemplateResponse("auth/login_mobile.html", {"request": request,"dictStatus":dictStatus})

@author_router.post("/addRole")
async def add_role_post(request: Request,info = Form(), db: AsyncSession = Depends(get_db)):
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
    if request.cookies.get('auth'):
        jwt = request.cookies.get('auth')
        try:
            user = await get_current_user_from_token(jwt,db)
        except:
            return templates.TemplateResponse("auth/login.html", {"request": request,"dictStatus":dictStatus})
        if user is None:
            return templates.TemplateResponse("auth/login.html", {"request": request,"dictStatus":dictStatus})
        else :
            data = eval(info)
            new_author = await _create_new_author(user.user_id,data['url'],data['type'],db)
            await _set_user_author(user.user_id, db)
            return templates.TemplateResponse("main_page.html", {"request": request,"dictStatus":dictStatus})
    else:
        return templates.TemplateResponse("auth/login.html", {"request": request,"dictStatus":dictStatus})

#показать информацию об авторе#
@author_router.get("/show/{user_id}")
async def get_role(user_id: str, request: Request,db: AsyncSession = Depends(get_db)):
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
    user = await _get_user_by_id_for_auth(uuid.UUID(user_id), db)
    if user is None:
        #TODO::Убрать это нахуй
        #error
        return templates.TemplateResponse("auth/login.html", {"request": request,"dictStatus":dictStatus})
    else :
        aboutAuthor = await _get_about_author_by_user_id(user.user_id,db)
        films_by_author = await _get_all_film_by_user_id(uuid.UUID(user_id),db)

        awards = aboutAuthor.about_awards.split(';')
        if awards[-1] == '':
            awards = awards[0:len(awards)-1]

        dictTypeFilm = {"DIRECTOR":[],"PRODUCER":[],"DIRECTOR_PRODUCER":[],"ACTOR":[],"OPERATOR":[],"ART":[],"ART_LOOK":[],"COMPOSER":[],"AUTHOR":[],"ASSISTANT_PRODUCER":[],"ASSISTANT_OPERATOR":[],"GRIM":[],"SOUND":[],"VISUAL_EFFECTS":[],"GAFER":[],"PHOTO":[],}

        for film in films_by_author:
            type = film[0].type.value
            buf = dictTypeFilm[type]
            buf = buf + [str(film[0].film_id)]
            dictTypeFilm[type] = buf

        dictTypeFilm = dict(filter(lambda x: x[1], dictTypeFilm.items()))

        dictFilm = {}
        for key,value in dictTypeFilm.items():
            dictFilm[key] = []
            for v in value:
                film = await _get_film_by_uuid(v,db)
                dictFilm[key]  = dictFilm[key] + [(str(film.film_id),str(film.name))]

        return templates.TemplateResponse("author/viewAuthor.html", {"request": request,"user":user,"aboutAuthor":aboutAuthor,"awards":awards,"dictFilm":dictFilm,"dictStatus":dictStatus})


@author_router.get("/p/show/{user_id}")
async def get_role(user_id: str, request: Request,db: AsyncSession = Depends(get_db)):
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
    user = await _get_user_by_id_for_auth(uuid.UUID(user_id), db)
    if user is None:
        #error
        return templates.TemplateResponse("auth/login_mobile.html", {"request": request,"dictStatus":dictStatus})
    else :
        aboutAuthor = await _get_about_author_by_user_id(user.user_id,db)
        films_by_author = await _get_all_film_by_user_id(uuid.UUID(user_id),db)

        awards = aboutAuthor.about_awards.split(';')
        if awards[-1] == '':
            awards = awards[0:len(awards)-1]

        dictTypeFilm = {"DIRECTOR":[],"PRODUCER":[],
                        "DIRECTOR_PRODUCER":[],"ACTOR":[],"OPERATOR":[],"ART":[],"ART_LOOK":[],
                        "COMPOSER":[],"AUTHOR":[],"ASSISTANT_PRODUCER":[],"ASSISTANT_OPERATOR":[],
                        "GRIM":[],"SOUND":[],"VISUAL_EFFECTS":[],"GAFER":[],"PHOTO":[],
                        "HELP_OPERATOR":[],"HELP_AUTHOR":[],"WEAR_OPERATOR":[],"ART_OPERATOR":[],
                        "MAIN_ACTOR":[],"HELP_PRODUCER":[]}
        for film in films_by_author:
            type = film[0].type.value
            buf = dictTypeFilm[type]
            buf = buf + [str(film[0].film_id)]
            dictTypeFilm[type] = buf

        dictTypeFilm = dict(filter(lambda x: x[1], dictTypeFilm.items()))

        dictFilm = {}
        for key,value in dictTypeFilm.items():
            dictFilm[key] = []
            for v in value:
                film = await _get_film_by_uuid(v,db)
                dictFilm[key]  = dictFilm[key] + [(str(film.film_id),str(film.name))]

        return templates.TemplateResponse("author/viewAuthor_mobile.html", {"request": request,"user":user,"aboutAuthor":aboutAuthor,"awards":awards,"dictFilm":dictFilm,"dictStatus":dictStatus})






#изменить информацию об авторе#
@author_router.get("/change")
async def change_role(request: Request,db: AsyncSession = Depends(get_db)):
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
    if request.cookies.get('auth'):
        jwt = request.cookies.get('auth')
        try:
            user = await get_current_user_from_token(jwt,db)
        except:
            return templates.TemplateResponse("auth/login.html", {"request": request,"dictStatus":dictStatus})
        if user is None:
            return templates.TemplateResponse("auth/login.html", {"request": request,"dictStatus":dictStatus})
        else :
            author_or_not = await _get_author_or_not(user.user_id,db)
            if not author_or_not :
                return templates.TemplateResponse("auth/login.html", {"request": request,"dictStatus":dictStatus})

            author = await _get_about_author_by_user_id(user.user_id,db)
            if author is None:
                return templates.TemplateResponse("author/addAboutAuthor.html", {"request": request,"author":author,"thereare":False,"dictStatus":dictStatus})
            return templates.TemplateResponse("author/addAboutAuthor.html", {"request": request,"author":author,"thereare":True,"dictStatus":dictStatus})
    else:
        return templates.TemplateResponse("auth/login.html", {"request": request,"dictStatus":dictStatus})


@author_router.get("/p/change")
async def change_role(request: Request,db: AsyncSession = Depends(get_db)):
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
    if request.cookies.get('auth'):
        jwt = request.cookies.get('auth')
        try:
            user = await get_current_user_from_token(jwt,db)
        except:
            return templates.TemplateResponse("auth/login_mobile.html", {"request": request,"dictStatus":dictStatus})
        if user is None:
            return templates.TemplateResponse("auth/login_mobile.html", {"request": request,"dictStatus":dictStatus})
        else :
            author_or_not = await _get_author_or_not(user.user_id,db)
            if not author_or_not :
                return templates.TemplateResponse("auth/login_mobile.html", {"request": request,"dictStatus":dictStatus})

            author = await _get_about_author_by_user_id(user.user_id,db)
            if author is None:
                return templates.TemplateResponse("author/addAboutAuthor_mobile.html", {"request": request,"author":author,"thereare":False,"dictStatus":dictStatus})
            return templates.TemplateResponse("author/addAboutAuthor_mobile.html", {"request": request,"author":author,"thereare":True,"dictStatus":dictStatus})
    else:
        return templates.TemplateResponse("auth/login_mobile.html", {"request": request,"dictStatus":dictStatus})


@author_router.post("/change")
async def change_role(request: Request,info = Form(),db: AsyncSession = Depends(get_db)):
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
    if request.cookies.get('auth'):
        jwt = request.cookies.get('auth')
        try:
            user = await get_current_user_from_token(jwt,db)
        except:
            return templates.TemplateResponse("auth/login.html", {"request": request,"dictStatus":dictStatus})
        if user is None:
            return templates.TemplateResponse("auth/login.html", {"request": request,"dictStatus":dictStatus})
        else :
            data = eval(info)
            author = await _get_about_author_by_user_id(user.user_id, db)
            if author is None:
                await _add_about_author_by_user_id(user.user_id, data['about_person'],data['about_awards'], db)
            else :
                await _update_about_author(user.user_id, data, db)
            return templates.TemplateResponse("main_page.html", {"request": request,"dictStatus":dictStatus})
    else:
        return templates.TemplateResponse("auth/login.html", {"request": request,"dictStatus":dictStatus})
