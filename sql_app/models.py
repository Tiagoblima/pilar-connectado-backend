from sqlalchemy import Boolean, Column, ForeignKey, Integer, String,Float
from sqlalchemy.orm import relationship

from .database import Base

"""
Faz o mapeamento para o banco de dados

"""


class User(Base):

    __tablename__ = "User"


    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    name = Column(String)
    address = Column(String)
    cpf = Column(Integer, unique=True, index=True)
    
    phone = relationship("Phone", back_populates="user")
    class Config:
        orm_mode = True


class Phone(Base):

    __tablename__ = "Phone"


    id = Column(Integer, primary_key=True, index=True)
    number = Column(Integer)
    type = Column(String, index=True)
    id_user = Column(Integer, ForeignKey("User.id"))

    user = relationship("User", back_populates="Phone")
   
    class Config:
        orm_mode = True

class PilarMember(Base):

    __tablename__ = "PilarMember"

    id = Column(Integer, ForeignKey("User.id"), primary_key=True, index=True)
    introduction = Column(String)
    evaluation = Column(Float)

    owner = relationship("User", back_populates="id")

    class Config:
        orm_mode = True


class PortoMember(Base):

    __tablename__ = "PortoMember"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("User.id"), index=True)
    workaddress: Column(String)

    class Config:
        orm_mode = True

class Skill(Base):
    __tablename__ = "Skill"
    id =  Column(Integer, primary_key=True, index=True) # primary key
    name = Column(String)

    class Config:
        orm_mode = True

class SkillPilarMember(Base):

    __tablename__ = "SkillPilarMember"

    id = Column(Integer, primary_key=True, index=True)
    id_pilarmember = Column(Integer, ForeignKey("PilarMember.id"), index=True) # foreign key
    id_skill = Column(Integer, ForeignKey("Skill.id"),  index=True) # foreign key
    xp = Column(Integer, index=True)
    description = Column(String)

    class Config:
        orm_mode = True

    