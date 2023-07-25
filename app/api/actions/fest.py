import uuid

from db.Models.News import Fest_AD
from db.DALS.FestDAL import FestDAL

#TODO::обработка ошибок возврат результата
async def _create_new_news_fest(title:str,description:str, session):
    async with session.begin():
        news_dal = FestDAL(session)
        news = await news_dal.create_news(
            title=title,
            description=description
        )
        return news
async def _create_new_ad_fest(title:str,description:str, session):
    async with session.begin():
        news_dal = FestDAL(session)
        news = await news_dal.create_ad(
            title=title,
            description=description
        )
        return news
async def _get_news_by_uuid_fest(fest_id: uuid.UUID, session):
    async with session.begin():
        news_dal = FestDAL(session)
        return await news_dal.get_news_or_ad_by_id(fest_id=fest_id)

async def _get_news_fest(session):
    async with session.begin():
        news_dal = FestDAL(session)
        return await news_dal.get_news()

async def _get_ad_fest(session):
    async with session.begin():
        news_dal = FestDAL(session)
        return await news_dal.get_ad()

async def _get_last_news_fest(session):
    async with session.begin():
        news_dal = FestDAL(session)
        return await news_dal.get_last_news()

async def _get_last_ad_fest(session):
    async with session.begin():
        news_dal = FestDAL(session)
        return await news_dal.get_last_ad()