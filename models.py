from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(String, index=True)
    telegram_id = Column(Integer, index=True)
    name = Column(String)
    is_student = Column(Boolean)

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    keyword = Column(String, index=True, unique=True)
    message = Column(String)
    options = Column(ARRAY(String), nullable=True)

class Token(Base):
    __tablename__ = "tokens"
    id = Column(Integer, primary_key=True, index=True)
    bot_name = Column(String, nullable=False, unique=True)
    token = Column(String, nullable=False)

