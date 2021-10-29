from typing import Optional
from pydantic import BaseModel
from sqlalchemy.sql.sqltypes import DateTime, Time

"""
Interage com o REST para o usuário.
"""

class SchemeUsers(BaseModel):
    id: int # primary key
    email: str # login ?
    name: str 
    password: str
    address: str
    cpf:int
    
class SchemePhone(BaseModel):
    id: int # primary key
    number: str
    type: str
    id_user: int # foreign key


class SchemePilarMember(SchemeUsers):
    id: int # primary key
    introduction: str
    evaluation: float
    instagram: str

class SchemePortoMember(SchemeUsers):
    id: int # primary key
    id_user: int
    workaddress: str


class SchemeSkillPilarMember(BaseModel):
    id: int # primary key
    id_pilarmember: int # foreign key
    id_skill: int # foreign key
    xp: int
    description: str
    startTime: str
    endTime: str

class SchemeSkill(BaseModel):
    id: int # primary key
    name: str
    

class SchemeLogin(BaseModel):
    login: str
    password: str