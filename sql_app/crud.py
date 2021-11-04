from sqlalchemy import ForeignKey
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
import sqlalchemy
from . import models, schemas

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

metadata = sqlalchemy.MetaData()

users = sqlalchemy.Table(
    "Users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("email", sqlalchemy.String),
    sqlalchemy.Column("password", sqlalchemy.Boolean),
    sqlalchemy.Column("name", sqlalchemy.String),
    sqlalchemy.Column("address", sqlalchemy.String),
    sqlalchemy.Column("cpf", sqlalchemy.String),

)

posts = sqlalchemy.Table(
    "PilarMemberPost",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("user_id", sqlalchemy.Integer, ForeignKey("Users.id"), index=True),
    sqlalchemy.Column("description", sqlalchemy.String),
    sqlalchemy.Column("rate", sqlalchemy.Integer),


)
def get_user(db: Session, user_id: int):
    return db.query(models.Users).filter(models.Users.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.Users).filter(models.Users.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Users).offset(skip).limit(limit).all()


def get_pilar_member(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.PilarMember).offset(skip).limit(limit).all()


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
    return db.query(models.Item).offset(skip).limit(limit).all()


def get_posts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.PilarMemberPost).offset(skip).limit(limit).all()


def create_pilar_member_post(db: Session, post: schemas.SchemePilarMemberPost):

    db_item = models.PilarMemberPost(id=post.id,
                                     user_id=post.user_id,
                                     description=post.description,
                                     rate=post.rate
                                     )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def save_core(user):
    """
    Cria um usuário no banco de dados
    """

    NotImplemented


def update(user_id, user_uptaded):
    """
    Atualiza o usuário no banco de dados

    """

    NotImplemented


def get_by_id(user_id):
    """
    Acessa o usário no banco pelo login e retorna as informações
    """

    NotImplemented


def get_by_login(login):
    """
    Acessa o usário no banco pelo ID e retorna o usuário
    """

    NotImplemented


def delete(user_id):
    """
    Deleta o usuário do banco de dados.
    """

    NotImplemented
