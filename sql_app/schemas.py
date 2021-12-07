from typing import Optional
from pydantic import BaseModel

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
    evaluation: Optional[float]
    instagram: str


class SchemePortoMember(BaseModel):
    id: Optional[int]
    id_user: int
    workaddress: str
    company_name: Optional[str]


class SchemePilarMemberPost(BaseModel):
    id: Optional[int]
    user_id: int  # foreign key
    description: str
    title: Optional[str]
    rate: int


class SchemePostImage(BaseModel):
    id: Optional[int]
    id_post: int  # foreign key
    image: bytes
    filename: str
    size: int

class SchemeSkillPilarMember(BaseModel):
    id: Optional[int]
    id_pilarmember: int  # foreign key
    id_skill: int  # foreign key
    xp: Optional[int]
    description: Optional[str]


class SchemeMatch(BaseModel):
    id: Optional[int]
    id_pilarmember: int  # foreign key
    id_opportunity: int  # foreign key
    approved: Optional[bool]


class SchemeMatchEvaluation(BaseModel):
    id: Optional[int]
    id_match: int  # foreign key
    comment: str  # foreign key
    id_user: int
    stars: float


class SchemePreviousMatchMember(BaseModel):
    id: Optional[int]
    id_match: int
    id_match_user: int
    porto_member_user_id: int


# class SchemePreviousMatchMember(BaseModel)


class SchemeSkill(BaseModel):
    id: Optional[int]
    name: str


class SchemeLogin(BaseModel):
    login: str
    password: str


class SchemeOpportunity(BaseModel):
    id: Optional[int]
    id_portomember: int
    title: Optional[str]
    startDate: str
    endDate: str
    isactive: Optional[bool]
    description: str
    id_skill: int
    value: float
