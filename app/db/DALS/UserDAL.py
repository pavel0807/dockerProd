from typing import Union
from uuid import UUID

from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from datetime import date

from db.Models.User import User

############
# USER DAL #
############
class UserDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    # создание пользователя
    async def create_user(self, name: str, surname: str, login: str, email: str,  password: str,
                          dataBirthday: date, path_to_image: str) -> User:
        new_user = User(name=name, surname=surname, email=email, login=login, password=password,
                        dataBirthday=dataBirthday, is_author=False, path_to_image=path_to_image)
        self.db_session.add(new_user)
        await self.db_session.flush()
        return new_user

    # получение  пользователя по id
    async def get_user_by_id(self, user_id: UUID) -> Union[User, None]:
        query = select(User).where(User.user_id == user_id)
        res = await self.db_session.execute(query)
        user_row = res.fetchone()
        if user_row is not None:
            return user_row[0]

    # получение  пользователя по login
    async def get_user_by_login(self, login: str) -> Union[User, None]:
        query = select(User).where(User.login == login)
        res = await self.db_session.execute(query)
        user_row = res.fetchone()
        if user_row is not None:
            return user_row[0]

    # получение  пользователя по email
    async def get_user_by_email(self, email: str) -> Union[User, None]:
        query = select(User).where(User.email == email)
        res = await self.db_session.execute(query)
        user_row = res.fetchone()
        if user_row is not None:
            return user_row[0]

    #получение id по mail
    async def get_uuid_by_email(self, email: str) -> Union[UUID, None]:
        query = select(User.user_id).where(User.email == email)
        res = await self.db_session.execute(query)
        user_row = res.fetchone()
        if user_row is not None:
            return user_row[0]

    #проверка is_active по майлу
    async def get_active_by_email(self, email: str) -> Union[bool, None]:
        query = select(User.user_id).where(User.email == email)
        res = await self.db_session.execute(query)
        user_row = res.fetchone()
        if user_row is not None:
            return user_row[0]

    #проверка is_active по майлу
    async def activate_by_email(self, email: str) -> Union[bool, None]:
        query = (
            update(User)
                .where(User.email == email)
                .values({"is_active":True})
                .returning(User.user_id)
        )
        res = await self.db_session.execute(query)
        update_user_id_row = res.fetchone()
        if update_user_id_row is not None:
            return update_user_id_row[0]

    async def update_user(self, user_id: UUID, **kwargs) -> Union[UUID, None]:
        query = (
            update(User)
                .where(User.user_id == user_id)
                .values(kwargs)
                .returning(User.user_id)
        )
        res = await self.db_session.execute(query)
        update_user_id_row = res.fetchone()
        if update_user_id_row is not None:
            return update_user_id_row[0]

    async def user_author_or_not(self, user_id: UUID) -> bool:
        query = select(User.is_author).where(User.user_id == user_id)
        res = await self.db_session.execute(query)
        update_user_id_row = res.fetchone()
        if update_user_id_row is not None:
            return update_user_id_row[0]


'''
############
# Author DAL #
############

class AuthorDAL:
    def __init__(self,db_session:AsyncSession):
        self.db_session = db_session

    #TODO:: добавление оценок  и фильмов
    #создание пользователя
    async def add_author_from_user(self,author_id: UUID,description,mark,cinema ) -> Author:
        new_author = Author(author_id=author_id,description =description,mark = mark,cinema=cinema)
        self.db_session.add(new_author)
        await self.db_session.flussst()
        return new_author


    async def update_author_desc(self,author_id: UUID,new_description: str ) -> Author:
        query = (
            update(Author)
            .where(Author.user_id == author_id)
            .values(description=new_description)
            .returning(Author.user_id)
        )
        res = await self.db_session.execute(query)
        update_user_id_row = res.fetchone()
        if update_user_id_row is not None:
            return update_user_id_row[0]


    async def update_author_awards(self, author_id: UUID, new_awards: str) -> Author:
        query = (
            update(Author)
                .where(Author.user_id == author_id)
                .values(awards=new_awards)
                .returning(Author.user_id)
        )
        res = await self.db_session.execute(query)
        update_user_id_row = res.fetchone()
        if update_user_id_row is not None:
            return update_user_id_row[0]

    async def update_author_work(self, author_id: UUID, new_work: str) -> Author:
        query = (
            update(Author)
                .where(Author.user_id == author_id)
                .values(work=new_work)
                .returning(Author.user_id)
        )
        res = await self.db_session.execute(query)
        update_user_id_row = res.fetchone()
        if update_user_id_row is not None:
            return update_user_id_row[0]

'''