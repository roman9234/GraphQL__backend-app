import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from graphQL_app.model.models import db_session, Blog as BlogModel, User as UserModel, Post as PostModel

from flask_graphql_auth import (
    AuthInfoField,
    get_jwt_identity,
    create_access_token,
    create_refresh_token,
    query_jwt_required,
    mutation_jwt_refresh_token_required,
    mutation_jwt_required,
)


# GraphQL представляет объекты в виде графической структуры, а не в виде более иерархической структуры.
# Чтобы создать такое представление, Graphene необходимо знать о каждом типе объектов, которые будут отображаться в графе.
# Этот граф также имеет тип root, через который начинается весь доступ. Это класс запросов, представленный ниже.
# В этом примере мы предоставляем возможность перечислять всех сотрудников с помощью all_users и возможность получать конкретный узел с помощью node.


class MessageField(graphene.ObjectType):
    message = graphene.String()


class ProtectedUnion(graphene.Union):
    class Meta:
        types = (MessageField, AuthInfoField)

    @classmethod
    def resolve_type(cls, instance, info):
        return type(instance)


class Blog(SQLAlchemyObjectType):
    class Meta:
        model = BlogModel
        interfaces = (relay.Node,)


class User(SQLAlchemyObjectType):
    class Meta:
        model = UserModel
        interfaces = (relay.Node,)


class Post(SQLAlchemyObjectType):
    class Meta:
        model = PostModel
        interfaces = (relay.Node,)


class Query(graphene.ObjectType):
    node = relay.Node.Field()

    # all_users = SQLAlchemyConnectionField(User.connection)
    all_users = SQLAlchemyConnectionField(User)

    all_blogs = SQLAlchemyConnectionField(Blog)

    all_Posts = SQLAlchemyConnectionField(Post)
    # Получить конкретного пользователя по имени
    get_user = graphene.Field(User, name=graphene.String())
    # Получить конкретный пост по id
    get_post = graphene.Field(Post, id=graphene.Int())
    # Получить конкретный блог по id
    get_blog = graphene.Field(Blog, id=graphene.Int())
    # Получить все посты в Блоге по id
    get_blog_posts = graphene.Field(lambda: graphene.List(Post), id=graphene.Int())
    # Получить все блоги пользователя id
    get_user_blogs = graphene.Field(lambda: graphene.List(Blog), id=graphene.Int())

    # расчёт более сложных запросов
    def resolve_get_user(parent, info, name):
        query = User.get_query(info)
        return query.filter(UserModel.name == name).first()

    def resolve_get_post(parent, info, id):
        query = Post.get_query(info)
        return query.filter(PostModel.id == id).first()

    def resolve_get_blog(parent, info, id):
        query = Blog.get_query(info)
        return query.filter(BlogModel.id == id).first()

    def resolve_get_blog_posts(parent, info, id):
        query = Blog.get_query(info)
        return query.filter(PostModel.blog_id == id).all()

    def resolve_get_user_blogs(parent, info, id):
        query = User.get_query(info)
        return query.filter(BlogModel.user_id == id).all()

    # AUTH tests
    protected = graphene.Field(type=ProtectedUnion, token=graphene.String())

    @query_jwt_required
    def resolve_protected(self, info):
        return MessageField(message="Hello World!")


class AuthMutation(graphene.Mutation):
    class Arguments(object):
        username = graphene.String()
        password = graphene.String()

    access_token = graphene.String()
    refresh_token = graphene.String()

    @classmethod
    def mutate(cls, _, info, username, password):
        return AuthMutation(
            access_token=create_access_token(username),
            refresh_token=create_refresh_token(username),
        )


class ProtectedMutation(graphene.Mutation):
    class Arguments(object):
        token = graphene.String()

    message = graphene.Field(ProtectedUnion)

    @classmethod
    @mutation_jwt_required
    def mutate(cls, _, info):
        return ProtectedMutation(
            message=MessageField(message="Protected mutation works")
        )


class RefreshMutation(graphene.Mutation):
    class Arguments(object):
        refresh_token = graphene.String()

    new_token = graphene.String()

    @classmethod
    @mutation_jwt_refresh_token_required
    def mutate(self, _):
        current_user = get_jwt_identity()
        return RefreshMutation(
            new_token=create_access_token(identity=current_user),
        )


class Mutation(graphene.ObjectType):
    auth = AuthMutation.Field()
    refresh = RefreshMutation.Field()
    protected = ProtectedMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
