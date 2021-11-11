from typing import Optional
from pydantic import BaseModel
from sqlalchemy.sql.sqltypes import DateTime, Time, Date

"""
Interage com o REST para o usuário.
"""


class SchemeUsers(BaseModel):
    id: Optional[int]
    email: str  # login ?
    name: str
    password: str
    address: str
    cpf: str


class SchemePhone(BaseModel):
    id: Optional[int]
    number: str
    type: str
    id_user: int  # foreign key


class SchemePilarMember(BaseModel):
    id: Optional[int]
    id_user: int  # foreign key
    introduction: str
    evaluation: float
    instagram: str


class SchemePortoMember(BaseModel):
    id: Optional[int]
    id_user: int
    workaddress: str


class SchemePilarMemberPost(BaseModel):
    id: Optional[int]
    user_id: int  # foreign key
    description: str
    rate: int


class SchemeSkillPilarMember(BaseModel):
    id: Optional[int]
    id_pilarmember: int  # foreign key
    id_skill: int  # foreign key
    xp: int
    description: str


class SchemeMatch(BaseModel):
    id: Optional[int]
    id_pilarmember: int  # foreign key
    id_opportunity: int  # foreign key
    approved: bool


class SchemeMatchEvaluation(BaseModel):
    id: Optional[int]
    id_match: int  # foreign key
    comment: str  # foreign key
    id_user: int
    stars: float


class SchemeSkill(BaseModel):
    id: Optional[int]
    name: str


class SchemeLogin(BaseModel):
    login: str
    password: str


class SchemeOpportunity(BaseModel):
    id: Optional[int]
    id_portomember: int
    startDate: str
    endDate: str
    isactive: bool
    description: str
    id_skill: int
    value: float
