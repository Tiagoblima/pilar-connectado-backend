from typing import List

from fastapi import Depends, HTTPException
from fastapi import FastAPI, Body
from sqlalchemy.orm import Session

from sql_app.crud import get_current_username

from sql_app import crud, models, schemas
from sql_app.database import SessionLocal, engine
from fastapi.middleware.cors import CORSMiddleware

# Cors
origins = [

    "http://127.0.0.1:5500",
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


# ----------------- REST USER ----------------


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


@app.get("/v1/users/{user_id}", response_model=schemas.SchemeUsers, tags=["Usuarios"])
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    user = {"id": db_user.id, "email": db_user.email, "password": db_user.password,
            "cpf": db_user.cpf, "address": db_user.address, "name": db_user.name}
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.get("/users/me", tags=["Usuarios"])
def read_current_user(username: str = Depends(get_current_username)):
    return {"username": username}


@app.get("/v1/member/{id_user}/", tags=["Usuarios"])
def read_pilar_member(id_user: int, db: Session = Depends(get_db)):
    member = crud.get_member(db, id_user=id_user)

    member_json = {key: value for key, value in member.__dict__.items() if value is not None}

    return member_json


# ---------------------------------------------------------------------

# -----------------------REST Pilar Member ----------------------------------------


@app.post("/v1/pilar_member/", response_model=schemas.SchemePilarMember, tags=["Pilar Member"])
def create_pilar_member(pilar_mbm: schemas.SchemePilarMember = Body(...), db: Session = Depends(get_db)):
    pilar_mbm = crud.create_pilar_member(db=db, pilar_mbm=pilar_mbm)
    return {"id": pilar_mbm.id, "introduction": pilar_mbm.introduction, "instagram": pilar_mbm.instagram,
            "id_user": pilar_mbm.id_user, "evaluation": pilar_mbm.evaluation}


@app.get("/v1/pilar_member/", response_model=List[schemas.SchemePilarMember], tags=["Pilar Member"])
def read_pilar_member(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    pilar_mbm = crud.get_pilar_member(db, skip=skip, limit=limit)
    pilar_mbm_list = [{"id": pilar_mbm.id, "introduction": pilar_mbm.introduction, "instagram": pilar_mbm.instagram,
                       "id_user": pilar_mbm.id_user, "evaluation": pilar_mbm.evaluation} for pilar_mbm in pilar_mbm]

    return pilar_mbm_list


@app.get("/v1/pilar_member/by/skill/{id_skill}/", tags=["Pilar Member"])
def read_pilar_member_by_skill(id_skill: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_pilar_member_by_skill(db, id_skill=id_skill, skip=skip, limit=limit)

    return users


# --------------------------------------------------------------

# REST Porto Member --------------------------------------------------

@app.post("/v1/porto_member/", response_model=schemas.SchemePortoMember, tags=["Porto Member"])
def create_porto_member(porto_mbm: schemas.SchemePortoMember = Body(...), db: Session = Depends(get_db)):
    porto_mbm = crud.create_porto_member(db=db, porto_mbm=porto_mbm)
    return {"id": porto_mbm.id, "workaddress": porto_mbm.workaddress, "id_user": porto_mbm.id_user}


@app.get("/v1/porto_member/", response_model=List[schemas.SchemePortoMember], tags=["Porto Member"])
def read_porto_member(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    porto_mbm = crud.get_porto_member(db, skip=skip, limit=limit)

    porto_mbm_list = [{"id": porto_mbm.id, "workaddress": porto_mbm.workaddress, "id_user": porto_mbm.id_user}
                      for porto_mbm in porto_mbm]

    return porto_mbm_list


# ------------------------------------------------------------------------------


# REST POSTER ----------------------------------
@app.post("/v1/posts/", response_model=schemas.SchemePilarMemberPost, tags=["Post"])
def create_post(post: schemas.SchemePilarMemberPost = Body(...), db: Session = Depends(get_db)):
    post = crud.create_pilar_member_post(db=db, post=post)
    return {"id": post.id, "user_id": post.user_id, "description": post.description, "rate": post.rate}


@app.get("/v1/posts/", response_model=List[schemas.SchemePilarMemberPost], tags=["Post"])
def read_posts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    db_post = crud.get_posts(db, skip=skip, limit=limit)
    returned_post = [{"id": post.id, "user_id": post.user_id, "description": post.description,
                      "rate": post.rate} for post in db_post]
    return returned_post


@app.get("/v1/posts/{id_user}/", response_model=List[schemas.SchemePilarMemberPost], tags=["Post"])
def read_posts_by_user_id(user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    db_post = crud.get_posts_by_id_user(db, user_id, skip=skip, limit=limit)
    returned_post = [{"id": post.id, "user_id": post.user_id, "description": post.description,
                      "rate": post.rate} for post in db_post]
    return returned_post


# --------------------------------------------------

# REST SKILL -------------------------------

@app.post("/v1/skill/", response_model=schemas.SchemeSkill, tags=["Skill"])
def create_skill(skill: schemas.SchemeSkill = Body(...), db: Session = Depends(get_db)):
    skill = crud.create_skill(db=db, skill=skill)
    return {"id": skill.id, "name": skill.name}


@app.get("/v1/skill/", response_model=List[schemas.SchemeSkill], tags=["Skill"])
def get_skill(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    db_skill = crud.get_skill(db, skip=skip, limit=limit)
    returned_skill_list = [{"id": skill.id, "name": skill.name} for skill in db_skill]
    return returned_skill_list


# -------------------------------------------------------


@app.post("/v1/skill_pilar_member/", response_model=schemas.SchemeSkillPilarMember, tags=["Skill Pilar Member"])
def create_skill(skill_pilar_member: schemas.SchemeSkillPilarMember = Body(...), db: Session = Depends(get_db)):
    skill_pilar_member = crud.create_skill_pilar_member(db=db, skill_pilar_member=skill_pilar_member)
    return {"id": skill_pilar_member.id, "id_pilarmember": skill_pilar_member.id_pilarmember,
            "id_skill": skill_pilar_member.id_skill,
            "xp": skill_pilar_member.xp, "description": skill_pilar_member.description}


@app.get("/v1/skill_pilar_member/", response_model=List[schemas.SchemeSkillPilarMember], tags=["Skill Pilar Member"])
def get_skill(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    db_skill = crud.get_skill_pilar_member(db, skip=skip, limit=limit)
    returned_skill_list = [{"id": skill_pilar_member.id, "id_pilarmember": skill_pilar_member.id_pilarmember,
                            "id_skill": skill_pilar_member.id_skill, "xp": skill_pilar_member.xp,
                            "description": skill_pilar_member.description} for skill_pilar_member in db_skill]
    return returned_skill_list


# --------------------------------------------------

# REST OPPORTUNITY -------------------------------


@app.post("/v1/opportunity/", response_model=schemas.SchemeOpportunity, tags=["Opportunity"])
def create_opportunity(opportunity: schemas.SchemeOpportunity = Body(...), db: Session = Depends(get_db)):
    opportunity = crud.create_opportunity(db=db, opportunity=opportunity)
    return {
        "id": opportunity.id, "id_portomember": opportunity.id_portomember, "startDate": opportunity.startDate,
        "endDate": opportunity.endDate, "isactive": opportunity.isactive,
        "description": opportunity.description,
        "id_skill": opportunity.id_skill, "value": opportunity.value
    }


@app.get("/v1/opportunity/", response_model=List[schemas.SchemeOpportunity], tags=["Opportunity"])
def get_opportunity(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    db_opportunity = crud.get_opportunity(db, skip=skip, limit=limit)
    returned_opportunity_list = [{"id": opportunity.id, "id_portomember": opportunity.id_portomember,
                                  "startDate": opportunity.startDate,
                                  "endDate": opportunity.endDate, "isactive": opportunity.isactive,
                                  "description": opportunity.description,
                                  "id_skill": opportunity.id_skill, "value": opportunity.value} for opportunity in
                                 db_opportunity]
    return returned_opportunity_list


@app.get("/v1/opportunity/by/id/{op_id}/", response_model=schemas.SchemeOpportunity, tags=["Opportunity"])
def get_opportunity_by_id(op_id: int, db: Session = Depends(get_db)):
    opportunity = crud.get_opportunity_by_id(db, op_id=op_id)
    # returned_opportunity_list = [ for opportunity in
    #                              db_opportunity]
    return {"id": opportunity.id, "id_portomember": opportunity.id_portomember,
            "startDate": opportunity.startDate,
            "endDate": opportunity.endDate, "isactive": opportunity.isactive,
            "description": opportunity.description,
            "id_skill": opportunity.id_skill, "value": opportunity.value}


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


# Match REST

@app.post("/v1/match/", response_model=schemas.SchemeMatch, tags=["Match"])
def create_match(match: schemas.SchemeMatch = Body(...), db: Session = Depends(get_db)):
    match = crud.create_match(db=db, match=match)
    return {"id": match.id, "id_opportunity": match.id_opportunity, "id_pilarmember": match.id_pilarmember,
            "approved": match.approved}


@app.get("/v1/match/", response_model=List[schemas.SchemeMatch], tags=["Match"])
def get_match(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    match_list = crud.get_match(db=db, skip=skip, limit=limit)
    return [{"id": match.id, "id_opportunity": match.id_opportunity, "id_pilarmember": match.id_pilarmember,
             "approved": match.approved} for match in match_list]


@app.post("/v1/match/evaluation/", response_model=schemas.SchemeMatchEvaluation, tags=["Match"])
def create_match(evaluation: schemas.SchemeMatchEvaluation = Body(...), db: Session = Depends(get_db)):
    match = crud.create_match_evaluation(db=db, evaluation=evaluation)
    return match.__dict__


@app.get("/v1/match/evaluation/", response_model=List[schemas.SchemeMatchEvaluation], tags=["Match"])
def get_match(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    evaluation_list = crud.get_match_evaluation(db=db, skip=skip, limit=limit)
    return [match.__dict__ for match in evaluation_list]
