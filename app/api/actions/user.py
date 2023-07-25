from fastapi import HTTPException
from api.schemas import ShowUser
from api.schemas import UserCreate,UserLogin
from db.DALS.UserDAL import UserDAL
from hashing import Hasher

from uuid import UUID


async def _create_new_user(body: UserCreate, session) -> ShowUser:
    user_by_login = await _get_user_by_login_for_auth(login=body.login, session=session)
    user_by_email = await _get_user_by_email_for_auth(email=body.email, session=session)

    if user_by_email != None:
        raise HTTPException(status_code=512, detail=f"Пользователь с такой почтой уже существует")

    if user_by_login != None:
        raise HTTPException(status_code=513, detail=f"Пользователь с таким логином уже существует")

    async with session.begin():
        user_dal = UserDAL(session)
        user = await user_dal.create_user(
            name=body.name,
            surname=body.surname,
            login = body.login,
            email=body.email,
            password=Hasher.get_password_hash(body.password),
            dataBirthday = body.dataBirthday,
            path_to_image=body.path_to_image,
        )
        return ShowUser(
            user_id = user.user_id,
            name = user.name,
            surname = user.surname,
            login = user.login,
            email = user.email,
            password = user.password,
            dataBirthday = user.dataBirthday,
            is_author = user.is_author,
            path_to_image = user.path_to_image
        )


async def _get_user_by_login_for_auth(login: str, session):
    async with session.begin():
        user_dal = UserDAL(session)
        return await user_dal.get_user_by_login(login=login)

async def _get_user_by_email_for_auth(email: str, session):
    async with session.begin():
        user_dal = UserDAL(session)
        return await user_dal.get_user_by_email(email=email)


async def _get_uuid_by_email_for_auth(email: str, session):
    async with session.begin():
        user_dal = UserDAL(session)
        return await user_dal.get_uuid_by_email(email=email)


async def _get_is_active_by_email_for_auth(email: str, session):
    async with session.begin():
        user_dal = UserDAL(session)
        return await user_dal.get_active_by_email(email=email)


async def _set_active_by_email_for_auth(email: str, session):
    async with session.begin():
        user_dal = UserDAL(session)
        return await user_dal.activate_by_email(email=email)

async def _get_user_by_id_for_auth(id: UUID, session):
    async with session.begin():
        user_dal = UserDAL(session)
        return await user_dal.get_user_by_id(user_id=id)

async def _update_user(id: UUID, ipdatee_user_param: dict, session):
    async with session.begin():
        user_dal = UserDAL(session)
        return await user_dal.update_user(user_id=id, **ipdatee_user_param)



async def _set_user_author(id: UUID, session):
    async with session.begin():
        user_dal = UserDAL(session)
        new = {"is_author":True}
        return await user_dal.update_user(user_id=id, **new)


async def _get_status_user(user_id :UUID, session):
    async with session.begin():
        user_dal = UserDAL(session)
        is_author = await user_dal.user_author_or_not(user_id)
        return is_author