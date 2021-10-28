from typing import Optional
from pydantic import BaseModel
from sqlalchemy.sql.sqltypes import DateTime

"""
Interage com o REST para o usuário.
"""

class SchemeUser(BaseModel):
    id: Optional[int] # primary key
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


class SchemePilarMember(SchemeUser):
    id: int # primary key
    introduction: str
    evaluation: float
    instagram: str

class SchemePortoMember(SchemeUser):
    id: int # primary key
    id_user: int
    workaddress: str


class SchemeSkillPilarMember(BaseModel):
    id: int # primary key
    id_pilarmember: int # foreign key
    id_skill: int # foreign key
    xp: int
    description: str
    startDateTime: DateTime
    endDateTime: DateTime
    
class SchemeSkill(BaseModel):
    id: int # primary key
    name: str
    

class SchemeLogin(BaseModel):
    login: str
    password: str