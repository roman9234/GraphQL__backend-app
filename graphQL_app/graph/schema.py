from datetime import datetime, timedelta
from typing import Any

import graphene
import jwt
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField

from flask import current_app
from graphQL_app.model.models import db_session, Blog as BlogGrapheneModel, User as UserGrapheneModel, \
    Post as PostGrapheneModel


class AuthenticationError(Exception):
    pass


# from flask_graphql_auth import create_access_token, query_header_jwt_required, create_refresh_token

def get_secret_key() -> str:
    with current_app.app_context():
        return current_app.config['SECRET_KEY']


def get_expiry_time() -> dict:
    with current_app.app_context():
        return current_app.config['JWT_EXPIRE_TIME']


def get_user_by_email_and_password(email, password) -> UserGrapheneModel:
    user = db_session.query(UserGrapheneModel).filter_by(email=email).first()
    if user and user.password == password:
        return user
    else:
        raise AuthenticationError("Email or password is incorrect")


def get_jwt_for_user(user: UserGrapheneModel) -> str:
    # Создаёт токен для авторизации пользователя

    _jwt_token = jwt.encode({
        "id": user.id,
        "email": user.email,
        "expiration": (datetime.now() + timedelta(**get_expiry_time())).strftime("%Y-%m-%d %H:%M:%S")
    },
        get_secret_key(),
        algorithm='HS256')

    return _jwt_token


def _jwt_expired(_jwt_token: str) -> bool:
    payload = jwt.decode(_jwt_token, get_secret_key(), algorithms=['HS256'])
    # False значит время актуальности JWT ещё не вышло
    return datetime.strptime(payload["expiration"], "%Y-%m-%d %H:%M:%S") < datetime.now()


def get_user_from_jwt(_jwt_token: str) -> UserGrapheneModel:
    payload = jwt.decode(_jwt_token, get_secret_key(), algorithms=['HS256'])
    user = db_session.query(UserGrapheneModel).filter_by(email=payload["email"], id=payload["id"]).first()
    if user is None:
        raise AuthenticationError("Failed to find autentificated user")
    return user


# GraphQL представляет объекты в виде графической структуры, а не в виде более иерархической структуры.
# Чтобы создать такое представление, Graphene необходимо знать о каждом типе объектов, которые будут отображаться в графе.
# Этот граф также имеет тип root, через который начинается весь доступ. Это класс запросов, представленный ниже.
# В этом примере мы предоставляем возможность перечислять всех сотрудников с помощью all_users и возможность получать конкретный узел с помощью node.


class BlogSQLObject(SQLAlchemyObjectType):
    class Meta:
        model = BlogGrapheneModel
        interfaces = (relay.Node,)


class UserSQLObject(SQLAlchemyObjectType):
    class Meta:
        model = UserGrapheneModel
        interfaces = (relay.Node,)


class PostSQLObject(SQLAlchemyObjectType):
    class Meta:
        model = PostGrapheneModel
        interfaces = (relay.Node,)


class Query(graphene.ObjectType):
    node = relay.Node.Field()

    # all_users = SQLAlchemyConnectionField(UserSQLObject.connection)
    all_users = SQLAlchemyConnectionField(UserSQLObject)

    all_blogs = SQLAlchemyConnectionField(BlogSQLObject)

    all_Posts = SQLAlchemyConnectionField(PostSQLObject)
    # Получить конкретного пользователя по id
    get_user = graphene.Field(UserSQLObject, id=graphene.Int())
    # Получить конкретный пост по id
    get_post = graphene.Field(PostSQLObject, id=graphene.Int())
    # Получить конкретный блог по id
    get_blog = graphene.Field(BlogSQLObject, id=graphene.Int())
    # Получить все посты в Блоге по id
    get_blog_posts = graphene.Field(lambda: graphene.List(PostSQLObject), id=graphene.Int())
    # Получить все блоги пользователя id
    get_user_blogs = graphene.Field(lambda: graphene.List(BlogSQLObject), id=graphene.Int())

    # расчёт запросов
    def resolve_get_user(parent, info, id):
        query = UserSQLObject.get_query(info)
        return query.filter(UserGrapheneModel.id == id).first()

    def resolve_get_post(parent, info, id):
        query = PostSQLObject.get_query(info)
        return query.filter(PostGrapheneModel.id == id).first()

    def resolve_get_blog(parent, info, id):
        query = BlogSQLObject.get_query(info)
        return query.filter(BlogGrapheneModel.id == id).first()

    def resolve_get_blog_posts(parent, info, id):
        query = BlogSQLObject.get_query(info)
        return query.filter(PostGrapheneModel.blog_id == id).all()

    def resolve_get_user_blogs(parent, info, id):
        query = UserSQLObject.get_query(info)
        return query.filter(BlogGrapheneModel.user_id == id).all()


class CreateUser(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    user = graphene.Field(lambda: UserSQLObject)

    def mutate(self, info, name, email, password):
        user = UserGrapheneModel(name=name, email=email, password=password)
        db_session.add(user)
        db_session.commit()
        return CreateUser(user=user)


class UpdateUser(graphene.Mutation):
    class Arguments:
        access_token = graphene.String()
        id = graphene.Int(required=True)
        name = graphene.String()

    user = graphene.Field(lambda: UserSQLObject)

    def mutate(self, info, access_token, id, name=None):

        # Аутентификация
        if _jwt_expired(access_token):
            raise AuthenticationError("jwt_token is expired")
        user_from_jwt = get_user_from_jwt(access_token)
        #

        user = db_session.query(UserGrapheneModel).get(id)
        if user_from_jwt == user:

            if user is None:
                raise Exception('User not found')

            if name is not None:
                user.name = name

            db_session.commit()
            return UpdateUser(user=user)

        else:
            raise AuthenticationError("Acces denied")


class CreateBlog(graphene.Mutation):
    class Arguments:
        access_token = graphene.String()
        name = graphene.String(required=True)
        user_id = graphene.Int(required=True)

    blog = graphene.Field(lambda: BlogSQLObject)

    def mutate(self, info, access_token, name, user_id):

        # Аутентификация
        if _jwt_expired(access_token):
            raise AuthenticationError("jwt_token is expired")
        user_from_jwt = get_user_from_jwt(access_token)
        #
        if user_from_jwt.id == user_id:

            blog = BlogGrapheneModel(name=name, user_id=user_id)
            db_session.add(blog)
            db_session.commit()
            return CreateBlog(blog=blog)

        else:
            raise AuthenticationError("acces denied")


class UpdateBlog(graphene.Mutation):
    class Arguments:
        access_token = graphene.String()
        blog_id = graphene.Int(required=True)
        name = graphene.String()

    blog = graphene.Field(lambda: BlogSQLObject)

    def mutate(self, info, access_token, blog_id, name=None):

        # Аутентификация
        if _jwt_expired(access_token):
            raise AuthenticationError("jwt_token is expired")
        user_from_jwt = get_user_from_jwt(access_token)
        #

        blog = db_session.query(BlogGrapheneModel).get(blog_id)

        if blog is None:
            raise Exception('Blog not found')

        if blog.user_id == user_from_jwt.id:

            if name is not None:
                blog.name = name

            db_session.commit()
            return UpdateBlog(blog=blog)

        else:
            raise AuthenticationError("acces denied")


class CreatePost(graphene.Mutation):
    class Arguments:
        access_token = graphene.String()
        title = graphene.String(required=True)
        text = graphene.String(required=True)
        blog_id = graphene.Int(required=True)

    post = graphene.Field(lambda: PostSQLObject)

    def mutate(self, info, access_token, title, text, blog_id):

        # Аутентификация
        if _jwt_expired(access_token):
            raise AuthenticationError("jwt_token is expired")
        user_from_jwt = get_user_from_jwt(access_token)
        blog = db_session.query(BlogGrapheneModel).get(blog_id)
        #

        if blog.user_id == user_from_jwt.id:

            post = PostGrapheneModel(title=title, text=text, blog_id=blog_id)
            db_session.add(post)
            db_session.commit()
            return CreatePost(post=post)
        else:
            raise AuthenticationError("acces denied")


class UpdatePost(graphene.Mutation):
    class Arguments:
        access_token = graphene.String()
        id = graphene.Int(required=True)
        title = graphene.String()
        text = graphene.String()

    post = graphene.Field(lambda: PostSQLObject)

    def mutate(self, info, access_token, id, title=None, text=None):

        # Аутентификация
        if _jwt_expired(access_token):
            raise AuthenticationError("jwt_token is expired")
        user_from_jwt = get_user_from_jwt(access_token)
        #
        post = db_session.query(PostGrapheneModel).get(id)
        blog = db_session.query(BlogGrapheneModel).get(post.blog_id)

        if blog.user_id == user_from_jwt.id:

            if post is None:
                raise Exception('Post not found')

            if title is not None:
                post.title = title
            if text is not None:
                post.text = text

            db_session.commit()
            return UpdatePost(post=post)
        else:
            raise AuthenticationError("acces denied")


# Аутентификация
class AuthMutation(graphene.Mutation):
    class Arguments(object):
        email = graphene.String()
        password = graphene.String()

    access_token = graphene.String()

    def mutate(self, info, email, password):
        # Строчку ниже надо исправить

        user = get_user_by_email_and_password(email, password)
        token = get_jwt_for_user(user)

        get_jwt_for_user(user)
        return AuthMutation(
            access_token=token
        )


# Аутентификация
class AuthCheckMutation(graphene.Mutation):
    class Arguments(object):
        access_token = graphene.String()

    result = graphene.String()

    def mutate(self, info, access_token):
        try:
            if _jwt_expired(access_token):
                return AuthCheckMutation(result="jwt_token is expired")
            else:
                user = get_user_from_jwt(access_token)
                return AuthCheckMutation(result=f"authentication jwt_token is correct. User email={user.email}")
        except Exception as e:
            return AuthCheckMutation(result=f"authentication failed due to unexpected exception: {e}")


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    create_blog = CreateBlog.Field()
    update_blog = UpdateBlog.Field()
    create_post = CreatePost.Field()
    update_post = UpdatePost.Field()
    authentication = AuthMutation.Field()
    check_authentication = AuthCheckMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
