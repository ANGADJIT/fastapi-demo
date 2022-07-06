from sqlalchemy.dialects.mysql import TINYINT, INTEGER, VARCHAR
from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Post(Base):
    __tablename__ = 'posts'

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    title = Column(VARCHAR(50), nullable=False)
    content = Column(VARCHAR(200), nullable=False)
    published = Column(TINYINT, nullable=False, server_default='1')
    rating = Column(INTEGER, nullable=True)
    user_id = Column(INTEGER, ForeignKey(
        'users.id', ondelete='CASCADE'), nullable=False)
    onwer = relationship('Users')


class Users(Base):
    __tablename__ = 'users'

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    email = Column(VARCHAR(64), nullable=False, unique=True)
    password = Column(VARCHAR(200), nullable=False)


class Votes(Base):
    __tablename__ = 'votes'

    user_id = Column(Integer, ForeignKey(
        'users.id', ondelete='CASCADE'), primary_key=True)
    post_id = Column(Integer, ForeignKey(
        'posts.id', ondelete='CASCADE'), primary_key=True)
