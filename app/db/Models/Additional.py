import uuid
import enum

from sqlalchemy import Column,String,Boolean,Date,Float,Enum,Integer, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base

##############################
# BLOCK WITH DATABASE MODELS #
##############################

Base = declarative_base()
#бд уведомлений
class Notification(Base):
    __tablename__ = "notification"
    not_id = Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True),nullable=False)
    description = Column(String,nullable=False)
    is_view = Column(Boolean,nullable=False,default=False)
    date = Column(Date, nullable=False,default=False)

#бд истори просмотренных видео
class HistoryViewUser(Base):
    __tablename__ = "historyViewUser"
    hist_id = Column(UUID(as_uuid=True),nullable=False,primary_key=True,default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True),nullable=False)
    film_id = Column(UUID(as_uuid=True),nullable=False)


class BookmarkUser(Base):
    __tablename__ = "bookmarkUser"
    mark_id = Column(UUID(as_uuid=True),nullable=False,primary_key=True,default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True),nullable=False)
    film_id = Column(UUID(as_uuid=True),nullable=False)



#бд количества просмотров
class CountViewFilm(Base):
    __tablename__ = "countViewFilm"
    hist_view_id = Column(UUID(as_uuid=True),nullable=False,default=uuid.uuid4,primary_key=True)
    film_id = Column(UUID(as_uuid=True),nullable=False)
    count = Column(Integer,default=0)


class RatingUser(Base):
    __tablename__ = "ratingUser"
    rating_id = Column(UUID(as_uuid=True),nullable=False,default=uuid.uuid4,primary_key=True)
    film_id = Column(UUID(as_uuid=True),nullable=False)
    user_id = Column(UUID(as_uuid=True),nullable=False)
    rating = Column(Numeric,nullable=False,default=0)