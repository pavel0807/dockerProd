import uuid
from enum import Enum
import enum

from sqlalchemy import Column,String,Boolean,Date,Float,Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base

##############################
# BLOCK WITH DATABASE MODELS #
##############################

Base = declarative_base()

###############
# Комментарии #
###############
class Comment(Base):
    __tablename__ = "Comment"
    comment_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    film_id = Column(UUID(as_uuid=True),nullable=False)
    from_id = Column(UUID(as_uuid=True),nullable=False)
    to_id = Column(UUID(as_uuid=True),nullable=True,default=None)
    date_add = Column(Date,nullable=False,default=Date)
    data = Column(String,nullable=False)

