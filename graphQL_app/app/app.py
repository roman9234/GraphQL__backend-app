from flask import Flask
from flask_graphql import GraphQLView

from graphQL_app.model.models import db_session
from graphQL_app.graph.schema import schema

# Создание View GraphQL в Flask
# В отличие от Restful, в GraphQL используется толкьо 1 URL для доступа к данным
# Мы будем использовать Flask для создания сервера, который предоставляет схему GraphQL в /graphql/ и интерфейс для простых запросов к ней.
# Также в /graphql/ при доступе через браузер будет окно ввода запрсов
# Библиотека Flask-GraphQL, которую мы установили ранее, значительно упрощает эту задачу.

# flask-graphql - Flask Package that will allow us to use GraphiQL IDE in the browser graphene - Python library for building GraphQL APIs graphene-sqlalchemy - Graphene package that works with SQLAlchemy to simplify working with our models

# Если пользователь авторизован, он может создать блог
# Если пользователь владеет блогом, он может создавать, редактировать и удалять посты, а также сам блог
# Если пользователь подписан на блог, он может смотреть посты


app = Flask(__name__)
app.debug = True

# IDE  GraphiQL позволяет тестировать запросы GraphQL непосредственно в браузере
app.add_url_rule(
    '/graphql/',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True  # это значение нужно, чтобы иметь интерфейс GraphQL
    )
)


# При закрытии контектса, закрывается подключение к БД
@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


if __name__ == '__main__':
    app.run()
