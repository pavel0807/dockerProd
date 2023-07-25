import uuid
from sqlalchemy import select,join

from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date


from db.Models.Comment import  Comment
from db.Models.User import User

###############
# COMMENT DAL #
###############
class CommentDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    # создание коммента
    async def create_new_comment(self, film_id: uuid.UUID, from_id: uuid.UUID, date_add: date, data: str) -> Comment:
        new_comment = Comment(film_id=film_id, from_id=from_id, date_add=date_add, data=data)
        self.db_session.add(new_comment)
        await self.db_session.flush()
        return new_comment

    # создание ответа на коммент
    async def create_new_responce(self, film_id: uuid.UUID, from_id: uuid.UUID, to_id: uuid.UUID, date_add: date,
                                  data: str) -> Comment:
        new_comment = Comment(film_id=film_id, from_id=from_id, to_id=to_id, date_add=date_add, data=data)
        self.db_session.add(new_comment)
        await self.db_session.flush()
        return new_comment

    # получить комментарии
    async def get_comment_to_film(self, film_id: uuid.UUID):
        query = select(Comment,User).where(Comment.film_id == film_id, Comment.to_id == None).join(User, Comment.from_id == User.user_id).order_by(Comment.date_add)
        res = await self.db_session.execute(query)
        comment_row = res.fetchall()
        if comment_row is not None:
            return comment_row

    async def get_comment_answer_to_film(self, to_id: uuid.UUID, comment_id:uuid.UUID ):
        query = select(Comment,User).where(Comment.to_id == comment_id).join(User, Comment.from_id == User.user_id)
        res = await self.db_session.execute(query)
        comment_row = res.fetchall()
        if comment_row is not None:
            return comment_row

    async def get_author_comment(self, comment_id: uuid.UUID ):
        query = select(User).where(Comment.to_id == comment_id).join(User, Comment.from_id == User.user_id)
        res = await self.db_session.execute(query)
        comment_row = res.fetchall()
        if comment_row is not None:
            return comment_row
