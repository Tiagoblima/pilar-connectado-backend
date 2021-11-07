from typing import Optional
from pydantic import BaseModel
from sqlalchemy.sql.sqltypes import DateTime, Time

"""
Interage com o REST para o usuário.
"""


class SchemeUsers(BaseModel):

    email: str  # login ?
    name: str
    password: str
    address: str
    cpf: str


class SchemePhone(BaseModel):

    number: str
    type: str
    id_user: int  # foreign key


class SchemePilarMember(BaseModel):

    id_user: int  # foreign key
    introduction: str
    evaluation: float
    instagram: str


class SchemePortoMember(BaseModel):

    id_user: int
    workaddress: str


class SchemePilarMemberPost(BaseModel):

    user_id: int  # foreign key
    description: str
    rate: int


class SchemeSkillPilarMember(BaseModel):

    id_pilarmember: int  # foreign key
    id_skill: int  # foreign key
    xp: int
    description: str
    startTime: str
    endTime: str


class SchemeSkill(BaseModel):

    name: str


class SchemeLogin(BaseModel):
    login: str
    password: str
