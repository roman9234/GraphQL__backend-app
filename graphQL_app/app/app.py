from flask import Flask
from flask_graphql import GraphQLView

from graphQL_app.model.models import db_session
from graphQL_app.graph.schema import schema, Department

# Создание View GraphQL в Flask
# В отличие от Restful, в GraphQL используется толкьо 1 URL для доступа к данным
# Мы будем использовать Flask для создания сервера, который предоставляет схему GraphQL в /graphql/ и интерфейс для простых запросов к ней.
# Также в /graphql/ при доступе через браузер будет окно ввода запрсов
# Библиотека Flask-GraphQL, которую мы установили ранее, значительно упрощает эту задачу.

app = Flask(__name__)
app.debug = True

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
