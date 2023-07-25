import uuid
from datetime import datetime
from sqlalchemy import func
from db.Models.Additional import Notification,HistoryViewUser,CountViewFilm,BookmarkUser
from db.DALS.AdditionalDAL  import AdditionalDAL
from db.DALS.CommentDAL import CommentDAL


####################
#   NOTIFICATION   #
####################
async def _create_notification(user_id: uuid.UUID, description: str, session):
    async with session.begin():
        notification_dal = AdditionalDAL(session)
        notification = await notification_dal.create_notification(
            user_id=user_id,
            description=description
        )
        return notification
async def _change_view_notification(user_id:uuid.UUID , session):
    async with session.begin():
        notification_dal = AdditionalDAL(session)
        notification = await notification_dal.change_view_notification(
            user_id=user_id
        )
        return notification
async def _get_notification_for_user(user_id:uuid.UUID , session):
    async with session.begin():
        notification_dal = AdditionalDAL(session)
        notification = await notification_dal.get_notification_for_user(user_id=user_id)
        return notification

###################
#   HISORY VIEW   #
###################
async def _create_history(user_id: uuid.UUID,film_id: uuid.UUID, session):
    async with session.begin():
        history_view__dal = AdditionalDAL(session)
        history_view = await history_view__dal.create_history(
            user_id=user_id,
            film_id=film_id
        )
        return history_view

async def _get_history_users(user_id: uuid.UUID, session):
    async with session.begin():
        history_view__dal = AdditionalDAL(session)
        history_view = await history_view__dal.get_history_users(
            user_id=user_id
        )
        return history_view

#################
#   BOOK MARK   #
#################

async def _create_or_delete_mark(user_id :  uuid.UUID,film_id: uuid.UUID, session):
    async with session.begin():
        history_view__dal = AdditionalDAL(session)
        history_view = await history_view__dal.create_mark(
            user_id=user_id,
            film_id=film_id
        )
        return history_view

async def _get_mark_users(user_id: uuid.UUID, session):
    async with session.begin():
        history_view__dal = AdditionalDAL(session)
        history_view = await history_view__dal.get_mark_users(
            user_id=user_id
        )
        return history_view
async def _film_is_mark_for_user(user_id: uuid.UUID,film_id:uuid.UUID, session):
    async with session.begin():
        history_view__dal = AdditionalDAL(session)
        is_history_view = await history_view__dal.film_is_bookmark_for_user(
            user_id=user_id,
            film_id=film_id
        )
        return is_history_view

#################
#   COUNT VIEW  #
#################
async def _create_history_count_view(film_id: uuid.UUID, session):
    async with session.begin():
        history_view__dal = AdditionalDAL(session)
        history_count_view = await history_view__dal.create_clear_count_view(
            film_id=film_id
        )
        return history_count_view


async def _get_history_count_view(film_id: uuid.UUID, session):
    async with session.begin():
        history_view__dal = AdditionalDAL(session)
        history_count_view = await history_view__dal.get_count_view(
            film_id=film_id
        )
        return history_count_view

async def _add_history_count_view(film_id: uuid.UUID, session):
    async with session.begin():
        history_view__dal = AdditionalDAL(session)
        try:
            return await history_view__dal.add_count_view(film_id=film_id)
        except:
            print("bad")


async def _get_best_view(session):
    async with session.begin():
        history_view__dal = AdditionalDAL(session)
        history_count_view = await history_view__dal.get_15_best_view()
        return history_count_view

async def _create_rating(user_id: uuid.UUID, film_id: uuid.UUID, rating: float, session):
    async with session.begin():

        notification_dal = AdditionalDAL(session)
        notification = await notification_dal.create_mark_rating(
            user_id=user_id,
            film_id=film_id,
            rating=rating
        )
        return notification

####################
#   COMMENT        #
####################
async def _create_comment(film_id :uuid.UUID,from_id: uuid.UUID,data: str, session):
    async with session.begin():
        comment_dal = CommentDAL(session)
        notification = await comment_dal.create_new_comment(
            film_id=film_id,
            from_id=from_id,
            date_add=datetime.date(datetime.now()),
            data=data
        )
        return notification

async def _create_new_responce(film_id :uuid.UUID,from_id: uuid.UUID, to_id:uuid.UUID, data: str, session):
    async with session.begin():
        comment_dal = CommentDAL(session)
        notification = await comment_dal.create_new_responce(
            film_id=film_id,
            from_id=from_id,
            to_id=to_id,
            date_add=datetime.date(datetime.now()),
            data=data
        )
        return notification

async def _get_comment_to_film(film_id :uuid.UUID,session):
    async with session.begin():
        comment_dal = CommentDAL(session)
        comment_row = await comment_dal.get_comment_to_film(film_id)
        return comment_row



async def _get_comment_answer_to_film(to_id: uuid.UUID, comment_id:uuid.UUID,session):
    async with session.begin():
        comment_dal = CommentDAL(session)
        comment_row = await comment_dal.get_comment_answer_to_film(to_id,comment_id)
        return comment_row