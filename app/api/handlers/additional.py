import uuid
import shutil

from fastapi import Request, UploadFile
from fastapi import Depends
from fastapi import HTTPException, Form
from fastapi.responses import HTMLResponse

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sendsay.api import SendsayAPI
from api.actions.auth import enter_or_not
from api.actions.auth import get_current_user_from_token
from api.actions.additional import _get_mark_users,_get_history_users,_create_or_delete_mark,_film_is_mark_for_user,_create_rating
from api.actions.film import _search_film
from api.actions.additional import _create_comment,_create_new_responce,_get_comment_to_film
from api.actions.additional import _create_notification
from api.schemas import Film
from api.actions.auth import get_current_user_from_token
from api.actions.user import _get_status_user
from api.actions.additional import _get_notification_for_user

from db.session import get_db

from fastapi import APIRouter
from fastapi.templating import Jinja2Templates

additional_router = APIRouter()

templates = Jinja2Templates(directory="public")
#########################
#   ADD FILM            #
#########################



@additional_router.get("/history")
async def get_history_and_bookmark(request: Request, db: AsyncSession = Depends(get_db)):
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
            history = await _get_history_users(user.user_id,db)
            history = list(set(history))
            bookmark= await _get_mark_users(user.user_id,db)
            return templates.TemplateResponse("additional/history_bookmark.html", {"request": request,"history":history,"bookmark":bookmark,"dictStatus":dictStatus})
    else:
        return templates.TemplateResponse("auth/login.html", {"request": request,"dictStatus":dictStatus})

@additional_router.get("/p/history")
async def get_history_and_bookmark(request: Request, db: AsyncSession = Depends(get_db)):
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
            history = await _get_history_users(user.user_id,db)
            history = list(set(history))
            bookmark= await _get_mark_users(user.user_id,db)
            return templates.TemplateResponse("additional/history_bookmark_mobile.html", {"request": request,"history":history,"bookmark":bookmark,"dictStatus":dictStatus})
    else:
        return templates.TemplateResponse("auth/login_mobile.html", {"request": request,"dictStatus":dictStatus})


@additional_router.get("/callback")
async def get_search(request: Request, db: AsyncSession = Depends(get_db)):
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
    return templates.TemplateResponse("additional/callback.html", {"request": request,"dictStatus":dictStatus})

@additional_router.get("/p/callback")
async def get_search(request: Request, db: AsyncSession = Depends(get_db)):
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
    return templates.TemplateResponse("additional/callback_mini.html", {"request": request,"dictStatus":dictStatus})

@additional_router.post("/callback")
async def send_callback(request: Request, email = Form(),text = Form(), db: AsyncSession = Depends(get_db)):
    dictStatus = {"is_log": False, "is_author": False, "notification": list()}
    html_content = " mail from :"+ email + " message: " + text
    api = SendsayAPI(login='forworkkul2000pi@yandex.ru', password='N%\O^IR>L)')

    response = api.request('issue.send', {
        'sendwhen': 'now',
        'letter': {
            'subject': "Обратная связь",
            'from.name': "Donateatr",
            'from.email': "notification@donateatr.ru",
            'message': {
                'html': html_content
            },
        },
        'relink' : 1,
        'users.list': "feedback@donateatr.ru",
        'group' : 'personal',
    })
    
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
    return templates.TemplateResponse("additional/callback_mini.html", {"request": request,"dictStatus":dictStatus})


@additional_router.get("/search")
async def send_search(request: Request, db: AsyncSession = Depends(get_db)):
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
    return templates.TemplateResponse("additional/search.html", {"request": request,"dictStatus":dictStatus})

@additional_router.get("/search/{str_search}")
async def send_search(str_search:str,request: Request, db: AsyncSession = Depends(get_db)):
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
    if '_' in str_search:
        list_search = str_search.split('_')
        list_search = list(filter(None, list_search))
        listResult = []
        for el_search in list_search:
            buffer = await _search_film(el_search,el_search,db)
            if len(buffer) :
                listResult = listResult +  buffer
        search_film = listResult.pop()

    else :
        search_film = await _search_film(str_search,str_search,db)
    return templates.TemplateResponse("additional/search.html", {"request": request,"resultSearch":search_film,"dictStatus":dictStatus})


@additional_router.get("/addBookmark/{film_id}")
async def get_search(request: Request, film_id : str, db: AsyncSession = Depends(get_db)):
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
            user = await get_current_user_from_token(jwt, db)
        except:
            return templates.TemplateResponse("auth/login.html", {"request": request,"dictStatus":dictStatus})
        if user is None:
            return templates.TemplateResponse("auth/login.html", {"request": request,"dictStatus":dictStatus})
        else:
            bookmark = await _create_or_delete_mark(user.user_id,uuid.UUID(film_id),db)
            return bookmark
    else:
        return HTTPException(status_code=520, status_text=f"Database error: {'ew'}")



@additional_router.post("/get_mark")
async def send_mark(request: Request, info = Form(), db: AsyncSession = Depends(get_db)):
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
            user = await get_current_user_from_token(jwt, db)
        except:
            return templates.TemplateResponse("auth/login.html", {"request": request,"dictStatus":dictStatus})
        if user is None:
            return templates.TemplateResponse("auth/login.html", {"request": request,"dictStatus":dictStatus})
        else:
            infoToDict = eval(info)
            mark = await _create_rating(user.user_id,infoToDict['film_id'],float(infoToDict['rating']),db)
            return mark
    else:
        raise HTTPException(status_code=520, detail=f"Database error: ")

@additional_router.post("/sendComment")
async def send_comment(request: Request, info = Form(), db: AsyncSession = Depends(get_db)):
    if request.cookies.get('auth'):
        jwt = request.cookies.get('auth')
        try:
            user = await get_current_user_from_token(jwt, db)
        except:
            raise HTTPException(
                status_code=512,
                detail="Incorrect username or password",
            )
        if user is None:
            raise HTTPException(
                status_code=512,
                detail="Incorrect username or password",
            )
        else:
            infoToDict = eval(info)
            if infoToDict['to'] == "id":
                infoToDict['to'] = None
                film_id = infoToDict['film_id'].replace(" ", "")
                comment = await _create_comment(uuid.UUID(film_id),user.user_id,infoToDict['comment'],db)
            else:
                #await _create_notification(user.user_id,"Пользователь "+ +)
                film_id = infoToDict['film_id'].replace(" ", "")
                responce = await _create_new_responce(uuid.UUID(film_id),user.user_id,uuid.UUID(infoToDict['to']),infoToDict['comment'],db)
            return "True"
    else:
        return HTTPException(status_code=520, status_text=f"Database error: {'ew'}")

@additional_router.get("/p/notification")
async def get_search(request: Request, db: AsyncSession = Depends(get_db)):
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
    return templates.TemplateResponse("additional/notification_mobile.html", {"request": request,"dictStatus":dictStatus})

@additional_router.get("/about")
async def get_about(request: Request, db: AsyncSession = Depends(get_db)):
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
    return templates.TemplateResponse("additional/about.html", {"request": request,"dictStatus":dictStatus})
