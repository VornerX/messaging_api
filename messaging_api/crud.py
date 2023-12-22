import hashlib

from sqlalchemy.orm import Session

from messaging_api import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = hashlib.sha1(user.password.encode()).hexdigest()
    db_user = models.User(
        username=user.username, hashed_password=hashed_password, id=user.id
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def delete_user(db: Session, user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        return None
    db.delete(user)
    db.commit()

    return user


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(
        models.User.username == username
    ).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user_message(
    db: Session, message: schemas.MessageCreate, user_id: int
):
    db_message = models.Message(**message.model_dump(), user_id=user_id)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)

    return db_message


def get_messages(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Message).offset(skip).limit(limit).all()


def get_messages_by_user(db: Session, user_id: int):
    return db.query(models.Message).filter(
        models.Message.user_id == user_id
    ).all()


def delete_messages_by_user_id(db: Session, user_id: int):
    db.query(models.Message).filter(models.Message.user_id == user_id).delete()
    db.commit()
