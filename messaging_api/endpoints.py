import hashlib

from fastapi import Depends, HTTPException, Header, status
from sqlalchemy.orm import Session

from messaging_api import crud, database, schemas, models


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


def _validate_auth_headers(
    username: str = Header(None),
    password: str = Header(None),
    db: Session = Depends(get_db)
) -> int:
    if (
        username is None or
        password is None or
        not (user := crud.get_user_by_username(db, username)) or
        user.hashed_password != hashlib.sha1(password.encode()).hexdigest()
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    return user.id


def user_create(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(
            status_code=400, detail="Username already registered"
        )

    return crud.create_user(db=db, user=user)


def user_list(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
    _=Depends(_validate_auth_headers)
):
    users = crud.get_users(db, skip=skip, limit=limit)

    return users


def user_message_create(
    user_id: int, message: schemas.MessageCreate,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(_validate_auth_headers)
):
    if not db.query(models.User).filter(models.User.id == user_id).first():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"The user with id {user_id} does not exist!"
        )

    if user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Creating messages on behalf of other users is not allowed."
        )

    return crud.create_user_message(db=db, message=message, user_id=user_id)


def user_message_list(
    user_id: int = None, db: Session = Depends(get_db),
    _=Depends(_validate_auth_headers)
):
    if user_id is None:
        return crud.get_messages(db)

    return crud.get_messages_by_user(db, user_id=user_id)
