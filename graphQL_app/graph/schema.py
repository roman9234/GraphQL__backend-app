import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from graphQL_app.model.models import db_session, Department as DepartmentModel, Employee as EmployeeModel

# GraphQL представляет объекты в виде графической структуры, а не в виде более иерархической структуры.
# Чтобы создать такое представление, Graphene необходимо знать о каждом типе объектов, которые будут отображаться в графе.
# Этот граф также имеет тип root, через который начинается весь доступ. Это класс запросов, представленный ниже.
# В этом примере мы предоставляем возможность перечислять всех сотрудников с помощью all_employees и возможность получать конкретный узел с помощью node.


class Department(SQLAlchemyObjectType):
    class Meta:
        model = DepartmentModel
        interfaces = (relay.Node, )


class Employee(SQLAlchemyObjectType):
    class Meta:
        model = EmployeeModel
        interfaces = (relay.Node, )


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    # Allows sorting over multiple columns, by default over the primary key
    all_employees = SQLAlchemyConnectionField(Employee.connection)
    # Disable sorting over this field
    all_departments = SQLAlchemyConnectionField(Department.connection, sort=None)

schema = graphene.Schema(query=Query)