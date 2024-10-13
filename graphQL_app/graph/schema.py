import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from graphQL_app.model.models import db_session, Blog as BlogModel, User as UserModel, Post as PostModel


# GraphQL представляет объекты в виде графической структуры, а не в виде более иерархической структуры.
# Чтобы создать такое представление, Graphene необходимо знать о каждом типе объектов, которые будут отображаться в графе.
# Этот граф также имеет тип root, через который начинается весь доступ. Это класс запросов, представленный ниже.
# В этом примере мы предоставляем возможность перечислять всех сотрудников с помощью all_users и возможность получать конкретный узел с помощью node.


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


schema = graphene.Schema(query=Query)
