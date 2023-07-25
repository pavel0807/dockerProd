import uuid


from sqlalchemy import Column,String,Boolean,Date,Float,Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base

##############################
# BLOCK WITH DATABASE MODELS #
##############################

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    user_id = Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    name = Column(String,nullable=False)
    surname = Column(String,nullable=False)
    login = Column(String,nullable=False, unique=True)
    email = Column(String,nullable=False,unique=True)
    password = Column(String,nullable=False)
    dataBirthday = Column(Date,nullable=False)
    is_author = Column(Boolean,nullable=False)
    path_to_image = Column(String,nullable=False)
    is_active = Column(Boolean,nullable=False,default=False)
