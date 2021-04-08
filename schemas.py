from typing import List, Optional
from pydantic import BaseModel



class MessageBase(BaseModel):
    keyword: str
    message:str
    options: Optional[List[str]]

#Creating class
class MessageCreate(MessageBase):
    pass

#Reading class
class Message(MessageBase):
    id: int
    class Config:
        orm_mode = True


class UserBase(BaseModel):
    name: str
    chat_id: int
    is_student: Optional[bool] = True

class UserCreate(UserBase):
    telegram_id: int
    pass

class User(UserBase):
    id: int
    class Config:
        orm_mode = True

# Telegram TOKEN
class TokenBase(BaseModel):
    bot_name: str
    token: str

class TokenCreate(TokenBase):
    pass

class Token(TokenBase):
    id: int
    class Config:
        orm_mode = True


    