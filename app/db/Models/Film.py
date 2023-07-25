import uuid
import enum

from sqlalchemy import Column,String,Boolean,Date,Float,Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base

##############################
# BLOCK WITH DATABASE MODELS #
##############################

Base = declarative_base()

##########
# ФИЛЬМЫ #
##########
#Класс таблицы информации о фильме
#
#TODO:: перевести нормально
class TypeOfFilm(enum.Enum):
    COMEDY = "COMEDY"
    DRAMA = "DRAMA"
    FANTASY = "FANTASY"
    HORROR = "HORROR"
    TRILLER = "TRILLER"
    STUDY = "STUDY"
    MELODRAMMA = "MELODRAMMA"
    MULT = "MULT"
    DOC = "DOC"
    WEB = "WEB"

class AgeRestriction(enum.Enum):
    Age = "Age"
    Kids = "Kids"
    Children = "Children"
    Body = "Body"
    Big = "Big"

#класс фильмов
class Film(Base):
    __tablename__ = "Film"
    film_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String,nullable=False)
    description = Column(String,nullable=False)
    url = Column(String,nullable=False,unique=True)
    rating = Column(Float,nullable=False)
    type_of_film = Column(Enum(TypeOfFilm),nullable=False)
    data_create = Column(Date,nullable=False,default=Date)
    data_add = Column(Date,nullable=False,default=Date)
    age_restriction = Column(Enum(AgeRestriction),nullable=False)


