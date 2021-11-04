from typing import Optional
from pydantic import BaseModel
from sqlalchemy.sql.sqltypes import DateTime, Time

"""
Interage com o REST para o usuário.
"""


class SchemeUsers(BaseModel):
    id: int  # primary key
    email: str  # login ?
    name: str
    password: str
    address: str
    cpf: str


class SchemePhone(BaseModel):
    id: int  # primary key
    number: str
    type: str
    id_user: int  # foreign key


class SchemePilarMember(BaseModel):
    id: int  # primary key
    id_user: int  # foreign key
    introduction: str
    evaluation: float
    instagram: str


class SchemePortoMember(BaseModel):
    id: int  # primary key
    id_user: int
    workaddress: str


class SchemePilarMemberPost(BaseModel):
    id: int  # primary key
    user_id: int  # foreign key
    description: str
    rate: int


class SchemeSkillPilarMember(BaseModel):
    id: int  # primary key
    id_pilarmember: int  # foreign key
    id_skill: int  # foreign key
    xp: int
    description: str
    startTime: str
    endTime: str


class SchemeSkill(BaseModel):
    id: int  # primary key
    name: str


class SchemeLogin(BaseModel):
    login: str
    password: str
