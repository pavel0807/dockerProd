import uuid
from typing import Union

from sqlalchemy import select, desc, update,values,distinct, delete
from sqlalchemy.ext.asyncio import AsyncSession

from db.Models.Additional import HistoryViewUser,CountViewFilm,Notification,BookmarkUser,RatingUser
from db.Models.Film import Film
##################
# ADDITIONAL DAL #
##################
class AdditionalDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session


    ####################
    #   NOTIFICATION   #
    ####################
    #создать уведомление
    async def create_notification(self, user_id: uuid.UUID, description: str) -> Notification:
        new_notification = Notification(user_id=user_id,description=description,  is_view = False)
        self.db_session.add(new_notification)
        await self.db_session.flush()
        return new_notification

    # сделать все уведомления просмотренными
    async def change_view_notification(self, user_id: uuid.UUID) -> Notification:
        query = update(Notification).where(Notification.user_id == user_id).values(is_view = True)
        try:
            return await self.db_session.execute(query)
        except:
            print("Bad view notification")

    #получить уведомления для пользователей
    async def get_notification_for_user(self, user_id: uuid.UUID) -> Notification:
        query = select(Notification).where(Notification.user_id == user_id and Notification.is_view == False)
        res = await self.db_session.execute(query)
        news_row = res.fetchall()
        if news_row is not None:
            return news_row


    #################
    #   BOOK MARK   #
    #################

    #сохранить что закладка просмотрена
    async def create_mark(self, user_id: uuid.UUID, film_id: uuid.UUID) -> bool:
        query = select(BookmarkUser).where(BookmarkUser.user_id == user_id,  BookmarkUser.film_id == film_id)
        res = await self.db_session.execute(query)
        news_row = res.fetchone()
        if not news_row:
            new_mark = BookmarkUser(user_id=user_id,film_id=film_id)
            self.db_session.add(new_mark)
            await self.db_session.flush()
            return True
        else:
            query = delete(BookmarkUser).where( BookmarkUser.film_id == film_id, BookmarkUser.user_id == user_id)
            res = await self.db_session.execute(query)
            return False

    #показать закладки просмотренные
    async def get_mark_users(self, user_id: uuid.UUID) -> BookmarkUser:
        query = select(Film).join(BookmarkUser, BookmarkUser.film_id == Film.film_id).where(BookmarkUser.user_id == user_id)
        res = await self.db_session.execute(query)
        news_row = res.fetchall()
        if news_row is not None:
            return news_row

    #показать закладки просмотренные
    async def film_is_bookmark_for_user(self, user_id: uuid.UUID,film_id: uuid.UUID) -> bool:
        query = select(BookmarkUser).where(BookmarkUser.film_id == film_id and BookmarkUser.user_id == user_id)
        res = await self.db_session.execute(query)
        news_row = res.fetchone()
        if news_row is not None:
            return True
        return False

    ###################
    #   HISORY VIEW   #
    ###################
    #сохранить что фильм просмотрена
    async def create_history(self, user_id: uuid.UUID, film_id: uuid.UUID) -> HistoryViewUser:
        new_history = HistoryViewUser(user_id=user_id,film_id=film_id)
        self.db_session.add(new_history)
        await self.db_session.flush()
        return new_history

    #показать фильмы просмотренные
    async def get_history_users(self, user_id: uuid.UUID) -> HistoryViewUser:
        query = select(Film).join(HistoryViewUser, HistoryViewUser.film_id == Film.film_id).where(HistoryViewUser.user_id == user_id)
        res = await self.db_session.execute(query)
        news_row = res.fetchall()
        if news_row is not None:
            return news_row



    #################
    #   COUNT VIEW  #
    #################
    #добавить фильм в базу данных для подсчета просмотров
    async def create_clear_count_view(self, film_id: uuid.UUID) -> CountViewFilm:
        new_count_view = CountViewFilm(film_id=film_id,count=0)
        self.db_session.add(new_count_view)
        await self.db_session.flush()
        return new_count_view

    #посмотреть количество просмотров
    async def get_count_view(self,film_id: uuid.UUID) -> str:
        query = select(CountViewFilm).where(CountViewFilm.film_id == film_id)
        res = await self.db_session.execute(query)
        news_row = res.fetchone()
        if news_row is not None:
            return str(news_row[0].count)

    #добавить +1 просмотр
    async def add_count_view(self,film_id: uuid.UUID):

        query = select(CountViewFilm).where(CountViewFilm.film_id == film_id)
        res = await self.db_session.execute(query)
        news_row = res.fetchone()
        if news_row is not None:
            oldValue = news_row[0].count
        else :
            oldValue = 0
        newValue = oldValue + 1
        query = update(CountViewFilm).where(CountViewFilm.film_id == film_id).values(count = newValue)
        try:
            return await self.db_session.execute(query)
        except:
            print("Bad add count View")

    async def get_15_best_view(self) -> Union[CountViewFilm, None]:
        query = select(Film).join(CountViewFilm, CountViewFilm.film_id == Film.film_id).order_by(desc(CountViewFilm.count)).limit(15)
        res = await self.db_session.execute(query)
        news_row = res.fetchall()
        if news_row is not None:
            return news_row


    async def create_mark_rating(self, user_id: uuid.UUID, film_id: uuid.UUID, rating: float):
        query = select(RatingUser).where(RatingUser.user_id == user_id, RatingUser.film_id == film_id)
        res = await self.db_session.execute(query)
        news_row = res.fetchone()
        if not news_row:
            new_mark = RatingUser(film_id = film_id,user_id=user_id,rating=rating)
            self.db_session.add(new_mark)
            await self.db_session.flush()
            return True
        else:
            query = update(RatingUser).where(RatingUser.user_id == user_id,RatingUser.film_id == film_id).values(rating=rating)
            res = await self.db_session.execute(query)
            return False
