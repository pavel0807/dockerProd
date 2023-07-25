import uuid

from db.Models.News import News_AD
from db.DALS.NewsDAL import NewsDAL

#TODO::обработка ошибок возврат результата
async def _create_new_news(title:str,description:str, session):
    async with session.begin():
        news_dal = NewsDAL(session)
        news = await news_dal.create_news(
            title=title,
            description=description
        )
        return news
async def _create_new_ad(title:str,description:str, session):
    async with session.begin():
        news_dal = NewsDAL(session)
        news = await news_dal.create_ad(
            title=title,
            description=description
        )
        return news
async def _get_news_by_uuid(news_id: uuid.UUID, session):
    async with session.begin():
        news_dal = NewsDAL(session)
        return await news_dal.get_news_or_ad_by_id(news_id=news_id)

async def _get_news(session):
    async with session.begin():
        news_dal = NewsDAL(session)
        return await news_dal.get_news()

async def _get_ad(session):
    async with session.begin():
        news_dal = NewsDAL(session)
        return await news_dal.get_ad()

async def _get_last_news(session):
    async with session.begin():
        news_dal = NewsDAL(session)
        return await news_dal.get_last_news()

async def _get_last_ad(session):
    async with session.begin():
        news_dal = NewsDAL(session)
        return await news_dal.get_last_ad()