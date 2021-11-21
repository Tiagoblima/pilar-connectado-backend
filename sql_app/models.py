from sqlalchemy import Column, ForeignKey, Integer, String, Float, Date, Boolean
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
    number = Column(String)
    type = Column(String, index=True)
    id_user = Column(Integer, ForeignKey("Users.id"))

    owener = relationship("Users", back_populates="phone")

    class Config:
        orm_mode = True


class PilarMember(Base):
    __tablename__ = "PilarMember"
    # Column(Integer, ForeignKey("User.id"), primary_key=True, index=True)
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_user = Column(Integer, ForeignKey("Users.id", ondelete='CASCADE'), unique=True)
    introduction = Column(String)
    instagram = Column(String)
    evaluation = Column(Float, default=0)

    class Config:
        orm_mode = True


class PortoMember(Base):
    __tablename__ = "PortoMember"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_user = Column(Integer, ForeignKey("Users.id", ondelete='CASCADE'), index=True)
    workaddress = Column(String)
    company_name = Column(String)
    class Config:
        orm_mode = True


class PilarMemberPost(Base):
    __tablename__ = "PilarMemberPost"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    description = Column(String)
    rate = Column(Integer)
    user_id = Column(Integer, ForeignKey("Users.id", ondelete='CASCADE'))

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

    class Config:
        orm_mode = True


class Match(Base):
    __tablename__ = "Match"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_pilarmember = Column(Integer, ForeignKey("PilarMember.id", ondelete='CASCADE'), index=True)  # foreign key
    id_opportunity = Column(Integer, ForeignKey("Opportunity.id", ondelete='CASCADE'), index=True)  # foreign key
    approved = Column(Boolean, index=True, default=False)

    class Config:
        orm_mode = True


class MatchEvaluation(Base):
    __tablename__ = "MatchEvaluation"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_match = Column(Integer, ForeignKey("Match.id", ondelete='CASCADE'), index=True)  # foreign key
    id_user = Column(Integer, ForeignKey("Users.id", ondelete='CASCADE'), index=True)  # foreign key
    comment = Column(String, index=True, default=False)
    stars = Column(Float, index=True)

    class Config:
        orm_mode = True


class Opportunity(Base):
    __tablename__ = "Opportunity"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_portomember = Column(Integer, ForeignKey("PortoMember.id", ondelete='CASCADE'), index=True)  # foreign key
    startDate = Column(String)
    endDate = Column(String)
    isactive = Column(Boolean)
    description = Column(String)
    id_skill = Column(Integer, ForeignKey("Skill.id"), index=True)  # foreign key
    value = Column(Float)

    class Config:
        orm_mode = True
