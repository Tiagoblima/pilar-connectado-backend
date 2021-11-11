import sqlalchemy
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from . import models, schemas
from .database import SessionLocal

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

metadata = sqlalchemy.MetaData()

# users = sqlalchemy.Table(
#     "Users",
#     metadata,
#     sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
#     sqlalchemy.Column("email", sqlalchemy.String),
#     sqlalchemy.Column("password", sqlalchemy.Boolean),
#     sqlalchemy.Column("name", sqlalchemy.String),
#     sqlalchemy.Column("address", sqlalchemy.String),
#     sqlalchemy.Column("cpf", sqlalchemy.String),
#
# )

# posts = sqlalchemy.Table(
#     "PilarMemberPost",
#     metadata,
#     sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
#     sqlalchemy.Column("user_id", sqlalchemy.Integer, ForeignKey("Users.id"), index=True),
#     sqlalchemy.Column("description", sqlalchemy.String),
#     sqlalchemy.Column("rate", sqlalchemy.Integer),
#
#
# )

#
#
# def update(user_id, user_uptaded):
#     """
#     Atualiza o usuário no banco de dados
#
#     """
#
#     NotImplemented
#
#
# def delete(user_id):
#     """
#     Deleta o usuário do banco de dados.
#     """
#
#     NotImplemented


security = HTTPBasic()


def get_user(db: Session, user_id: int):
    return db.query(models.Users).filter(models.Users.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.Users).filter(models.Users.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Users).offset(skip).limit(limit).all()


def get_pilar_member(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.PilarMember).offset(skip).limit(limit).all()


def get_member(db, id_user):
    response = db.query(models.PilarMember).filter(models.PilarMember.id_user == id_user).first()
    if not response:
        response = db.query(models.PortoMember).filter(models.PortoMember.id_user == id_user).first()
    return response


def get_pilar_member_by_skill(db, id_skill, skip, limit):
    skill_pilar_member = db.query(models.SkillPilarMember).filter(models.SkillPilarMember.id_skill == id_skill).offset(
        skip).limit(limit).all()

    users_list = []
    for skill_pilar in skill_pilar_member:
        pilar_member = db.query(models.PilarMember).filter(
            models.PilarMember.id == skill_pilar.id_pilarmember).first().__dict__
        user = db.query(models.Users).filter(models.Users.id == pilar_member["id_user"]).first().__dict__
        user.update(pilar_member)
        user.update(skill_pilar.__dict__)
        user.pop("password")
        user.pop("id_pilarmember")
        user.pop("id")
        user.pop("id_skill")
        users_list.append(user)

    return users_list


def get_password_hash(password):
    return pwd_context.hash(password)


def create_user(db: Session, user: schemas.SchemeUsers):
    db_user = models.Users(name=user.name, address=user.address,
                           cpf=user.cpf, email=user.email,
                           password=get_password_hash(user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_pilar_member(db: Session, pilar_mbm: schemas.SchemePilarMember):
    db_pilar_mbm = models.PilarMember(introduction=pilar_mbm.introduction,
                                      instagram=pilar_mbm.instagram,
                                      id_user=pilar_mbm.id_user, evaluation=pilar_mbm.evaluation)
    db.add(db_pilar_mbm)
    db.commit()
    db.refresh(db_pilar_mbm)
    return db_pilar_mbm


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Phone).offset(skip).limit(limit).all()


def get_posts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.PilarMemberPost).offset(skip).limit(limit).all()


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(db, username: str, password: str):
    db_user = get_user_by_email(db, email=username)

    if not db_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email não registrado.",
                            headers={"WWW-Authenticate": "Basic"})

    if not verify_password(password, db_user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Senha inválida",
                            headers={"WWW-Authenticate": "Basic"})

    return db_user


def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    db = SessionLocal()

    return authenticate_user(db, username=credentials.username, password=credentials.password)


def create_pilar_member_post(db: Session, post: schemas.SchemePilarMemberPost):
    db_item = models.PilarMemberPost(
        user_id=post.user_id,
        description=post.description,
        rate=post.rate
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def create_post(db: Session, post: schemas.SchemePilarMemberPost):
    db_post = models.PilarMemberPost(user_id=post.user_id, description=post.description, rate=post.rate)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def create_porto_member(db, porto_mbm):
    db_porto_mbm = models.PortoMember(id_user=porto_mbm.id_user, workaddress=porto_mbm.workaddress)
    db.add(db_porto_mbm)
    db.commit()
    db.refresh(db_porto_mbm)
    return db_porto_mbm


def get_porto_member(db, skip, limit):
    return db.query(models.PortoMember).offset(skip).limit(limit).all()


def create_skill(db, skill):
    db_skill = models.Skill(**skill.dict())
    db.add(db_skill)
    db.commit()
    db.refresh(db_skill)
    return db_skill


def get_skill(db, skip, limit):
    return db.query(models.Skill).offset(skip).limit(limit).all()


def create_skill_pilar_member(db, skill_pilar_member):
    db_skill = models.SkillPilarMember(**skill_pilar_member.dict())
    db.add(db_skill)
    db.commit()
    db.refresh(db_skill)
    return db_skill


def get_skill_pilar_member(db, skip, limit):
    return db.query(models.SkillPilarMember).offset(skip).limit(limit).all()


def create_opportunity(db: Session, opportunity: schemas.SchemeOpportunity):
    db_opportunity = models.Opportunity(**opportunity.dict())
    db.add(db_opportunity)
    db.commit()
    db.refresh(db_opportunity)
    return db_opportunity


def get_opportunity(db, skip, limit):
    return db.query(models.Opportunity).offset(skip).limit(limit).all()


def get_opportunity_by_id(db, op_id):
    return db.query(models.Opportunity).filter(models.Opportunity.id == op_id).first()


def get_opportunity_by_porto_member_id(db, id_porto_member, skip, limit):
    return db.query(models.Opportunity).filter(models.Opportunity.id_portomember == id_porto_member). \
        offset(skip).limit(limit).all()


def create_match(db, match: schemas.SchemeMatch):
    db_match = models.Match(**match.dict())
    db.add(db_match)
    db.commit()
    db.refresh(db_match)
    return db_match


def get_match(db, skip, limit):
    return db.query(models.Match).offset(skip).limit(limit).all()


def get_opportunity_by_id_skill(db, id_skill, skip, limit):
    return db.query(models.Opportunity).filter(models.Opportunity.id_skill == id_skill). \
        offset(skip).limit(limit).all()


def create_match_evaluation(db, evaluation: schemas.SchemeMatchEvaluation):
    db_evaluation = models.MatchEvaluation(**evaluation.dict())
    db.add(db_evaluation)
    db.commit()
    db.refresh(db_evaluation)
    return db_evaluation


def get_match_evaluation(db, skip, limit):
    return db.query(models.MatchEvaluation).offset(skip).limit(limit).all()