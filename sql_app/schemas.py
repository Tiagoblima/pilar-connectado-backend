from typing import Optional
from pydantic import BaseModel


class User(BaseModel):
    id: int # primary key
    email: str # login ?
    name: str 
    password: str
    address: str
    cpf:int
    
class Phone(BaseModel):
    id: int # primary key
    number: str
    type: str
    id_user: int # foreign key


class PilarMember(User):
    id: int # primary key
    introduction: str
    evaluation: float

class PortoMember(User):
    id: int # primary key
    id_user: int
    workaddress: str


class SkillPilarMember(BaseModel):
    id: int # primary key
    id_pilarmember: int # foreign key
    id_skill: int # foreign key
    xp: int
    description: str

class Skill(BaseModel):
    id: int # primary key
    name: str
    

class Login(BaseModel):
    login: str
    password: str