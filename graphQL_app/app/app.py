import graphene


# Полная копия типа User из фронтенда
class User(graphene.ObjectType):
    id = graphene.ID()
    username = graphene.String()


class Query(graphene.ObjectType):
    get_user = graphene.Field(User)

    # Так в GraphQL обрабатываются запросы
    @staticmethod
    def resolve_get_user(root, info):
        new_user = User()
        new_user.id = 0
        new_user.username = "Andrew"
        return new_user


# Переходим к саой схеме
# Схема это самая важная часть GraphQL, которая содержит все возможные запросы

schema = graphene.Schema(query=Query)
# Получим данные
results = schema.execute("""
    query{
        getUser{
            id
            username
        }    
    }
""")
print(results.data)
# {'getUser': {'id': '0', 'username': 'Andrew'}}














