from sqlalchemy import *
from sqlalchemy.orm import (scoped_session, sessionmaker, relationship,
                            backref)
from sqlalchemy.ext.declarative import declarative_base

# Здесь происходит инициализация базы данных
engine = create_engine('sqlite:///../database/database.sqlite3', convert_unicode=True)

db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base = declarative_base()
# Это нам потребуется для запросов
Base.query = db_session.query_property()


class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True)
    blog_id = Column(Integer, ForeignKey('blogs.id'))
    title = Column(String, nullable=True)
    text = Column(String)


class Blog(Base):
    __tablename__ = "blogs"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    name = Column(String, nullable=False)

    posts = relationship(
        Post,
        backref=backref('blog'), uselist=True, cascade='delete,all'
    )


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)

    blogs = relationship(
        Blog,
        backref=backref('owner'), uselist=True, cascade='delete,all'
    )
