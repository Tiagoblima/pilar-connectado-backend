from sqlalchemy.orm import Session



import models, schemas




def get_user(db: Session, user_id: int):

    return db.query(models.User).filter(models.User.id == user_id).first()




def get_user_by_email(db: Session, email: str):

    return db.query(models.User).filter(models.User.email == email).first()




def get_users(db: Session, skip: int = 0, limit: int = 100):

    return db.query(models.User).offset(skip).limit(limit).all()



def create_user(db: Session, user: schemas.SchemeUser):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
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