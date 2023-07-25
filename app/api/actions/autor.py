import uuid
from sqlalchemy.types import Boolean
from fastapi import HTTPException
from api.schemas import ShowUser
from api.schemas import AuthorCreateDirector
from db.DALS.AuthorDAL import  AuthorDAL,AuthorAboutDAL
from hashing import Hasher

from uuid import UUID


async def _create_new_director_author(body:AuthorCreateDirector, session) -> AuthorCreateDirector:
    async with session.begin():
        author_dal = AuthorDAL(session)
        author = await author_dal.create_author(
            user_id = body.user_id,
            film_id= body.film_id,
            type = "DIRECTOR"
        )
        return AuthorCreateDirector(
            user_id = body.user_id,
            film_id= body.film_id,
            type = "DIRECTOR"
        )
async def _create_new_author(user_id: uuid.UUID,film_id: uuid.UUID,type: str, session):
    async with session.begin():
        author_dal = AuthorDAL(session)
        author = await author_dal.create_author(user_id,film_id,type)
        return author


async def _get_id_author_by_film(film_id: uuid.UUID, session) -> UUID:
    async with session.begin():
        author_dal = AuthorDAL(session)
        author_id = await author_dal.get_author_by_film(film_id)
        return author_id

async def _get_all_film_by_user_id(user_id: uuid.UUID, session):
    async with session.begin():
        author_dal = AuthorDAL(session)
        films = await author_dal.get_all_film_by_user_id(user_id)
        return films

async def _get_author_or_not(user_id: uuid.UUID, session) -> bool:
    async with session.begin():
        author_dal = AuthorDAL(session)
        films_author = await author_dal.get_all_film_by_user_id(user_id)
        if films_author is None:
            return False
        return True

async def _get_about_author_by_user_id(user_id: uuid.UUID, session):
    async with session.begin():
        author_dal = AuthorAboutDAL(session)
        return await author_dal.get_author_about_by_user_id(user_id)

async def _update_about_author(id: UUID, ipdatee_author_param: dict, session):
    async with session.begin():
        author_dal = AuthorAboutDAL(session)
        return await author_dal.update_author_about(user_id=id, **ipdatee_author_param)

async def _add_about_author_by_user_id(user_id: str,about_person:str,about_awards:str, session):
    async with session.begin():
        author_dal = AuthorAboutDAL(session)
        author = await author_dal.add_author_about(
            user_id = user_id,
            about_person= about_person,
            about_awards = about_awards
        )
        return user_id
'''
async def _get_user_by_login_for_auth(login: str, session):
    async with session.begin():
        user_dal = UserDAL(session)
        return await user_dal.get_user_by_login(login=login)
'''