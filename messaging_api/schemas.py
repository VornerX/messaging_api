from datetime import datetime

from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    """ User creation """
    id: int | None = None
    password: str


class User(UserBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class MessageBase(BaseModel):
    content: str


class MessageCreate(MessageBase):
    """ Create a message from a user """
    pass


class Message(MessageBase):
    id: int
    user_id: int
    created: datetime

    model_config = ConfigDict(from_attributes=True)
