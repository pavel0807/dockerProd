import uuid

from fastapi import Request, UploadFile
from fastapi import Depends
from fastapi import HTTPException, Form

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession


from api.actions.auth import enter_or_not
from api.actions.fest import _get_news_fest,_get_ad_fest,_get_news_by_uuid_fest,_get_last_news_fest,_get_last_ad_fest,_create_new_news_fest,_create_new_ad_fest
from api.schemas import News_AD
from api.actions.auth import get_current_user_from_token
from api.actions.user import _get_status_user
from api.actions.additional import _get_notification_for_user



from db.session import get_db


import shutil
from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
fest_router = APIRouter()

templates = Jinja2Templates(directory="public")
#########################
#   ADD NEWS            #
#########################

@fest_router.get("/add")
async def get_upload_news(request: Request, db: AsyncSession = Depends(get_db)):
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
    return templates.TemplateResponse("fest/addFest.html",{"request": request,"dictStatus":dictStatus})

@fest_router.post("/add")
async def post_upload_news(request: Request,imagess: UploadFile,info = Form(), db: AsyncSession = Depends(get_db)):
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
    infoToDict = eval(info)
    if infoToDict['type'] == "news":
        news_id = await _create_new_news_fest(infoToDict['name'],infoToDict['news'],db)
        with open("Img/tmpImgFest/" + str(news_id) + ".png", "wb") as buffer:
            shutil.copyfileobj(imagess.file, buffer)
    elif infoToDict['type'] == "ad":
        news_id = await  _create_new_ad_fest(infoToDict['name'],infoToDict['news'],db)
        with open("Img/tmpImgFest/" + str(news_id) + ".png", "wb") as buffer:
            shutil.copyfileobj(imagess.file, buffer)
    else:
        return HTTPException(status_code=520)

    return templates.TemplateResponse("fest/addFest.html",{"request": request,"dictStatus":dictStatus})

@fest_router.get("/")
async def getMainPageNews(request: Request, db: AsyncSession = Depends(get_db)):
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
        ten_last_news = await _get_last_news_fest(db)
        ten_last_ad = await _get_last_ad_fest(db)
        return templates.TemplateResponse("fest/fest_ad_main.html", {"request": request,"last_news":ten_last_news,"last_ad":ten_last_ad,"dictStatus":dictStatus})
    except IntegrityError as err:
        raise HTTPException(status_code=520, status_text=f"Database error: {err}")

@fest_router.get("/p/")
async def getMainPageNews(request: Request, db: AsyncSession = Depends(get_db)):
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
        ten_last_news = await _get_last_news_fest(db)
        ten_last_ad = await _get_last_ad_fest(db)
        return templates.TemplateResponse("fest/fest_ad_main_mobile.html", {"request": request,"last_news":ten_last_news,"last_ad":ten_last_ad,"dictStatus":dictStatus})
    except IntegrityError as err:
        raise HTTPException(status_code=520, status_text=f"Database error: {err}")


@fest_router.get("/{type_film}")
async def getAllNewsOrAd(type_film: str, request: Request, db: AsyncSession = Depends(get_db)):
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
    list_type_of_film = ["NEWS","AD"]
    if type_film not in list_type_of_film:
        return getMainPageNews(request=request)
    if type_film == "NEWS":
        needed_news = await _get_news_fest(db)
    else:
        needed_news = await _get_ad_fest(db)
    return templates.TemplateResponse("fest/fest_ad_all.html",{"request": request,"type":type_film,"listNews":needed_news,"dictStatus":dictStatus})

@fest_router.get("/p/{type_film}")
async def getAllNewsOrAd(type_film: str, request: Request, db: AsyncSession = Depends(get_db)):
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
    list_type_of_film = ["NEWS","AD"]
    if type_film not in list_type_of_film:
        return getMainPageNews(request=request)
    if type_film == "NEWS":
        needed_news = await _get_news_fest(db)
    else:
        needed_news = await _get_ad_fest(db)
    return templates.TemplateResponse("fest/fest_ad_all_mobile.html",{"request": request,"type":type_film,"listNews":needed_news,"dictStatus":dictStatus})

@fest_router.get("/watch/{type}/{fest_id}")
async def getPageNews(type : str, fest_id : str, request: Request, db: AsyncSession = Depends(get_db)):
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
    list_type_of_film = ["NEWS", "AD"]
    if type not in list_type_of_film:
        return getMainPageNews(request=request)
    try:
        news =  await _get_news_by_uuid_fest(uuid.UUID(fest_id), db)
        if news:
            return  templates.TemplateResponse("fest/fest_show.html", {"request": request,"news":news,"type":type,"dictStatus":dictStatus})
    except IntegrityError as err:
        raise HTTPException(status_code=520, status_text=f"Database error: {err}")

@fest_router.get("/p/watch/{type}/{fest_id}")
async def getPageNews(type : str, fest_id : str, request: Request, db: AsyncSession = Depends(get_db)):
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
    list_type_of_film = ["NEWS", "AD"]
    if type not in list_type_of_film:
        return getMainPageNews(request=request)
    try:
        news =  await _get_news_by_uuid_fest(uuid.UUID(fest_id), db)
        if news:
            return  templates.TemplateResponse("fest/fest_show_mobile.html", {"request": request,"news":news,"type":type,"dictStatus":dictStatus})
    except IntegrityError as err:
        raise HTTPException(status_code=520, status_text=f"Database error: {err}")