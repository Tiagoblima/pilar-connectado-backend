from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from fastapi import FastAPI, Body

from sql_app.crud import get_current_username
from sql_app.schemas import SchemeUsers

from sqlalchemy.orm import Session

app = FastAPI()

from sql_app import crud, models, schemas
from sql_app.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)


@app.get("/v1/")
def read_root():
    return {"Hello": "World"}


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/v1/users/")
def create_user(user: schemas.SchemeUsers = Body(...), db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)

    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = crud.create_user(db=db, user=user)
    return {"id": user.id, "email": user.email, "password": user.password, "name": user.name}


@app.get("/v1/users/", response_model=List[schemas.SchemeUsers])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    users2 = [{"id": user.id, "email": user.email, "password": user.password,
               "cpf": user.cpf, "address": user.address, "name": user.name} for user in users]

    return users2


@app.post("/v1/pilar_member/", response_model=schemas.SchemePilarMember)
def create_pilar_member(pilar_mbm: schemas.SchemePilarMember = Body(...), db: Session = Depends(get_db)):
    pilar_mbm = crud.create_pilar_member(db=db, pilar_mbm=pilar_mbm)
    return {"id": pilar_mbm.id, "introduction": pilar_mbm.introduction, "instagram": pilar_mbm.instagram,
            "id_user": pilar_mbm.id_user, "evaluation": pilar_mbm.evaluation}


@app.get("/v1/pilar_member/", response_model=List[schemas.SchemePilarMember])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    pilar_mbm = crud.get_pilar_member(db, skip=skip, limit=limit)
    pilar_mbm2 = [{"id": pilar_mbm.id, "introduction": pilar_mbm.introduction, "instagram": pilar_mbm.instagram,
                   "id_user": pilar_mbm.id_user, "evaluation": pilar_mbm.evaluation} for pilar_mbm in pilar_mbm]

    return pilar_mbm2


@app.get("/v1/users/{user_id}", response_model=schemas.SchemeUsers)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    user = {"id": db_user.id, "email": db_user.email, "password": db_user.password,
            "cpf": db_user.cpf, "address": db_user.address, "name": db_user.name}
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.get("/users/me")
def read_current_user(username: str = Depends(get_current_username)):
    return {"username": username}


@app.post("/v1/posts/", response_model=schemas.SchemePilarMemberPost)
def create_post(post: schemas.SchemePilarMemberPost = Body(...), db: Session = Depends(get_db)):
    post = crud.create_pilar_member_post(db=db, post=post)
    return {"id": post.id, "user_id": post.user_id, "description": post.description, "rate": post.rate}


@app.get("/v1/posts/", response_model=List[schemas.SchemePilarMemberPost])
def read_posts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    db_post = crud.get_posts(db, skip=skip, limit=limit)
    returned_post = [{"id": post.id, "user_id": post.user_id, "description": post.description,
                      "rate": post.rate} for post in db_post]
    return returned_post
