import uuid
from typing import Union

from sqlalchemy import select, desc,or_,func
from sqlalchemy.ext.asyncio import AsyncSession

from datetime import date
from datetime import datetime

from db.Models.Film import Film,TypeOfFilm
from db.Models.Film import AgeRestriction

############
# FILM DAL #
############
class FilmDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    # создание фильма
    async def create_film(self, uuid: uuid.UUID, name: str, description: str, url: str, rating: float,
                          type_of_film: str, age_restriction: str, data_create: date) -> Film:

        new_film = Film(film_id=uuid, name=name, description=description, url=url, rating=rating,
                        type_of_film=type_of_film,  data_create=data_create,
                        data_add=datetime.date(datetime.now()),age_restriction=age_restriction)
        self.db_session.add(new_film)
        await self.db_session.flush()
        return new_film

    async def get_film_by_uuid(self, film_id: str) -> Union[Film, None]:
        query = select(Film).where(Film.film_id == film_id)
        res = await self.db_session.execute(query)
        film_row = res.fetchone()
        if film_row is not None:
            return film_row[0]

    async def get_film_by_name(self, name: str) -> Union[Film, None]:
        query = select(Film).where(Film.name == name)
        res = await self.db_session.execute(query)
        film_row = res.fetchone()
        if film_row is not None:
            return film_row[0]


    #TODO://Need test and solution about order by
    async def get_film_by_type(self, type: TypeOfFilm):
        result = []
        query = select(Film).where(Film.type_of_film == type)
        res = await self.db_session.execute(query)
        film_row = res.fetchall()
        if film_row is not None:
            for row in film_row:
                result.append(row)
            return result
        return None

    async def get_15_new_film(self) -> Union[Film, None]:
        query = select(Film).order_by(desc(Film.data_add)).limit(15)
        res = await self.db_session.execute(query)
        news_row = res.fetchall()
        if news_row is not None:
            return news_row


    async def search_film(self,name: str, description: str) -> Union[Film, None]:
        search_name = "%{}%".format(name)
        search_descr = "%{}%".format(description)
        query = select(Film).filter(or_(Film.description.ilike(search_descr),Film.name.ilike(search_name)))
        res = await self.db_session.execute(query)
        news_row = res.fetchall()
        if news_row is not None:
            return news_row