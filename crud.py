from sqlalchemy.orm import Session
import schemas
from sqlalchemy.exc import SQLAlchemyError
import models

def get_user(db: Session, user_id:int):
    return db.query(models.User).filter(models.User.telegram_id == user_id).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
                name = user.name, 
                telegram_id = user.telegram_id,
                chat_id = user.chat_id
              )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_messages(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Message).offset(skip).limit(limit).all()

def create_message(db: Session, message: schemas.MessageCreate):
    db_message = models.Message(
        keyword= message.keyword.lower(),
        message = message.message,
        options = message.options
    )
    try:
        db.add(db_message)
        db.commit()
        db.refresh(db_message)
        return db_message
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        return 'Request falhou! Um erro foi encontrado: ' + error

def get_token(db: Session, bot_name: str = 'nubot'):
    return db.query(models.Token).filter(models.Token.bot_name == bot_name).first()

def create_token(db: Session, token: schemas.TokenCreate):
    db_token = models.Token(
                bot_name = token.bot_name,
                token = token.token
            )
    db.add(db_token)
    db.commit()
    db.refresh(db_token)
    return db_token

def query_keyword(db: Session, keyword: str):
    result = None
    try:
        result = db.query(models.Message).filter(models.Message.keyword == keyword).first()
    except:
        result = None
    return result

def delete_message(db: Session, keyword: str):
    try:
        db.query(models.Message).filter(models.Message.keyword == keyword).delete()
        db.commit()
        return 'Mensagem deletada. Keyword: ' + keyword
    except SQLAlchemyError as e:
        print(e)
        return None
