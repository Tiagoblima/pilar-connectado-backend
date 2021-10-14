from typing import Optional
from pydantic import BaseModel


class User(BaseModel):
    email: str # login ?
    name: str 
    password: str
    address: str
    phone: str
    
class Login(BaseModel):
    login: str
    password: str