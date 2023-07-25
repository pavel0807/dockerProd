from datetime import datetime
from db.Models.Film import TypeOfFilm
from api.schemas import FilmCreate
from db.DALS.FilmDAL import FilmDAL

#TODO::обработка ошибок возврат результата
async def _create_new_film(body: FilmCreate, session):
    async with session.begin():
        film_dal = FilmDAL(session)
        date_add_str = "01-01-"+body.data_create
        date_object = datetime.strptime(date_add_str, '%m-%d-%Y').date()
        film = await film_dal.create_film(
            uuid=body.uuid,
            name=body.name,
            description=body.description,
            url = body.url,
            rating= 0,
            type_of_film=body.type_of_film,
            age_restriction=body.age_restriction,
            data_create = date_object
        )
        return body.uuid;


async def _get_film_by_uuid(film_id: str, session):
    async with session.begin():
        film_dal = FilmDAL(session)
        return await film_dal.get_film_by_uuid(film_id=film_id)


async def _get_film_by_type(type_film: TypeOfFilm, session) :
    async with session.begin():
        film_dal = FilmDAL(session)
        FilmToList =  await film_dal.get_film_by_type(type=type_film)
        return FilmToList

async def _get_15_new_film(session) :
    async with session.begin():
        film_dal = FilmDAL(session)
        FilmToList =  await film_dal.get_15_new_film()
        return FilmToList

async def _search_film(name: str,description:str,session) :
    async with session.begin():
        film_dal = FilmDAL(session)
        searchFilm =  await film_dal.search_film(name,description)
        listFilm = []
        for film in searchFilm:
            listFilm.append((film[0]))
        return searchFilm
