from typing import Optional
from pydantic import BaseModel
from fastapi import FastAPI
import requests
from models import Login, User


app = FastAPI()



@app.get("/v1/")
def read_root():
    return {"Hello": "World"}

@app.get("/v1/user/login/")
def get_user_by_login(login: Login):
    """
    Acessa o base de dados com as
    informações do usuário e realiza o login
    return: Retorna o usário pelo login
    """
    return {
        "user_id": 1,
        "name": "Foo",
        "description": "The pretender",
        "price": 42.0,
        "tax": 3.2
    }

@app.get("/v1/user/{user_id}/")
def get_user_by_id(user_id: int):

    """
    O endpoint retorna o usuário pelo ID
    return: retorna as informações do usuário.
    """
    # TODO Acessar o banco de dados para retornar o o usuário pelo ID
    return {
        "user_id": 1,
        "name": "Foo",
        "description": "The pretender",
        "price": 42.0,
        "tax": 3.2
    }


@app.put("/v1/user/{user_id}/")
async def update_item(user_id: int, user: User):
   
   """
    O endendpont atualiza o usuário pelo ID
    return: retorna a mensagem se o usário foi atualizado com sucesso ou não
   """

   # TODO Acessa o banco de dados passando o ID e os dados atualizados 
   # do usuário.
   return {"msg": "Item atualizado com sucesso!"}

@app.post("/v1/user/")
async def create_user(item: User):
   
    """
    O endndpoint cria um usuário 
    return: retorna o ID do usuário criado 
    """

    # TODO Acessa o banco de dados e salva o novo usuário
    
    return {"user_id": 3}


@app.delete("/v1/user/{user_id}")
async def delete_user_by_id(user_id: int):

    """
    O endpoint deleta um usuário 
    retorn: retorna uma messagem se a delação foi com sucesso ou não
    """
    # TODO Acessa o banco de dados e deleta um usuário


    return {"msg": "Deletado com sucesso!"}

