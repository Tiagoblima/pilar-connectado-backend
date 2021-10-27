from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext


from . import models, schemas

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_user(db: Session, user_id: int):

    return db.query(models.User).filter(models.User.id == user_id).first()




def get_user_by_email(db: Session, email: str):

    return db.query(models.User).filter(models.User.email == email).first()




def get_users(db: Session, skip: int = 0, limit: int = 100):

    return db.query(models.User).offset(skip).limit(limit).all()


def get_password_hash(password):
    return pwd_context.hash(password)


def create_user(db: Session, user: schemas.SchemeUser):
    
    db_user = models.User(name=user.name, address=user.address,
                         cpf=user.cpf,email=user.email, 
                         password=get_password_hash(user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user



def get_items(db: Session, skip: int = 0, limit: int = 100):

    return db.query(models.Item).offset(skip).limit(limit).all()



def create_user_item(db: Session, item: schemas.SchemePhone, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
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