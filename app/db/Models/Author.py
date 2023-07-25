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
    PRODUCER = "PRODUCER"   #продюсер
    DIRECTOR_PRODUCER = "DIRECTOR_PRODUCER" #режисер-постановщик
    ACTOR = "ACTOR" #актер
    OPERATOR = "OPERATOR"       #оператор-постановщик
    ART = "ART"     #художник-постановщик
    ART_LOOK = "ART_LOOK"    #художник по кастюмам
    COMPOSER = "COMPOSER"    #композитор
    AUTHOR = "AUTHOR"    #автор сценария
    ASSISTANT_PRODUCER = "ASSISTANT_PRODUCER"    #помошник режисера
    ASSISTANT_OPERATOR = "ASSISTANT_OPERATOR"    #ассистент оператора
    GRIM = "GRIM"    #грим
    SOUND = "SOUND"    #звукорежисер
    VISUAL_EFFECTS = "VISUAL_EFFECTS"    #художник по визуальным эффектам
    GAFER = "GAFER"    #гафер
    PHOTO = "PHOTO"    #фотограф

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