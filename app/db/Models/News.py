import uuid
import enum

from sqlalchemy import Column,String,Boolean,Date,Float,Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base

##############################
# BLOCK WITH DATABASE MODELS #
##############################

Base = declarative_base()
#класс фильмов
class News_AD(Base):
    __tablename__ = "News_Ad"
    news_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String,nullable=False)
    description = Column(String,nullable=False)
    news_or_ad =  Column(Boolean,nullable=False)


class Fest_AD(Base):
    __tablename__ = "Fest_AD"
    fest_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String,nullable=False)
    description = Column(String,nullable=False)
    news_or_ad =  Column(Boolean,nullable=False)
