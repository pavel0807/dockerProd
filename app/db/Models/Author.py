import uuid
import enum

from sqlalchemy import Column,String,Boolean,Date,Float,Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base

##############################
# BLOCK WITH DATABASE MODELS #
##############################

Base = declarative_base()
class TypeOfAuthor(enum.Enum):
    DIRECTOR = "DIRECTOR"    #режисер
    PRODUCER = "PRODUCER"
    DIRECTOR_PRODUCER = "DIRECTOR_PRODUCER"
    HELP_PRODUCER = "HELP_PRODUCER"
    MAIN_ACTOR = "MAIN_ACTOR"
    ACTOR = "ACTOR"
    OPERATOR = "OPERATOR"
    HELP_OPERATOR = "HELP_OPERATOR"
    AUTHOR = "AUTHOR"
    ART_OPERATOR = "ART_OPERATOR"
    WEAR_OPERATOR = "WEAR_OPERATOR"
    GRIM = "GRIM"
    VISUAL_EFFECTS = "VISUAL_EFFECTS"
    SOUND = "SOUND"
    HELP_AUTHOR = "HELP_AUTHOR"
    ASSISTANT_PRODUCER = "ASSISTANT_PRODUCER"

class Author(Base):
    __tablename__ = "author"
    author_id = Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True),nullable=False)
    film_id = Column(UUID(as_uuid=True),nullable=False)
    type = Column(Enum(TypeOfAuthor),nullable=False)

class AuthorAbout(Base):
    __tablename__ = "authorAbout"
    user_id = Column(UUID(as_uuid=True),primary_key=True,nullable=False)
    about_person = Column(String,nullable=True)
    about_awards = Column(String,nullable=True)