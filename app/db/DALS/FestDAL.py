import uuid
from typing import Union

from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from db.Models.News import Fest_AD

############
# NEWS DAL #
############
class FestDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_news(self, title: str, description: str):
        new_news = Fest_AD( title=title,description=description,  news_or_ad = True)
        self.db_session.add(new_news)
        await self.db_session.flush()
        return new_news.fest_id
    async def create_ad(self,title: str, description: str):
        new_news = Fest_AD(title=title,description=description,  news_or_ad = False)
        self.db_session.add(new_news)
        await self.db_session.flush()
        return new_news.fest_id

    async def get_news(self) -> Union[Fest_AD, None]:
        query = select(Fest_AD).where(Fest_AD.news_or_ad == True).order_by(desc(Fest_AD.fest_id))
        res = await self.db_session.execute(query)
        news_row = res.fetchall()
        if news_row is not None:
            return news_row
    async def get_news_or_ad_by_id(self,fest_id: uuid.UUID) -> Union[Fest_AD, None]:
        query = select(Fest_AD).where(Fest_AD.fest_id == fest_id)
        res = await self.db_session.execute(query)
        news_row = res.fetchall()
        if news_row is not None:
            return news_row[0]

    async def get_ad(self) -> Union[Fest_AD, None]:
        query = select(Fest_AD).where(Fest_AD.news_or_ad == False).order_by(desc(Fest_AD.fest_id))
        res = await self.db_session.execute(query)
        news_row = res.fetchall()
        if news_row is not None:
            return news_row


    async def get_last_ad(self) -> Union[Fest_AD, None]:
        query = select(Fest_AD).where(Fest_AD.news_or_ad == False).order_by(desc(Fest_AD.fest_id)).limit(10)
        res = await self.db_session.execute(query)
        news_row = res.fetchall()
        if news_row is not None:
            return news_row

    async def get_last_news(self) -> Union[Fest_AD, None]:
        query = select(Fest_AD).where(Fest_AD.news_or_ad == True).order_by(desc(Fest_AD.fest_id)).limit(10)
        res = await self.db_session.execute(query)
        news_row = res.fetchall()
        if news_row is not None:
            return news_row