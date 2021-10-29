from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from fastapi import FastAPI, Body


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



@app.post("/v1/users/", response_model=schemas.SchemeUsers)
def create_user(user: schemas.SchemeUsers = Body(...), db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
   
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/v1/users/", response_model=List[schemas.SchemeUsers])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    users2 = [{"id":user.id,"email": user.email, "password": user.password,
     "cpf": user.cpf, "address":user.address, "name":user.name} for user in users]
    
    return users2


@app.get("/v1/users/{user_id}", response_model=schemas.SchemeUsers)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
