from sqlalchemy import *
from sqlalchemy.orm import (scoped_session, sessionmaker, relationship,
                            backref)
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///../database/database.sqlite3', convert_unicode=True)

db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base = declarative_base()
# Это нам потребуется для запрсов
Base.query = db_session.query_property()


# class Blog(Base):
#     __tablename__ = 'department'
#     id = Column(Integer, primary_key=True)
#     name = Column(String)
#
#
#
# class User(Base):
#     __tablename__ = 'employee'
#     id = Column(Integer, primary_key=True)
#     name = Column(String)
#     hired_on = Column(DateTime, default=func.now())
#     department_id = Column(Integer, ForeignKey('department.id'))
#     department = relationship(
#         Blog,
#         backref=backref('employees',
#                         uselist=True,
#                         cascade='delete,all'))

class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True)
    user_name = Column(String, nullable=False)


class Blog(Base):
    __tablename__ = "blogs"
    blog_id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey('users.user_id'))
    blog_name = Column(String, nullable=False)

    owner = relationship(
        User,
        backref=backref('blogs', uselist=True, cascade='delete,all')
    )


class Post(Base):
    __tablename__ = "posts"
    post_id = Column(Integer, primary_key=True)
    blog_id = Column(Integer, ForeignKey('blogs.blog_id'))
    title = Column(String, nullable=True)
    text = Column(String)

    post_blog = relationship(
        Blog,
        backref=backref('posts', uselist=True, cascade='delete,all')
    )