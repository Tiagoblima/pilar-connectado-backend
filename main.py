from typing import List

from datetime import datetime

from fastapi_utils.tasks import repeat_every
from fastapi import Depends, HTTPException
from fastapi import FastAPI, Body
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from sql_app.crud import get_current_username

from sql_app import crud, models, schemas
from sql_app.database import SessionLocal, engine
from fastapi.middleware.cors import CORSMiddleware

import VerifyDateChange

# Cors
origins = [

    "*",
]
# https://pilar-connectado.herokuapp.com/v1/
app = FastAPI(title="Pilar Connectado")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=engine)


@app.get("/v1/")
def read_root():
    return {"msg": "Hello World"}


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.on_event("startup")
@repeat_every(seconds=3600)  # 1 hour
def inactivate_opportunities(skip: int = 0, limit: int = 100):
    db = SessionLocal()
    try:
        db_opportunity = crud.get_opportunity(db, skip=skip, limit=limit)
        for opportunity in db_opportunity:
            now = datetime.today()
            opportunity_end_date = datetime.strptime(opportunity.endDate, '%d/%m/%Y')
            if opportunity_end_date < now and opportunity.isactive is True:
                crud.update_active_status(db, opportunity, False)

    except Exception as e:
        print("Error: ", e.__str__())



# region REST USER


@app.post("/v1/users/", tags=["Usuarios"])
def create_user(user: schemas.SchemeUsers = Body(...), db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)

    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = crud.create_user(db=db, user=user)
    return {"id": user.id, "email": user.email, "password": user.password, "name": user.name}


@app.get("/v1/users/", response_model=List[schemas.SchemeUsers], tags=["Usuarios"])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    users2 = [{"id": user.id, "email": user.email, "password": user.password,
               "cpf": user.cpf, "address": user.address, "name": user.name} for user in users]

    return users2


# @app.put("/v1/users/{user_id}", tags=["Usuarios"])
# def update_users(user: schemas.SchemeUsers = Body(...), db: Session = Depends(get_db)):
#     user = crud.update_user(db=db, user=user)
#     return {"id": user.id, "email": user.email, "password": user.password, "name": user.name}


@app.get("/v1/user/by/id/{user_id}/", response_model=schemas.SchemeUsers, tags=["Usuarios"])
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return jsonable_encoder(db_user)


@app.get("/v1/users/me", tags=["Usuarios"])
def read_current_user(username: str = Depends(get_current_username)):
    return {"username": username}


@app.get("/v1/member/{id_user}/", tags=["Usuarios"])
def read_pilar_member(id_user: int, db: Session = Depends(get_db)):
    member = crud.get_member(db, id_user=id_user)

    # member_json = {key: value for key, value in member.__dict__.items() if value is not None}

    return jsonable_encoder(member)


@app.put("/v1/users/{user_id}/", tags=["Usuarios"])
def update_user(user: schemas.SchemeUsers, db: Session = Depends(get_db)):
    response = crud.update_user(db, user=user)

    return response


@app.delete("/v1/users/{user_id}/", tags=["Usuarios"])
def delete_user(user: schemas.SchemeUsers, db: Session = Depends(get_db)):
    response = crud.delete_user(db, user=user)

    return response


# endregionS


#  region REST Mobile Phone

@app.post("/v1/users/", tags=["Usuarios"])
def create_user(user: schemas.SchemeUsers = Body(...), db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)

    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = crud.create_user(db=db, user=user)
    return jsonable_encoder(user)


@app.post("/v1/phone/", tags=["Phone"])
def create_user(phone: schemas.SchemePhone = Body(...), db: Session = Depends(get_db)):
    phone = crud.create_phone(db=db, phone=phone)
    return jsonable_encoder(phone)


@app.get("/v1/phone/", response_model=List[schemas.SchemePhone], tags=["Phone"])
def read_phones(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    phones = crud.get_phones(db, skip=skip, limit=limit)

    return jsonable_encoder(phones)


@app.get("/v1/phone/by/user/{id_user}/", response_model=List[schemas.SchemePhone], tags=["Phone"])
def read_phones(id_user: int, db: Session = Depends(get_db)):
    phones = crud.get_phones_by_id_user(db, id_user=id_user)

    return jsonable_encoder(phones)


@app.put("/v1/phone/by/user/{id_user}/", tags=["Phone"])
def update_phone(phone: schemas.SchemePhone, db: Session = Depends(get_db)):
    response = crud.update_phone(db, phone=phone)

    return response


@app.delete("/v1/phone/by/user/{id_user}/", tags=["Phone"])
def delete_phone(phone: schemas.SchemePhone, db: Session = Depends(get_db)):
    response = crud.delete_phone(db, phone=phone)

    return response


# endregion


#  region REST Pilar Member


@app.post("/v1/pilar_member/", response_model=schemas.SchemePilarMember, tags=["Pilar Member"])
def create_pilar_member(pilar_mbm: schemas.SchemePilarMember = Body(...), db: Session = Depends(get_db)):
    pilar_mbm = crud.create_pilar_member(db=db, pilar_mbm=pilar_mbm)
    return jsonable_encoder(pilar_mbm)


@app.get("/v1/pilar_member/", response_model=List[schemas.SchemePilarMember], tags=["Pilar Member"])
def read_pilar_member(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    pilar_mbm = crud.get_pilar_member(db, skip=skip, limit=limit)

    return jsonable_encoder(pilar_mbm)


@app.get("/v1/pilar_member/by/user/{user_id}/", tags=["Pilar Member"])
def read_pilar_member(user_id: int, db: Session = Depends(get_db)):
    pilar_mbm = crud.get_pilar_member_by_user_id(db, user_id)
    if not pilar_mbm:
        raise HTTPException(status_code=204, detail="There is no pilar member with this id user.")
    return jsonable_encoder(pilar_mbm)


@app.get("/v1/pilar_member/by/skill/{id_skill}/", tags=["Pilar Member"])
def read_pilar_member_by_skill(id_skill: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_pilar_member_by_skill(db, id_skill=id_skill, skip=skip, limit=limit)

    return users


@app.put("/v1/pilar_member/{user_id}/", tags=["Pilar Member"])
def update_pilar_member(pilar_mbm: schemas.SchemePilarMember, db: Session = Depends(get_db)):
    response = crud.update_pilar_member(db, user=pilar_mbm)

    return response


@app.delete("/v1/pilar_member/{user_id}/", tags=["Pilar Member"])
def delete_pilar_member(pilar_mbm: schemas.SchemePilarMember, db: Session = Depends(get_db)):
    response = crud.delete_pilar_member(db, pilar_member=pilar_mbm)

    return response


# endregion


# region REST Porto Member


@app.post("/v1/porto_member/", response_model=schemas.SchemePortoMember, tags=["Porto Member"])
def create_porto_member(porto_mbm: schemas.SchemePortoMember = Body(...), db: Session = Depends(get_db)):
    porto_mbm = crud.create_porto_member(db=db, porto_mbm=porto_mbm)
    return {"id": porto_mbm.id, "workaddress": porto_mbm.workaddress, "id_user": porto_mbm.id_user}


@app.get("/v1/porto_member/", response_model=List[schemas.SchemePortoMember], tags=["Porto Member"])
def read_porto_member(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    porto_mbm = crud.get_porto_member(db, skip=skip, limit=limit)

    return jsonable_encoder(porto_mbm)


@app.get("/v1/porto_member/by/id/{op_id}/", response_model=schemas.SchemePortoMember, tags=["Porto Member"])
def get_porto_member_by_id(op_id: int, db: Session = Depends(get_db)):
    porto_mbm = crud.get_porto_member_by_id(db, op_id=op_id)
    return jsonable_encoder(porto_mbm)


@app.get("/v1/porto_member/by/user/{op_id}/", response_model=schemas.SchemePortoMember, tags=["Porto Member"])
def get_porto_member_by_user_id(op_id: int, db: Session = Depends(get_db)):
    porto_mbm = crud.get_porto_member_by_user_id(db, op_id=op_id)

    if not porto_mbm:
        raise HTTPException(status_code=404, detail="There is no porto member with this id user.")

    return jsonable_encoder(porto_mbm)


@app.put("/v1/porto_member/by/id/{op_id}/", tags=["Porto Member"])
def update_porto_member(porto_mbm: schemas.SchemePortoMember, db: Session = Depends(get_db)):
    response = crud.update_porto_member(db, user=porto_mbm)

    return response


@app.delete("/v1/porto_member/by/id/{op_id}/", tags=["Porto Member"])
def delete_porto_member(porto_mbm: schemas.SchemePortoMember, db: Session = Depends(get_db)):
    response = crud.delete_porto_member(db, porto_member=porto_mbm)

    return response


# endregion


# region REST POST


@app.post("/v1/posts/", response_model=schemas.SchemePilarMemberPost, tags=["Post"])
def create_post(post: schemas.SchemePilarMemberPost = Body(...), db: Session = Depends(get_db)):
    post = crud.create_pilar_member_post(db=db, post=post)
    return {"id": post.id, "user_id": post.user_id, "description": post.description, "rate": post.rate}


@app.get("/v1/posts/", response_model=List[schemas.SchemePilarMemberPost], tags=["Post"])
def read_posts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    db_post = crud.get_posts(db, skip=skip, limit=limit)

    return jsonable_encoder(db_post)


@app.get("/v1/posts/{id_user}/", response_model=List[schemas.SchemePilarMemberPost], tags=["Post"])
def read_posts_by_user_id(user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    db_post = crud.get_posts_by_id_user(db, user_id, skip=skip, limit=limit)

    return jsonable_encoder(db_post)


@app.put("/v1/posts/{id_post}", tags=["Porto Member"])
def update_post(post: schemas.SchemePilarMemberPost, db: Session = Depends(get_db)):
    response = crud.update_post(db, post=post)

    return response


@app.delete("/v1/porto_member/by/id/{op_id}/", tags=["Porto Member"])
def delete_porto_member(post: schemas.SchemePilarMemberPost, db: Session = Depends(get_db)):
    response = crud.delete_post(db, post=post)

    return response


# endregion


# TODO: update and delete
# region REST SKILL


@app.post("/v1/skill/", response_model=schemas.SchemeSkill, tags=["Skill"])
def create_skill(skill: schemas.SchemeSkill = Body(...), db: Session = Depends(get_db)):
    skill = crud.create_skill(db=db, skill=skill)
    return {"id": skill.id, "name": skill.name}


@app.post("/v1/skill_pilar_member/", response_model=schemas.SchemeSkillPilarMember, tags=["Skill Pilar Member"])
def create_skill(skill_pilar_member: schemas.SchemeSkillPilarMember = Body(...), db: Session = Depends(get_db)):
    skill_pilar_member = crud.create_skill_pilar_member(db=db, skill_pilar_member=skill_pilar_member)
    return jsonable_encoder(skill_pilar_member)


@app.get("/v1/skill/", response_model=List[schemas.SchemeSkill], tags=["Skill"])
def get_skill(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    db_skill = crud.get_skill(db, skip=skip, limit=limit)
    returned_skill_list = [{"id": skill.id, "name": skill.name} for skill in db_skill]
    return returned_skill_list


@app.get("/v1/skill/by/id/{op_id}/", response_model=schemas.SchemeSkill, tags=["Skill"])
def get_skill_by_id(op_id: int, db: Session = Depends(get_db)):
    skill = crud.get_skill_by_id(db, op_id=op_id)
    return {"id": skill.id, "name": skill.name}


@app.get("/v1/skill_pilar_member/", response_model=List[schemas.SchemeSkillPilarMember], tags=["Skill Pilar Member"])
def get_skill(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    db_skill_pilar_member = crud.get_skill_pilar_member(db, skip=skip, limit=limit)

    return jsonable_encoder(db_skill_pilar_member)


# endregion


# region REST OPPORTUNITY


@app.post("/v1/opportunity/", response_model=schemas.SchemeOpportunity, tags=["Opportunity"])
def create_opportunity(opportunity: schemas.SchemeOpportunity = Body(...), db: Session = Depends(get_db)):
    opportunity = crud.create_opportunity(db=db, opportunity=opportunity)
    return jsonable_encoder(opportunity)


@app.get("/v1/opportunity/", response_model=List[schemas.SchemeOpportunity], tags=["Opportunity"])
def get_opportunity(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    db_opportunity = crud.get_opportunity(db, skip=skip, limit=limit)

    return jsonable_encoder(db_opportunity)


@app.get("/v1/opportunity/by/id/{op_id}/", response_model=schemas.SchemeOpportunity, tags=["Opportunity"])
def get_opportunity_by_id(op_id: int, db: Session = Depends(get_db)):
    opportunity = crud.get_opportunity_by_id(db, op_id=op_id)
    # returned_opportunity_list = [ for opportunity in
    #                              db_opportunity]
    return jsonable_encoder(opportunity)


@app.get("/v1/opportunity/by/porto_member_id/{porto_member_id}/", response_model=List[schemas.SchemeOpportunity],
         tags=["Opportunity"])
def get_opportunity_by_porto_member_id(porto_member_id: int, skip: int = 0, limit: int = 100,
                                       db: Session = Depends(get_db)):
    db_opportunity = crud.get_opportunity_by_porto_member_id(db, id_porto_member=porto_member_id, skip=skip,
                                                             limit=limit)
    returned_opportunity_list = [{"id": opportunity.id, "id_portomember": opportunity.id_portomember,
                                  "startDate": opportunity.startDate,
                                  "endDate": opportunity.endDate, "isactive": opportunity.isactive,
                                  "description": opportunity.description,
                                  "id_skill": opportunity.id_skill, "value": opportunity.value} for opportunity in
                                 db_opportunity]

    return returned_opportunity_list


@app.get("/v1/opportunity/by/skill/{id_skill}/", response_model=List[schemas.SchemeOpportunity], tags=["Opportunity"])
def get_opportunity_by_id(id_skill: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    db_opportunity = crud.get_opportunity_by_id_skill(db, id_skill=id_skill, skip=skip, limit=limit)
    returned_opportunity_list = [{"id": opportunity.id, "id_portomember": opportunity.id_portomember,
                                  "startDate": opportunity.startDate,
                                  "endDate": opportunity.endDate, "isactive": opportunity.isactive,
                                  "description": opportunity.description,
                                  "id_skill": opportunity.id_skill, "value": opportunity.value} for opportunity in
                                 db_opportunity]
    return returned_opportunity_list


@app.get("/v1/opportunity/by/value/{value}/", response_model=List[schemas.SchemeOpportunity], tags=["Opportunity"])
def get_opportunity_by_value(value: float, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    db_opportunity = crud.get_opportunity_by_value(db, value=value, skip=skip, limit=limit)
    returned_opportunity_list = [{"id": opportunity.id, "id_portomember": opportunity.id_portomember,
                                  "startDate": opportunity.startDate,
                                  "endDate": opportunity.endDate, "isactive": opportunity.isactive,
                                  "description": opportunity.description,
                                  "id_skill": opportunity.id_skill, "value": opportunity.value} for opportunity in
                                 db_opportunity]
    return returned_opportunity_list


@app.put("/v1/opportunity/{op_id}/", tags=["Opportunity"])
def update_opportunity(opportunity: schemas.SchemeOpportunity, db: Session = Depends(get_db)):
    response = crud.update_opportunity(db, opportunity=opportunity)

    return response


@app.delete("/v1/opportunity/{op_id}/", tags=["Opportunity"])
def update_opportunity(opportunity: schemas.SchemeOpportunity, db: Session = Depends(get_db)):
    response = crud.delete_opportunity(db, opportunity=opportunity)

    return response, "Opportunity id: " + opportunity.id.__str__() + "was deleted"


# endregion


# region Match REST


@app.post("/v1/match/", response_model=schemas.SchemeMatch, tags=["Match"])
def create_match(match: schemas.SchemeMatch = Body(...), db: Session = Depends(get_db)):
    db_match_list = crud.get_match_by_opportunity(db, id_opportunity=match.id_opportunity)

    for db_match in db_match_list:
        if db_match.id_pilarmember == match.id_pilarmember:
            raise HTTPException(status_code=400, detail="Match already registered")

    match = crud.create_match(db=db, match=match)
    return jsonable_encoder(match)


@app.post("/v1/match/evaluation/", response_model=schemas.SchemeMatchEvaluation, tags=["Match"])
def create_match(evaluation: schemas.SchemeMatchEvaluation = Body(...), db: Session = Depends(get_db)):
    match = crud.create_match_evaluation(db=db, evaluation=evaluation)
    return jsonable_encoder(match)


@app.get("/v1/match/", response_model=List[schemas.SchemeMatch], tags=["Match"])
def get_match(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    match_list = crud.get_match(db=db, skip=skip, limit=limit)
    return jsonable_encoder(match_list)


@app.get("/v1/match/evaluation/", response_model=List[schemas.SchemeMatchEvaluation], tags=["Match"])
def get_match(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    evaluation_list = crud.get_match_evaluation(db=db, skip=skip, limit=limit)
    return jsonable_encoder(evaluation_list)

# endregion


# region Previous Match Member

@app.post("/v1/previous_match_member/", response_model=schemas.SchemePreviousMatchMember,
          tags=["Previous Match Member"])
def create_previous_match_member(previous_match_member: schemas.SchemePreviousMatchMember = Body(...),
                                 db: Session = Depends(get_db)):
    match_member = crud.create_previous_match_member(db=db, previous_match_member=previous_match_member)
    return jsonable_encoder(match_member)


@app.get("/v1/previous_match_members/", response_model=List[schemas.SchemePreviousMatchMember], tags=["Previous Match Member"])
def get_previous_match_members(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    previous_match_members_list = crud.get_previous_match_member(db=db, skip=skip, limit=limit)
    return jsonable_encoder(previous_match_members_list)


@app.get("/v1/previous_match_member/{porto_member_user_id}", response_model=List[schemas.SchemePreviousMatchMember],
         tags=["Previous Match Member"])
def get_previous_match_member(porto_member_user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_previous_match_member_by_porto_member(db, porto_member_user_id=porto_member_user_id)

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return jsonable_encoder(db_user)


@app.get("/v1/previous_match_member_amount/{porto_member_user_id}", tags=["Previous Match Member"])
def get_previous_match_member_amount(porto_member_user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_previous_match_member_by_porto_member(db, porto_member_user_id=porto_member_user_id)

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return len(jsonable_encoder(db_user))

# endregion

