from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship

from .database import Base

"""
Faz o mapeamento para o banco de dados

"""


class Users(Base):
    __tablename__ = "Users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    name = Column(String)
    address = Column(String)
    cpf = Column(String, unique=True, index=True)

    phone = relationship("Phone", back_populates="owener")

    class Config:
        orm_mode = True


class Phone(Base):
    __tablename__ = "Phone"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    number = Column(Integer)
    type = Column(String, index=True)
    id_user = Column(Integer, ForeignKey("Users.id"))

    owener = relationship("Users", back_populates="phone")

    class Config:
        orm_mode = True


class PilarMember(Base):
    __tablename__ = "PilarMember"
    # Column(Integer, ForeignKey("User.id"), primary_key=True, index=True)
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_user = Column(Integer, ForeignKey("Users.id"))
    introduction = Column(String)
    instagram = Column(String)
    evaluation = Column(Float)

    class Config:
        orm_mode = True


class PortoMember(Base):
    __tablename__ = "PortoMember"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("Users.id"), index=True)
    workaddress = Column(String)

    class Config:
        orm_mode = True


class PilarMemberPost(Base):
    __tablename__ = "PilarMemberPost"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    description = Column(String)
    rate = Column(Integer)
    user_id = Column(Integer, ForeignKey("Users.id"))

    class Config:
        orm_mode = True


class Skill(Base):
    __tablename__ = "Skill"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)  # primary key
    name = Column(String)

    class Config:
        orm_mode = True


class SkillPilarMember(Base):
    __tablename__ = "SkillPilarMember"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_pilarmember = Column(Integer, ForeignKey("PilarMember.id"), index=True)  # foreign key
    id_skill = Column(Integer, ForeignKey("Skill.id"), index=True)  # foreign key
    xp = Column(Integer, index=True)
    description = Column(String)

    startTime = Column(String)
    endTime = Column(String)

    class Config:
        orm_mode = True
