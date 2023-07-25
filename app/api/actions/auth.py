
from typing import Union
from uuid import UUID
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Request

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordBearer


from jose import jwt
from jose import JWTError

from starlette import status

import settings
from hashing import Hasher

from db.session import get_db
from db.Models.User import User
from api.actions.user import _get_user_by_email_for_auth

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/token")

async def authenticate_user(email:str,password:str, db) -> Union[User, None]:
    user_by_email = await _get_user_by_email_for_auth(email=email, session=db)
    if user_by_email is None:
        return
    if not Hasher.verify_password(password, user_by_email.password):
        return
    return user_by_email


async def get_current_user_from_token(token: str , db: AsyncSession = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await _get_user_by_email_for_auth(email=email, session=db)
    if user is None:
        raise credentials_exception
    return user

async def enter_or_not(request: Request):
    if request.cookies.get('auth'):
        jwt = request.cookies.get('auth')
        user = await get_current_user_from_token(jwt)
        return user