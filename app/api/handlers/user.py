import uuid
import shutil

from hashing import Hasher

from fastapi import Request
from fastapi import Depends
from fastapi import HTTPException, Form
from fastapi import APIRouter
from fastapi import Request, UploadFile
from fastapi.templating import Jinja2Templates
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from api.actions.additional import _get_best_view,_get_notification_for_user
from api.actions.auth import enter_or_not
from api.actions.user import _create_new_user,_get_uuid_by_email_for_auth,_get_user_by_id_for_auth,_set_active_by_email_for_auth,_update_user, _get_status_user
from api.schemas import UserCreate, ShowUser, ActiveEmail
from api.actions.film import _create_new_film,_get_film_by_uuid,_get_15_new_film
from db.session import get_db

from datetime import timedelta

from fastapi import Request,Response
from fastapi import Depends
from fastapi import status
from fastapi import HTTPException

from fastapi.security import OAuth2PasswordRequestForm


from sqlalchemy.ext.asyncio import AsyncSession

from api.actions.auth import authenticate_user,get_current_user_from_token

from api.schemas import Token

from sendEmailToAuth import sendEmail


from security import create_access_token

from db.session import get_db

import settings

templates = Jinja2Templates(directory="public")

user_router = APIRouter()

#1 - Пользователь регистрируется
#GET
# показываем страницу регистрации
@user_router.get("/registration")
def registrationShowPage(request: Request):
    dictStatus = {"is_log": False, "is_author": False, "notification": list()}
    return templates.TemplateResponse("auth/registration.html", {"request": request,"dictStatus":dictStatus})

@user_router.get("/p/registration")
def registrationShowPage(request: Request):
    dictStatus = {"is_log": False, "is_author": False, "notification": list()}
    return templates.TemplateResponse("auth/registration_mobile.html", {"request": request,"dictStatus":dictStatus})

#POST
#обработка формы регистрации
@user_router.post("/registration", response_model=UserCreate)
async def registrationForm(body: UserCreate,response: Response, db: AsyncSession = Depends(get_db)):

    try:
        new_registation_user =  await _create_new_user(body, db)
        response.set_cookie(key='user', value=new_registation_user.email, httponly=True, secure=True, samesite='none')
        return new_registation_user
    except IntegrityError as err:
        raise HTTPException(status_code=520, status_text=f"Database error: {err}")


#2 - Пользователю показывается страница что нужно подтвердить письмо
#GET
#банер подтверждения почты
#TODO::КРАСИВОЕ ПИСЬМО
@user_router.get("/activeEmail")
async def confirmEmailShowPage(request: Request, db: AsyncSession = Depends(get_db)):
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
    if request.cookies.get('user'):
        user_email = request.cookies.get('user')
        id = await _get_uuid_by_email_for_auth(user_email,db)
        sendEmail(user_email, "127.0.0.1:8080/user/confirmEmail/"+str(id))
    return templates.TemplateResponse("auth/activeEmail.html", {"request": request,"dictStatus":dictStatus})

#POSTeк
#если пользователь с почты подтверждает письмоs
#ссылка на подтверждение мыла
@user_router.get("/confirmEmail/{id}")
async def confirmEmail(id: str,request: Request, db: AsyncSession = Depends(get_db)):
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
        email = await _get_user_by_id_for_auth(uuid.UUID(id),db)
        await _set_active_by_email_for_auth(email.email,db)
        return templates.TemplateResponse("main_page.html", {"request": request,"dictStatus":dictStatus})
    except IntegrityError as err:
        raise HTTPException(status_code=520, status_text=f"Database error: {err}")


#3 - Пользователь пытается войти
#GET
@user_router.get("/login")
def login(request: Request):
    dictStatus = {"is_log": False, "is_author": False, "notification": list()}
    return templates.TemplateResponse("auth/login.html", {"request": request,"dictStatus":dictStatus})

@user_router.get("/p/login")
async def login(request: Request, db: AsyncSession = Depends(get_db)):
    dictStatus = {"is_log": False, "is_author": False, "notification": list()}
    if request.cookies.get('auth'):
        jwt = request.cookies.get('auth')
        try:
            user = await get_current_user_from_token(jwt,db)
        except:
            return templates.TemplateResponse("auth/login_mobile.html", {"request": request,"dictStatus":dictStatus})
        if user is None:
            return templates.TemplateResponse("auth/login_mobile.html", {"request": request,"dictStatus":dictStatus})
        else :
            user_status = await _get_status_user(user.user_id, db)
            user_notification = await _get_notification_for_user(user.user_id, db)
            dictStatus = {"is_log": True, "is_author": user_status, "notification": user_notification}
            return templates.TemplateResponse("user/lk_mobile.html", {"request": request, "dictStatus": dictStatus})
    return templates.TemplateResponse("auth/login_mobile.html", {"request": request,"dictStatus":dictStatus})

#POST
@user_router.post("/login", response_model=Token)
async def login_for_access_token(response: Response,form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user = await authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException( status_code = 512, detail = "Incorrect username or password")
    if user.is_active == False:
        raise HTTPException(
            status_code = 511,
            detail="Incorrect username or password"
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    #информация в токене
    access_token = create_access_token(
        data={"sub": user.email, "other_custom_data": [1, 2, 3, 4]},
        expires_delta=access_token_expires,
    )
    response.set_cookie(key='auth',value=access_token,httponly=True, secure=True, samesite='none')

    return {"access_token": access_token, "token_type": "bearer"}





#4 - Служебные утилиты
#как проверять токен
@user_router.get("/change")
async def change_data(request: Request, db: AsyncSession = Depends(get_db)):
    dictStatus = {"is_log": False, "is_author": False, "notification": list()}
    if request.cookies.get('auth'):
        jwt = request.cookies.get('auth')
        try:
            user = await get_current_user_from_token(jwt,db)
        except:
            return templates.TemplateResponse("auth/login.html", {"request": request,"dictStatus":dictStatus})
        if user is None:
            return templates.TemplateResponse("auth/login.html", {"request": request,"dictStatus":dictStatus})
        else :
            user_status = await _get_status_user(user.user_id, db)
            user_notification = await _get_notification_for_user(user.user_id, db)
            dictStatus = {"is_log": True, "is_author": user_status, "notification": user_notification}
            return templates.TemplateResponse("user/changeUser.html", {"request": request,"dictStatus":dictStatus})
    else:
        return templates.TemplateResponse("auth/login.html", {"request": request,"dictStatus":dictStatus})

@user_router.get("/p/change")
async def change_data(request: Request, db: AsyncSession = Depends(get_db)):
    dictStatus = {"is_log": False, "is_author": False, "notification": list()}
    if request.cookies.get('auth'):
        jwt = request.cookies.get('auth')
        try:
            user = await get_current_user_from_token(jwt,db)
        except:
            return templates.TemplateResponse("auth/login_mobile.html", {"request": request,"dictStatus":dictStatus})
        if user is None:
            return templates.TemplateResponse("auth/login_mobile.html", {"request": request,"dictStatus":dictStatus})
        else :
            user_status = await _get_status_user(user.user_id, db)
            user_notification = await _get_notification_for_user(user.user_id, db)
            dictStatus = {"is_log": True, "is_author": user_status, "notification": user_notification}
            return templates.TemplateResponse("user/changeUser_mobile.html", {"request": request,"dictStatus":dictStatus})
    else:
        return templates.TemplateResponse("auth/login_mobile.html", {"request": request,"dictStatus":dictStatus})

@user_router.post("/changeWithoutPhoto")
async def change_data_post(request: Request,info = Form(),db: AsyncSession = Depends(get_db)):
    dictStatus = {"is_log": False, "is_author": False, "notification": list()}
    if request.cookies.get('auth'):
        jwt = request.cookies.get('auth')
        try:
            user = await get_current_user_from_token(jwt,db)
        except:
            return templates.TemplateResponse("auth/login.html", {"request": request})
        if user is None:
            return templates.TemplateResponse("auth/login.html", {"request": request})
        else :

            data = eval(info)
            if data['oldpassword'] == '' and data['newpassword'] == '':
                data = dict(filter(lambda x: x[1], data.items()))
                await _update_user(user.user_id,data,db)
            elif data['oldpassword'] == '' and data['newpassword'] != '':
                raise HTTPException(
                    status_code=512,
                    detail="Incorrect pasw password",
                )
            elif data['oldpassword'] != '' and data['newpassword'] == '':
                raise HTTPException(
                    status_code=513,
                    detail="Set new  password",
                )
            else:
                user = await authenticate_user(user.email, data['oldpassword'], db)
                if user is None:
                    raise HTTPException(
                        status_code=514,
                        detail="Old password not true",
                    )
                else:
                    data = dict(filter(lambda x: x[1], data.items()))
                    del data['oldpassword']
                    data['password'] = Hasher.get_password_hash(data['newpassword'])
                    del data['newpassword']

                    await _update_user(user.user_id,data,db)

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

            return templates.TemplateResponse("main_page.html", {"request": request,"dictStatus":dictStatus})
    else:
        return templates.TemplateResponse("auth/login.html", {"request": request,"dictStatus":dictStatus})

@user_router.post("/change")
async def change_data_post(request: Request,imagess: UploadFile,info = Form(),db: AsyncSession = Depends(get_db)):
    dictStatus = {"is_log": False, "is_author": False, "notification": list()}
    if request.cookies.get('auth'):
        jwt = request.cookies.get('auth')
        try:
            user = await get_current_user_from_token(jwt,db)
        except:
            return templates.TemplateResponse("auth/login.html", {"request": request,"dictStatus":dictStatus})
        if user is None:
            return templates.TemplateResponse("auth/login.html", {"request": request, "dictStatus": dictStatus})
        else :

            data = eval(info)
            if data['oldpassword'] == '' and data['newpassword'] == '':
                data = dict(filter(lambda x: x[1], data.items()))
                if len(data) == 0:
                    with open("Img/tmpImgUser/" + str(user.user_id) + ".png", "wb") as buffer:
                        shutil.copyfileobj(imagess.file, buffer)
                else :
                    with open("Img/tmpImgUser/" + str(user.user_id) + ".png", "wb") as buffer:
                        shutil.copyfileobj(imagess.file, buffer)
                    await _update_user(user.user_id,data,db)
            elif data['oldpassword'] == '' and data['newpassword'] != '':
                raise HTTPException(
                    status_code=512,
                    detail="Incorrect pasw password",
                )
            elif data['oldpassword'] != '' and data['newpassword'] == '':
                raise HTTPException(
                    status_code=513,
                    detail="Set new  password",
                )
            else:
                user = await authenticate_user(user.login, data['oldpassword'], db)
                if user is None:
                    raise HTTPException(
                        status_code=514,
                        detail="Old password not true",
                    )
                else:
                    data = dict(filter(lambda x: x[1], data.items()))
                    del data['oldpassword']
                    data['password'] = data['newpassword']
                    del data['newpassword']

                    with open("Img/tmpImgUser/" + str(user.user_id) + ".png", "wb") as buffer:
                        shutil.copyfileobj(imagess.file, buffer)

                    await _update_user(user.user_id,data,db)


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

            return templates.TemplateResponse("main_page.html", {"request": request, "dictStatus": dictStatus})
    else:
        return templates.TemplateResponse("auth/login.html", {"request": request, "dictStatus": dictStatus})



#4 - Служебные утилиты
#как проверять токен
@user_router.get("/check")
async def check_jwt(request: Request, db: AsyncSession = Depends(get_db)):
    if request.cookies.get('auth'):
        jwt = request.cookies.get('auth')
        user = await get_current_user_from_token(jwt,db)
        return user

#удаляем токен
@user_router.get("/exit")
async def delete_token(responce: Response,request: Request, db: AsyncSession = Depends(get_db)):
    dictStatus = {"is_log": False, "is_author": False, "notification": list()}

    new_film = await _get_15_new_film(db)
    best_film = await _get_best_view(db)

    responce = templates.TemplateResponse("main_page.html", {"request": request,"dictStatus":dictStatus,"new_film":new_film,"best_film":best_film})
    responce.delete_cookie(key='auth')
    return responce






