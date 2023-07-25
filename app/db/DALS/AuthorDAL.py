from typing import Union
from uuid import UUID

from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date

from db.Models.Author import Author,AuthorAbout

##############
# AUTHOR DAL #
##############
class AuthorDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    # создание пользователя
    async def create_author(self, user_id:  UUID, film_id: UUID,type: str) -> Author:
        new_author = Author(user_id=user_id,film_id=film_id,type=type)
        self.db_session.add(new_author)
        await self.db_session.flush()
        return new_author

    # получение  пользователя по id
    async def get_all_film_by_user_id(self, user_id: UUID) -> Union[Author, None]:
        query = select(Author).where(Author.user_id == user_id)
        res = await self.db_session.execute(query)
        user_row = res.fetchall()
        if user_row is not None:
            return user_row

    async def get_author_by_film(self, film_id: UUID) -> Union[Author, None]:
        query = select(Author.user_id).where(Author.film_id == film_id)
        res = await self.db_session.execute(query)
        user_row = res.fetchone()
        if user_row is not None:
            return user_row[0]


class AuthorAboutDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def add_author_about(self, user_id: str,about_person:str,about_awards:str) -> Union[Author, None]:
        new_author_about = AuthorAbout(user_id=user_id,about_person=about_person,about_awards=about_awards)
        self.db_session.add(new_author_about)
        await self.db_session.flush()
        return new_author_about


    async def update_author_about(self, user_id: UUID,**kwargs) -> Union[UUID, None]:
        query = (
            update(AuthorAbout)
            .where(AuthorAbout.user_id == user_id)
            .values(kwargs)
            .returning(AuthorAbout.user_id)
        )
        res = await self.db_session.execute(query)
        update_user_id_row = res.fetchone()
        if update_user_id_row is not None:
            return update_user_id_row[0]

    async def get_author_about_by_user_id(self, user_id: UUID) -> Union[AuthorAbout, None]:
        query = select(AuthorAbout).where(AuthorAbout.user_id == user_id)
        res = await self.db_session.execute(query)
        user_row = res.fetchone()
        if user_row is not None:
            return user_row[0]


