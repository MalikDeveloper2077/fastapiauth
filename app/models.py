from sqlalchemy import Column, Integer, String

from app.config import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(30), unique=True)
    password = Column(String(100))
