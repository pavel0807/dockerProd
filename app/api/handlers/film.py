import uuid
import shutil
import os

from fastapi import Request, UploadFile
from fastapi import Depends
from fastapi import APIRouter
from fastapi import HTTPException, Form
from fastapi.responses import HTMLResponse

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from api.actions.auth import enter_or_not
from api.actions.film import _create_new_film,_get_film_by_uuid
from api.actions.user import _get_user_by_id_for_auth,_set_user_author
from api.actions.auth import authenticate_user,get_current_user_from_token
from api.actions.autor import _create_new_director_author,_get_id_author_by_film
from api.actions.additional import _create_history_count_view,_add_history_count_view,_create_history,_film_is_mark_for_user,_get_comment_to_film,_get_comment_answer_to_film
from api.schemas import  FilmCreate
from api.schemas import AuthorCreateDirector
from api.actions.user import _get_status_user
from api.actions.additional import _get_notification_for_user
from db.session import get_db

from fastapi.templating import Jinja2Templates

film_router = APIRouter()

templates = Jinja2Templates(directory="public")
#########################
#   ADD FILM            #
#########################



@film_router.get("/add")
async def registration(request: Request, db: AsyncSession = Depends(get_db)):
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
            return templates.TemplateResponse("film/add_film.html", {"request": request,"dictStatus":dictStatus})
    else:
        return templates.TemplateResponse("auth/login.html", {"request": request,"dictStatus":dictStatus})

@film_router.get("/p/add")
async def registration(request: Request, db: AsyncSession = Depends(get_db)):
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
            return templates.TemplateResponse("film/add_film_mobile.html", {"request": request,"dictStatus":dictStatus})
    else:
        return templates.TemplateResponse("auth/login_mobile.html", {"request": request,"dictStatus":dictStatus})



#list[UploadFile]
@film_router.post("/add")
#TODO::ПРОВЕРКА ПАРАМЕТРОВ НА JS
async def Registration(request: Request,imagess: UploadFile,info = Form(), db: AsyncSession = Depends(get_db)):
    uuidFilm = uuid.uuid4()
    with open("Img/tmpImgFilm/"+str(uuidFilm)+".png", "wb") as buffer:
        shutil.copyfileobj(imagess.file, buffer)
    infoToDict = eval(info)
    url = infoToDict['url']
    if "youtube" in url:
        indexCod = str(url).find('=')
        url = url[indexCod+1:]
        url = "https://www.youtube.com/embed/"+url
    if "rutube" in url:
        indexCod = str(url).find('o/')
        url = url[indexCod+2:]
        url = "https://rutube.ru/play/embed/"+url
    if "vk" in url:
        indexCod = str(url).find('o-')
        url = url[indexCod+2:]
        url_first = url[:str(url).find('_')]
        url_sec = url[str(url).find('_')+1:str(url).find('%')]
        url = "https://vk.com/video_ext.php?oid=-"+url_first+"&id="+url_sec+"&hd=2"
    new_film = FilmCreate(uuidFilm,infoToDict['name'],infoToDict['description'],url,infoToDict['rating'],infoToDict['type_of_film'],infoToDict['age_restriction'],infoToDict['data_create'],infoToDict['data_add'])
    try:
        jwt = request.cookies.get('auth')
        user = await get_current_user_from_token(jwt,db)
        if user is None:
            raise HTTPException(status_code=520, status_text=f"Database error: User not found")
        film_id = await _create_new_film(new_film, db)
        author = AuthorCreateDirector(user_id = user.user_id,film_id=film_id)
        await _set_user_author(user.user_id,db)
        await _create_new_director_author(author, db)
        await _create_history_count_view(film_id,db)
        await _create_history(author.user_id,film_id,db)
    except IntegrityError as err:
        raise HTTPException(status_code=520, status_text=f"Database error: {err}")

###################
#   SHOW FILM     #
###################
#use film_router

#TODO::обработка HTML
@film_router.get("/watch/{uuid_film}",response_class=HTMLResponse)
async def showFilm(uuid_film: str, request: Request, db: AsyncSession = Depends(get_db)):
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
    try:
        film_info =  await _get_film_by_uuid(uuid_film, db)
        await _add_history_count_view(uuid.UUID(uuid_film),db)
        id_user_author = await _get_id_author_by_film(uuid.UUID(uuid_film),db)
        author_user = await _get_user_by_id_for_auth(id_user_author,db)
        str_uuid = str(author_user.user_id)
        await _create_history(author_user.user_id,film_info.film_id,db)
        pathToImg = "Img/tmpImgUser/"+str_uuid+".png"
        if os.path.exists(pathToImg):
            defaultImg = False
        else:
            defaultImg = True

        film_in_bookmark = False

        comment = await _get_comment_to_film(uuid.UUID(uuid_film),db)
        comment = list(reversed(comment))
        commentRes = list()
        i = 0
        for commentOne, userOne in comment:
            subComment = await _get_comment_answer_to_film(commentOne.to_id,commentOne.comment_id,db)
            subComment = list(reversed(subComment))
            subList = (subComment,i)
            commentRes.append((commentOne, userOne, subList))
            i = i + 1


        if request.cookies.get('auth'):
            jwt = request.cookies.get('auth')
            try:
                user = await get_current_user_from_token(jwt, db)
            except:
                return  templates.TemplateResponse("film/film_show.html", {"request": request,"comment":commentRes,"film_in_bookmark":film_in_bookmark,"film_info":film_info,"author_user":author_user,"thereareImg":defaultImg,"user_id":author_user.user_id,"dictStatus":dictStatus})
            if user is None:
                return  templates.TemplateResponse("film/film_show.html", {"request": request,"comment":commentRes,"film_in_bookmark":film_in_bookmark,"film_info":film_info,"author_user":author_user,"thereareImg":defaultImg,"user_id":author_user.user_id,"dictStatus":dictStatus})
            else:
                if film_info:
                    film_in_bookmark = await _film_is_mark_for_user(user.user_id,film_info.film_id,db)
        if film_info:
            return  templates.TemplateResponse("film/film_show.html", {"request": request,"comment":commentRes,"film_in_bookmark":film_in_bookmark,"film_info":film_info,"author_user":author_user,"thereareImg":defaultImg,"user_id":author_user.user_id,"dictStatus":dictStatus})
    except IntegrityError as err:
        raise HTTPException(status_code=520, status_text=f"Database error: {err}")





@film_router.get("/p/watch/{uuid_film}",response_class=HTMLResponse)
async def showFilm(uuid_film: str, request: Request, db: AsyncSession = Depends(get_db)):
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
    try:
        film_info =  await _get_film_by_uuid(uuid_film, db)
        await _add_history_count_view(uuid.UUID(uuid_film),db)
        id_user_author = await _get_id_author_by_film(uuid.UUID(uuid_film),db)
        author_user = await _get_user_by_id_for_auth(id_user_author,db)
        str_uuid = str(author_user.user_id)
        await _create_history(author_user.user_id,film_info.film_id,db)
        pathToImg = "Img/tmpImgUser/"+str_uuid+".png"
        if os.path.exists(pathToImg):
            defaultImg = False
        else:
            defaultImg = True

        film_in_bookmark = False

        comment = await _get_comment_to_film(uuid.UUID(uuid_film),db)
        comment = list(reversed(comment))
        commentRes = list()
        i = 0
        for commentOne, userOne in comment:
            subComment = await _get_comment_answer_to_film(commentOne.to_id,commentOne.comment_id,db)
            subComment = list(reversed(subComment))
            subList = (subComment,i)
            commentRes.append((commentOne, userOne, subList))
            i = i + 1


        if request.cookies.get('auth'):
            jwt = request.cookies.get('auth')
            try:
                user = await get_current_user_from_token(jwt, db)
            except:
                return  templates.TemplateResponse("film/film_show_mobile.html", {"request": request,"comment":commentRes,"film_in_bookmark":film_in_bookmark,"film_info":film_info,"author_user":author_user,"thereareImg":defaultImg,"user_id":author_user.user_id,"dictStatus":dictStatus})
            if user is None:
                return  templates.TemplateResponse("film/film_show_mobile.html", {"request": request,"comment":commentRes,"film_in_bookmark":film_in_bookmark,"film_info":film_info,"author_user":author_user,"thereareImg":defaultImg,"user_id":author_user.user_id,"dictStatus":dictStatus})
            else:
                if film_info:
                    film_in_bookmark = await _film_is_mark_for_user(user.user_id,film_info.film_id,db)
        if film_info:
            return  templates.TemplateResponse("film/film_show_mobile.html", {"request": request,"comment":commentRes,"film_in_bookmark":film_in_bookmark,"film_info":film_info,"author_user":author_user,"thereareImg":defaultImg,"user_id":author_user.user_id,"dictStatus":dictStatus})
    except IntegrityError as err:
        raise HTTPException(status_code=520, status_text=f"Database error: {err}")
