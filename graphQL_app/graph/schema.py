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
        interfaces = (relay.Node, )


class User(SQLAlchemyObjectType):
    class Meta:
        model = UserModel
        interfaces = (relay.Node, )

class Post(SQLAlchemyObjectType):
    class Meta:
        model = PostModel
        interfaces = (relay.Node, )

class Query(graphene.ObjectType):
    node = relay.Node.Field()
    # Allows sorting over multiple columns, by default over the primary key
    all_users = SQLAlchemyConnectionField(User.connection)
    # Disable sorting over this field
    all_blogs = SQLAlchemyConnectionField(Blog.connection)

    all_Posts = SQLAlchemyConnectionField(Post.connection)


schema = graphene.Schema(query=Query)