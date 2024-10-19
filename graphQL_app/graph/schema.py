import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from graphQL_app.model.models import db_session, Blog as BlogGrapheneModel, User as UserGrapheneModel, \
    Post as PostGrapheneModel

# from flask_graphql_auth import create_access_token, query_header_jwt_required, create_refresh_token


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

    @classmethod
    def mutate(cls, info, name, email, password):
        user = UserGrapheneModel(name=name, email=email, password=password)
        db_session.add(user)
        db_session.commit()
        return CreateUser(user=user)


class UpdateUser(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        name = graphene.String()

    user = graphene.Field(lambda: UserSQLObject)

    @classmethod
    def mutate(cls, info, id, name=None):
        user = db_session.query(UserGrapheneModel).get(id)
        if user is None:
            raise Exception('User not found')

        if name is not None:
            user.name = name

        db_session.commit()
        return UpdateUser(user=user)


class CreateBlog(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        user_id = graphene.Int(required=True)

    blog = graphene.Field(lambda: BlogSQLObject)

    @classmethod
    def mutate(cls, info, name, user_id):
        blog = BlogGrapheneModel(name=name, user_id=user_id)
        db_session.add(blog)
        db_session.commit()
        return CreateBlog(blog=blog)


class UpdateBlog(graphene.Mutation):
    class Arguments:
        blog_id = graphene.Int(required=True)
        name = graphene.String()

    blog = graphene.Field(lambda: BlogSQLObject)

    @classmethod
    def mutate(cls, info, blog_id, name=None):
        blog = db_session.query(BlogGrapheneModel).get(blog_id)
        if blog is None:
            raise Exception('Blog not found')

        if name is not None:
            blog.name = name

        db_session.commit()
        return UpdateBlog(blog=blog)


class CreatePost(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        text = graphene.String(required=True)
        blog_id = graphene.Int(required=True)

    post = graphene.Field(lambda: PostSQLObject)

    @classmethod
    def mutate(cls, info, title, text, blog_id):
        post = PostGrapheneModel(title=title, text=text, blog_id=blog_id)
        db_session.add(post)
        db_session.commit()
        return CreatePost(post=post)


class UpdatePost(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        title = graphene.String()
        text = graphene.String()

    post = graphene.Field(lambda: PostSQLObject)

    @classmethod
    def mutate(cls, info, id, title=None, text=None):
        post = db_session.query(PostGrapheneModel).get(id)
        if post is None:
            raise Exception('Post not found')

        if title is not None:
            post.title = title
        if text is not None:
            post.text = text

        db_session.commit()
        return UpdatePost(post=post)


# Аутентификация
class AuthMutation(graphene.Mutation):
    class Arguments(object):
        email = graphene.String()
        password = graphene.String()

    access_token = graphene.String()
    refresh_token = graphene.String()

    def mutate(cls, info, email, password):
        # Строчку ниже надо исправить

        user = db_session.query(UserGrapheneModel).filter_by(email=email).first()
        print(user)


        if user and user.password == password:
            return AuthMutation(
                # access_token=create_access_token(email),
                # refresh_token=create_refresh_token(email),
                access_token="new_token_"+email,
                refresh_token="new_refresh_token_"+email,
            )
        else:
            raise Exception("Неверный email или пароль")


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    create_blog = CreateBlog.Field()
    update_blog = UpdateBlog.Field()
    create_post = CreatePost.Field()
    update_post = UpdatePost.Field()
    auth = AuthMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
