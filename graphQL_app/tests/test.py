from graphQL_app.model.models import engine, db_session, Base, User, Blog, Post

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
# Введём тестовые данные
user1 = User(name='User1 name')
db_session.add(user1)

user2 = User(name='User2 name')
db_session.add(user2)

blog1 = Blog(owner=user1, name='User 1 blog')
db_session.add(blog1)

blog2 = Blog(owner=user1, name='User 1 second blog')
db_session.add(blog2)

user3 = User(name='User3 name')
db_session.add(user3)

post1 = Post(blog=blog1, title="Post in User 1's first blog", text="Lorum Ipsum")
db_session.add(post1)

db_session.commit()
